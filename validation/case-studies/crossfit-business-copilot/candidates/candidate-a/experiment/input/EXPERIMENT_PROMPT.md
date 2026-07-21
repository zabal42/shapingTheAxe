# Business Intelligence Copilot for CrossFit

You are starting a controlled technical feasibility experiment.

## Objective

Design and build an MVP Business Intelligence Copilot for CrossFit box owners.

The system must answer business questions using a simulated dataset compatible
with the concepts documented in the AimHarder Public API.

## Operating System

Use the provided ShapingTheAxe runtime as the operating system for this task.

ShapingTheAxe is responsible for determining the preparation, context
discovery, questioning, capability selection, planning, execution,
verification and handoff justified by the project's purpose, risk,
constraints and Definition of Done.

Do not reproduce a predefined workflow from this prompt.

Allow the working process to emerge from inspection, evidence, authority,
material uncertainty and the current decision.

Ask only questions whose answers materially reduce uncertainty affecting scope,
correctness, safety, architecture, authority or validation.

## MVP Questions

The MVP must support:

1. Average class occupancy during a period.
2. Classes with the lowest occupancy.
3. Time slots with the highest cancellation rate.
4. Active users with no attendance for more than 21 days.
5. Occupancy comparison between two periods.

## Core Constraints

- Use simulated data only.
- Do not connect to the real AimHarder API.
- Do not request or store real API credentials.
- Do not perform write operations.
- Metrics must be calculated deterministically.
- The language model must not invent business figures.
- Every analytical answer must explain:
  - the metric;
  - the period;
  - the data used;
  - exclusions;
  - relevant assumptions;
  - relevant limitations.
- A future real AimHarder integration must be possible without rewriting the
  business metric calculations.
- Keep the MVP small and demonstrable.

## Required Final Outcomes

The completed candidate repository must contain sufficient evidence of:

- understanding of the AimHarder documentation;
- identified capabilities, contradictions, assumptions and limitations;
- architecture and major technical decisions;
- data model and reproducible simulated dataset;
- implementation approach;
- working MVP;
- automated verification;
- installation and execution instructions;
- acceptance-criteria evaluation;
- technical handoff;
- future AimHarder integration considerations.

ShapingTheAxe determines if, when and how these outcomes are produced.

The runtime MUST generate only the artifacts justified by the task,
the current decision, the accepted risk and the Definition of Done.
## Working Rule

Prefer explicit assumptions over silent invention.

Do not treat undocumented API behaviour as confirmed.


The project does not prescribe a workflow.

The runtime is expected to inspect the available environment, determine the
minimum sufficient context, and conduct the work accordingly.