#!/usr/bin/env python3
"""Minimal pytest-compatible runner for candidate-y's OWN test suite.

WHY THIS EXISTS
---------------
candidate-y's declared test command is `pytest`. In this evaluation
environment there is no network access, and pytest is not installed and cannot
be installed offline (no wheel in the local pip cache). This runner is an
evaluator-generated SUBSTITUTE: it installs a tiny fake `pytest` module that
implements only the features candidate-y's tests actually use
(`pytest.fixture`, `pytest.raises`, and the builtin `monkeypatch` / `capsys`
fixtures), then discovers and runs the candidate's test files UNMODIFIED.

This is NOT the official pytest. It is a best-effort substitute for the
`Run each candidate's test suite` step under a no-network environment
limitation. Results should be read with that caveat.

Usage:
    python3 run_candidate_y_tests.py /path/to/extracted/candidate-y
"""
from __future__ import annotations

import importlib.util
import inspect
import io
import sys
import types
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None
if root is None:
    print("ERROR: pass the extracted candidate-y directory as argv[1]", file=sys.stderr)
    sys.exit(2)


# --------------------------------------------------------------------------
# Fake `pytest` module (only what candidate-y's tests use)
# --------------------------------------------------------------------------
class _FixtureMarker:
    def __init__(self, func):
        self.func = func


def fixture(func=None, **_kwargs):
    if func is None:  # called as @pytest.fixture(...) with kwargs
        return lambda f: _FixtureMarker(f)
    return _FixtureMarker(func)


class _Raises:
    def __init__(self, expected):
        self.expected = expected

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            raise AssertionError(f"DID NOT RAISE {self.expected!r}")
        return issubclass(exc_type, self.expected)


def raises(expected):
    return _Raises(expected)


def approx(value, rel=1e-6, abs=1e-12):  # not used by candidate-y, provided for safety
    class _A:
        def __eq__(self, other):
            return abs_((other - value)) <= max(rel * abs_(value), abs)
    def abs_(x):
        return x if x >= 0 else -x
    return _A()


class _Mark:
    def __getattr__(self, _name):
        def _decorator(*_a, **_k):
            def wrap(f):
                return f
            return wrap
        return _decorator


fake_pytest = types.ModuleType("pytest")
fake_pytest.fixture = fixture
fake_pytest.raises = raises
fake_pytest.approx = approx
fake_pytest.mark = _Mark()
sys.modules["pytest"] = fake_pytest


# --------------------------------------------------------------------------
# Builtin fixtures: monkeypatch, capsys
# --------------------------------------------------------------------------
class MonkeyPatch:
    def __init__(self):
        self._undo = []

    def setattr(self, target, name, value=None, raising=True):
        # dotted-string form: setattr("pkg.mod.attr", value)
        if isinstance(target, str):
            value = name
            module_path, _, attr = target.rpartition(".")
            obj = importlib.import_module(module_path)
            old = getattr(obj, attr)
            self._undo.append((obj, attr, old))
            setattr(obj, attr, value)
        else:
            old = getattr(target, name)
            self._undo.append((target, name, old))
            setattr(target, name, value)

    def undo(self):
        for obj, attr, old in reversed(self._undo):
            setattr(obj, attr, old)
        self._undo.clear()


class _Captured:
    def __init__(self, out, err):
        self.out = out
        self.err = err


class CapSys:
    def __init__(self):
        self._out = io.StringIO()
        self._err = io.StringIO()
        self._cm_out = redirect_stdout(self._out)
        self._cm_err = redirect_stderr(self._err)
        self._cm_out.__enter__()
        self._cm_err.__enter__()

    def readouterr(self):
        out, err = self._out.getvalue(), self._err.getvalue()
        self._out.truncate(0); self._out.seek(0)
        self._err.truncate(0); self._err.seek(0)
        return _Captured(out, err)

    def close(self):
        self._cm_out.__exit__(None, None, None)
        self._cm_err.__exit__(None, None, None)


# --------------------------------------------------------------------------
# Discovery + execution
# --------------------------------------------------------------------------
sys.path.insert(0, str(root / "src"))
tests_dir = root / "tests"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# conftest first (defines shared fixtures)
conftest = _load_module(tests_dir / "conftest.py", "conftest")
conftest_fixtures = {n: v.func for n, v in vars(conftest).items() if isinstance(v, _FixtureMarker)}


def resolve_fixture(name, module_fixtures, teardowns):
    if name == "monkeypatch":
        mp = MonkeyPatch()
        teardowns.append(mp.undo)
        return mp
    if name == "capsys":
        cs = CapSys()
        teardowns.append(cs.close)
        return cs
    func = module_fixtures.get(name) or conftest_fixtures.get(name)
    if func is None:
        raise KeyError(f"unknown fixture '{name}'")
    # resolve fixture's own params (shallow; candidate-y fixtures take none)
    kwargs = {p: resolve_fixture(p, module_fixtures, teardowns)
              for p in inspect.signature(func).parameters}
    produced = func(**kwargs)
    if inspect.isgenerator(produced):
        gen = produced
        value = next(gen)
        teardowns.append(lambda g=gen: next(g, None))
        return value
    return produced


passed, failed = 0, 0
failures = []

test_files = sorted(p for p in tests_dir.glob("test_*.py"))
for tf in test_files:
    mod = _load_module(tf, tf.stem)
    module_fixtures = {n: v.func for n, v in vars(mod).items() if isinstance(v, _FixtureMarker)}
    test_funcs = [(n, v) for n, v in vars(mod).items()
                  if n.startswith("test_") and inspect.isfunction(v)]
    for name, func in test_funcs:
        teardowns = []
        params = list(inspect.signature(func).parameters)
        try:
            kwargs = {p: resolve_fixture(p, module_fixtures, teardowns) for p in params}
            func(**kwargs)
            passed += 1
        except Exception as e:  # noqa: BLE001
            failed += 1
            failures.append((tf.name, name, f"{type(e).__name__}: {e}"))
        finally:
            for td in reversed(teardowns):
                try:
                    td()
                except Exception:  # noqa: BLE001
                    pass

print(f"Collected test files: {[p.name for p in test_files]}")
print(f"\nPASSED: {passed}")
print(f"FAILED: {failed}")
if failures:
    print("\n--- FAILURES ---")
    for fname, tname, err in failures:
        print(f"  {fname}::{tname}  ->  {err}")
sys.exit(1 if failed else 0)
