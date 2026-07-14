# `ft_irc` Independent Evaluation Record

**Case ID:** `ft-irc-reference-001`
**Closed:** 2026-07-14
**Protocol:** `context-init v0.2`
**Verdict:** **PASS**
**Score:** **91.3/100**

## Decision

The independent evaluation found no hard failures and the independent handoff
passed. It also confirmed exact correspondence among the evaluated framework,
official subject, frozen repository snapshot, technical execution report, and
supporting evidence.

This closes the reference case. No repeat audit is required.

## Reference-grade gap

The run did not reach Reference-grade because:

1. the complete chronological transcript was not retained;
2. the change from Planning to Full-cycle mode was not formally recorded; and
3. the `irssi` check remains pending after being blocked by the environment.

The blocked `irssi` check was documented and was not a hard failure.

## Evidence status

The technical execution report, supporting evidence, and the independent
executor and evaluator conversations are frozen. This record summarizes the
final decision; it does not replace, edit, or recreate those primary sources.

The controlled inputs remain identified by the manifest in
[`README.md`](README.md). Neither the snapshot nor the official subject is
published in this repository.

## Scope boundary

The audit concerned only the frozen experimental fixture. Any defects found in
that fixture belong exclusively to the experiment and must not be attributed
to the separate, real Urduliz project.

## Framework follow-up

The result validates the first reference baseline while identifying three
process improvements for consideration: durable chronological evidence, formal
mode-transition records, and structured handling of environment-blocked
verification. They are roadmap inputs, not retroactive changes to this case.
