# `ft_irc` Reference Case

**Case ID:** `ft-irc-reference-001`
**Protocol:** `context-init v0.2`
**Declared evaluation mode:** Planning
**Evaluated scope:** Full cycle; transition not formally recorded
**Status:** Closed — **91.3/100, PASS**

## Purpose

This is the first controlled reference case for ShapingTheAxe. It tests whether
a clean AI instance can inspect a real, completed student project, close the
five sources of uncertainty, and produce an approved correction plan without
depending on hidden conversation memory.

`ft_irc` is useful because it combines:

- a formal specification with zero-grade failure conditions;
- an existing C++98 codebase and git history;
- personal style and explainability requirements;
- platform and submission constraints;
- a real collaborator boundary between two authors.

The case evaluates the protocol. It is not a public distribution of the student
repository or the 42 subject.

## Official result

The case closed on 2026-07-14 after independent evaluation:

| Measure | Result |
|---|---|
| Score | **91.3/100** |
| Verdict | **PASS** |
| Hard failures | **0** |
| Independent handoff | **Passed** |
| Framework/subject/snapshot/report/evidence correspondence | **Exact** |
| Reference-grade | Not reached |

The complete chronological transcript was not retained, the transition from
Planning to Full-cycle mode was not formally recorded, and the `irssi` check
remains blocked by the execution environment. These limitations prevent a
Reference-grade verdict but do not invalidate the PASS.

The executor and evaluator conversations are frozen as evidence. The audit
must not be repeated and the controlled fixture must not be modified.

Any defects found during the run belong exclusively to the frozen experimental
fixture. They are not findings about the separate, real Urduliz project.

## Success conditions

The reference run succeeds only when:

1. The evaluated instance inspects the supplied artifacts before asking
   questions.
2. Every question is necessary, evidence-based, and asked one at a time.
3. The context brief closes or explicitly controls all five sources.
4. Material contradictions and missing decisions are exposed rather than
   silently resolved.
5. The user confirms the understanding and approves an executable correction
   plan.
6. An independent evaluator assigns **Pass** using
   [`evaluation/rubric.md`](../../evaluation/rubric.md).
7. A clean executor passes the independent handoff test without the original
   discovery conversation.

## Controlled inputs

The files below are supplied privately to the evaluated instance. They are not
committed to this public framework repository.

| Input | Frozen identity | Size | Role |
|---|---|---:|---|
| `local_IRC_auditoria.tar.gz` | SHA-256 `83b132b9b5ad0cc8532f50e9338bbc99129204b32ddf6c59baee1e3c6f94fced` | 105,598 bytes | Repository snapshot including git history |
| `Irc.pdf` | SHA-256 `216877566d020d68177ca9a447e0f725b0edc1a719218ea3322f663dcdbf9c9b` | 1,362,415 bytes | Official `ft_irc` subject, version 10.0, 13 pages |
| Repository `HEAD` | Git commit `7fa8e6831b5b4274d259a97d10264d92a46cdaf1` | 34 tracked files | Exact code and history under evaluation |

The official PDF is authoritative for project requirements. Any Markdown
conversion inside the repository is a convenience copy and must be checked
against the PDF before it is treated as evidence.

## Human-provided contract

These facts are explicit inputs, not conclusions the evaluated instance must
rediscover.

### Goal and definition of done

Audit the supplied `ft_irc` repository against the official subject and prepare
an evidence-backed correction plan for final evaluation. Determine:

- whether the project builds and behaves as the mandatory subject requires;
- whether tracked submission files expose local Claude tooling or private
  AI-workflow artifacts;
- whether required AI-use disclosure remains honest and subject-compliant;
- whether the Zabal-owned code is simple, readable, explainable, and consistent
  with ZabalStyle;
- what must change before submission, without modifying files before plan
  approval.

### Collaborator contract

- **Zabal owns:** network layer, sockets, non-blocking descriptors, `poll`,
  client lifecycle, input/output buffers, partial-message reconstruction, and
  the real server loop.
- **Jessica owns:** parser, IRC commands, channels, users, and operator
  permissions.
- Existing interfaces between both areas must be inspected and preserved.
- Do not rewrite Jessica-owned code merely to make it resemble Zabal-owned
  style.

### Style and execution norms

- C++98 and all official subject constraints are mandatory.
- Zabal-owned code should favor straightforward control flow, descriptive
  functions, tabs, the Urduliz header, and logic the author can explain during
  evaluation.
- Findings must distinguish functional defects, subject violations, style
  observations, and non-blocking improvements.
- Every proposed change must name affected files, current behavior, required
  behavior, source of truth, exact change, risk, and verification.
- No implementation file may be modified before the user approves the plan.

## Exact run prompt

Give the evaluated instance the canonical `ShapingTheAxe.md`, the three
templates, the two frozen inputs, and the human-provided contract above. Then
send exactly:

> Follow `ShapingTheAxe.md` and begin `context-init` for the `ft_irc` audit.
> Treat the official PDF as the normative subject. Search all supplied
> artifacts before asking me anything. Do not modify the project during this
> run; stop after producing an approved implementation plan.

Do not provide the original project conversation, prior audit findings, or an
answer key to the evaluated instance.

## Run procedure

1. Verify both file hashes and the repository `HEAD` before the run.
2. Start with a clean AI instance that has no `ft_irc` conversation history.
3. Provide only the protocol, templates, frozen inputs, explicit contract, and
   exact run prompt defined here.
4. Preserve the complete ordered transcript, including tool evidence,
   questions, answers, confirmation, and approval.
5. Do not change frozen files during the Planning-mode run.
6. Save the confirmed output as `context-brief.md`.
7. Save the approved output as `implementation-plan.md`.
8. Give the frozen evidence and outputs to an independent evaluator.
9. Save its report as `evaluation.md`.
10. Run the handoff test with a second clean executor.

The evaluated instance should not receive the rubric during the run. The
evaluator uses the rubric after the evidence is frozen.

## Retained outputs

The full execution report, evidence package, and executor/evaluator
conversations remain frozen outside this public repository. The repository
retains the case definition and the official public result:

```text
examples/ft_irc/
├── README.md
└── evaluation.md
```

The public result does not replace or reconstruct the frozen evidence.

## Integrity and privacy

- Do not commit the private repository snapshot or official subject PDF here.
- Do not publish personal email addresses from git history in case outputs.
- Retain hashes, commit identity, artifact names, and evaluator evidence so the
  run remains reproducible without redistributing the inputs.
- If an input changes, create a new case ID instead of silently replacing this
  fixture.
