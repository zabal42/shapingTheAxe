# ShapingTheAxe

> Shape the context before cutting the code.

ShapingTheAxe is a public, tool-agnostic engineering framework for human-AI
collaboration. It turns an AI from an eager implementation assistant into a
project architect that searches for evidence, reduces uncertainty, validates
its understanding, and only then plans and executes.

This repository is not a collection of magic prompts. It is a repeatable and
auditable working method.

## Status

- **Framework milestone:** ShapingTheAxe `v0.1` has completed its first
  independent reference validation and remains in development.
- **Core protocol:** `context-init v0.2` is the validated baseline.
- **Evidence:** the first independent reference case passed with **91.3/100**,
  no hard failures, and a successful handoff.
- **Canonical language:** English.

The framework and the protocol are versioned independently. A framework
release can package a specific protocol version together with templates,
evaluations, examples, and future tool adapters.

## The problem

AI-assisted development often starts too late in the process: the AI is asked
to implement before it understands the goal, the existing system, the rules,
or another collaborator's work. The resulting code may look plausible while
solving the wrong problem or violating hidden constraints.

ShapingTheAxe moves the expensive thinking to the beginning. Its central claim
is simple:

> Implementation should begin only when the remaining uncertainty is too small
> to change the chosen solution materially.

## The five sources of uncertainty

Every project is examined through the same five lenses:

1. Goal and definition of done.
2. Current state.
3. Style and execution norms.
4. External constraints.
5. Collaborator contract.

The lenses stay fixed. The number of questions does not. A well-documented
project may require none; an ambiguous project may require several.

## Quick start

1. Give your AI access to [ShapingTheAxe.md](ShapingTheAxe.md).
2. Make the relevant project artifacts available: repository, specification,
   documentation, issues, policies, and collaborator work.
3. Instruct it: `Follow ShapingTheAxe.md and begin context-init.`
4. Let it inspect the artifacts before answering questions.
5. Confirm its understanding and approve its plan before implementation.

The protocol is designed to work with any sufficiently capable AI coding
environment. It does not depend on Claude, Codex, a particular model, MCP, or a
specific agent runtime.

## Core workflow

1. **Load context:** search every available artifact first.
2. **Discover:** ask only the minimum unanswered questions, one at a time.
3. **Validate understanding:** summarize and obtain explicit confirmation.
4. **Analyze gaps:** expose contradictions, risks, and hidden assumptions.
5. **Plan:** produce a complete, verifiable implementation strategy.
6. **Execute:** implement only after approval; return to discovery whenever new
   uncertainty appears.
7. **Review and complete:** prove the result against requirements and evidence.

## Repository structure

```text
.
├── README.md
├── ShapingTheAxe.md
├── docs/
│   ├── architecture.md
│   ├── roadmap.md
│   └── validation-history.md
├── evaluation/
│   └── rubric.md
├── examples/
│   └── ft_irc/
│       ├── README.md
│       └── evaluation.md
└── templates/
    ├── completion-report.md
    ├── context-brief.md
    └── implementation-plan.md
```

The repository includes one completed reference case as evidence. Tool-specific
skills, agents, MCP integrations, translations, and the book remain
deliberately outside the current foundation.

## Design principles

- Search first. Ask second. Assume never.
- Prefer evidence over confidence.
- Ask the minimum number of high-value questions.
- Make unknowns and contradictions visible.
- Treat human confirmation and approval as hard gates.
- Keep decisions traceable to an artifact or an explicit human answer.
- Re-enter discovery when reality invalidates the plan.
- Claim completion only with verification evidence.

## Evidence so far

`context-init v0.2` passed its first independent reference validation with
**91.3/100**, no hard failures, and a successful handoff. This is the first
evidence-backed baseline, not the destination: transfer tests across unfamiliar
projects and richer product domains come next. The full result and its recorded
limitations live in the [validation history](docs/validation-history.md).

See [the architecture](docs/architecture.md) for the system boundaries and
[the roadmap](docs/roadmap.md) for the validation sequence. Use the
[conformance rubric](evaluation/rubric.md) to evaluate an actual protocol run
and the [reference case record](examples/ft_irc/README.md) to inspect the first
controlled validation.
