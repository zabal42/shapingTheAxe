# Changelog

All notable changes to ShapingTheAxe are recorded here. Versions follow the
identity declared in `framework.yaml`. This log was reconstructed from git
history on 2026-07-21; entries before that date are grouped by the version
they produced, not by individual commit.

## [Unreleased] — repository reorganization, 2026-07-21

Working-tree changes, not committed. No entry here is a new normative
version: `SHAPING_THE_AXE_BRAIN_SPEC.md` and `ShapingTheAxe.md` remain
`0.2.0-beta.2`, unchanged in meaning. A distinct repository- or
distribution-level version identity is deliberately deferred — see
`business/DECISIONS.md`-style open questions; none is introduced yet.

### Fixed

- Resolved version drift: the core (`SHAPING_THE_AXE_BRAIN_SPEC.md`,
  `ShapingTheAxe.md`) had silently advanced to `0.2.0-beta.2` while
  `framework.yaml` and every other contract still declared `0.2.0-beta.1`.
  All normative and derived files now consistently declare `0.2.0-beta.2` —
  the true, unchanged current normative version. An earlier draft of this
  reorganization incorrectly bumped these to a fabricated `0.3.0-beta.1`
  with no corresponding rule change; that bump has been reverted.
- `README.md` described a repository tree that no longer matched reality
  (missing `adapters/`, `prompts/`, `incubator/`, `translations/`,
  `validation/`) and falsely claimed no adapter/translation directories
  existed. Rewritten to match the actual tree.
- `framework.yaml` `contracts:` was missing several existing contracts
  (`prompts/activate.md`, `adapters/`, `incubator/`,
  `evaluation/testing-strategy-incubation-protocol.md`,
  `docs/skill-candidate-decision.md`); `current_translations` declared `[]`
  despite `translations/es/START_HERE.md` existing. Both corrected.
  `framework.yaml`'s `released` date now reflects when `0.2.0-beta.2`
  actually landed (`5ea50cc`, 2026-07-19), not the reorganization date.
- `validation/case-studies/crossfit-business-copilot/EVIDENCE_MANIFEST.md`
  contained an unfilled `<hash>` placeholder, violating the framework's own
  rule against fabricated or placeholder evidence. Replaced with a real,
  reproducible SHA-256 over the consolidated evidence tree.

### Added

- `business/` — the framework's product-exploration material (vision, the
  Eldorado hypothesis, STA Assistants foundation, business models, product
  hypotheses, MVP validation protocol, decision log), consolidated from a
  previously duplicated and diverging state.
- `business/history/` — verbatim originals retired from active use but kept
  for traceability: the two independent `ELDORADO_HYPOTHESIS.md` sources
  (STA Assistants and the CrossFit laboratory), which disagree on the scope
  of evolution level 3 (`Generación avanzada` vs `Generación autónoma` —
  unresolved, flagged in the consolidated document, not decided here), and
  the original `STA_Assistants_Foundation_v0.1/README.md` prose, which an
  earlier draft of this reorganization replaced with a new index instead of
  preserving.
- `validation/case-studies/crossfit-business-copilot/` now contains the full
  laboratory evidence directly (candidate source trees, experiment docs and
  protocol, all three independent blind evaluation reports, evaluator
  adversarial evidence, meta-evaluation, and identity map), not only a
  status summary pointing outside the repository. This full inclusion is a
  deliberate choice for the development repository; a future production
  distribution will be trimmed separately.
- `CLAUDE.md` and `AGENTS.md` at the repository root: pure activation and
  routing adapters (mirroring `adapters/CLAUDE.stub.md` /
  `adapters/AGENTS.stub.md`, plus one line noting the kernel files are
  already present so the user isn't asked to attach them) so this repository
  self-activates ShapingTheAxe when opened by a capable AI environment.
  They classify no budget and add no gate.
- `CHANGELOG.md` (this file).

### Removed

- `STA/STA-Assistant/` — including a committed `.zip` archive duplicating an
  already-extracted folder next to it (verified byte-identical). Content
  migrated into `business/` and `business/history/`.
- Duplicate laboratory artifacts verified byte-identical before deletion:
  `candidate-x.tar.gz` existed with the same SHA-256 in three separate
  locations (`packages/`, `blind-evaluation/`, and a redundant
  `crossfit-evaluation-3/` run); only the authoritative `final-evidence/`
  package was kept, now reorganized as `validation/.../evidence/`.
  `crossfit-business-copilot/` as a standalone code checkout was removed —
  its tree was the pre-divergence shared baseline already contained in both
  candidates' git history; only its unique docs and experiment protocol were
  kept.
- `.venv/` (27 MB), `__MACOSX/`, `.DS_Store`, and nested `.git/` directories
  inside the candidate source trees. Each candidate's commit history and
  tags are preserved as text in its own `PROVENANCE.md`.

## `0.2.0-beta.2` — 2026-07-19

- `core: evolve adaptive context discovery model` (`5ea50cc`) — advanced
  `SHAPING_THE_AXE_BRAIN_SPEC.md` and `ShapingTheAxe.md` to `0.2.0-beta.2`.
  This version was never propagated to `framework.yaml` or other contracts;
  corrected above. It remains the current normative version.

## `0.2.0-beta.1` — 2026-07-14 to 2026-07-17

- `feat: establish ShapingTheAxe foundation` (`e0266e5`)
- `feat: add ShapingTheAxe brain beta v0.2.0-beta.1` (`df86fe9`)
- `docs: record skill candidate decisions` (`72f258e`)
- `feat: add MANUAL_INSTALACION_SHAPINGTHEAXE[.pdf]` (`44fed41`, `1744ee0`)
- `feat: add universal ShapingTheAxe activation` (`c90c786`)
- `docs: add synchronized Spanish quick start` (`fc6379a`)
- `docs: remove outdated installation manual` (`06e1073`)
- `chore: ignore macOS metadata files` (`1bad230`)
- `feat: add STA Assistants foundation documents` (`5f92056`)
- `docs(validation): add first blind evaluation case study` (`e61ae28`)

## `v0.1` — foundation

- `Initial commit` (`a305b04`)

Immutable historical predecessor. Contains `context-init v0.2`. Preserved
byte-identical; its source archive SHA-256 is recorded in `framework.yaml`
under `predecessor.source_archive_sha256`. See `COHERENCE_DIAGNOSIS.md` for
the full migration rationale from `v0.1` to the `0.2.0-beta.x` line.
