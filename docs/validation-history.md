# Validation History

This document records completed framework validations without rewriting their
frozen evidence. The canonical protocol and rubric remain independently
versioned artifacts.

## `ft-irc-reference-001`

| Field | Result |
|---|---|
| Closed | 2026-07-14 |
| Protocol | `context-init v0.2` |
| Declared mode | Planning |
| Evaluated scope | Full cycle |
| Independent score | **91.3/100** |
| Verdict | **PASS** |
| Hard failures | **0** |
| Independent handoff | **Passed** |
| Reference-grade | Not reached |

The independent evaluation confirmed exact correspondence among the framework,
official subject, repository snapshot, execution report, and retained evidence.
The case is therefore closed and does not require another audit.

Reference-grade was not reached for three recorded reasons:

1. The complete chronological transcript was not retained.
2. The transition from Planning to Full-cycle mode was not formally recorded
   when it occurred.
3. The `irssi` check remains pending because the execution environment blocked
   it.

The `irssi` limitation was explicitly documented and did not produce a hard
failure. The executor and evaluator conversations are frozen as evidence; this
repository records their outcome but does not edit, replace, or reconstruct
them.

### Scope boundary

The evaluated repository is a frozen experimental fixture created to test an
AI-assisted end-to-end workflow. Any defects found in that fixture belong
exclusively to the experiment. They are not findings about the separate, real
Urduliz project and must never be attributed to it.

### Framework consequences

The result validates `context-init v0.2` as the first evidence-backed baseline,
not as a universal or Reference-grade solution. The next protocol revision
should consider:

- a required declaration for the active evaluation mode;
- a formal record whenever the mode or approved scope changes;
- a durable chronological transcript or equivalent event log;
- a structured status for environment-blocked verification.

These are revision candidates, not retroactive changes to the evaluated run.
This post-validation documentation update changes status metadata only; it does
not change the protocol behavior or rubric scoring rules used in the case.

The public case summary is retained in
[`examples/ft_irc/evaluation.md`](../examples/ft_irc/evaluation.md).
