---
authority: the architecture template, the sections every architecture document carries
implements: []
verified: 2026-10-23
---

# Architecture - <project>

<!-- Made from `docs/templates/architecture.md` by the steps in `docs/templates/README.md`, from the
approved PRD, whose version the frontmatter's `prd:` records. Replace each section's guidance with
the design, and where something is not settled yet, name it in section 13. Keep the headings and their
numbers. -->

## 1. Context

<!-- What the system is for, in one paragraph, and the PRD version it was built from. -->

## 2. Quality attributes

<!-- Each non-functional requirement of the PRD, how the design meets it, and the check that
proves it. -->

| NFR | How it is met | How it is verified |
|-----|---------------|--------------------|
| NFR-1 | | |

## 3. System context

<!-- The actors and the external systems, as a diagram and a sentence each. -->

```mermaid
flowchart LR
  user[User] --> system[The system]
  system --> external[External system]
```

## 4. Components

<!-- Each component's one responsibility, and the functional requirements it serves. Every FR of
the PRD is served by at least one component. -->

| Component | Responsibility | Serves |
|-----------|----------------|--------|
| | | FR-1 |

## 5. Data

<!-- The model, the stores, how data flows between them, its retention and its sensitivity. -->

## 6. Interfaces

<!-- The APIs and contracts between components and with external systems, and who owns each. -->

## 7. Technology choices

<!-- Each significant choice with the decision that records it in `sprint/decision-log.md`, and the
alternatives rejected. -->

| Choice | Decision | Alternatives rejected |
|--------|----------|-----------------------|
| | | |

## 8. Deployment and environments

<!-- The environments, the hosting, CI/CD, and the infrastructure as code that builds them. -->

## 9. Security

<!-- Identity and access, secrets by `docs/standards/secrets_management_standard_v1.0.md`, and the
protection the data's sensitivity calls for. -->

## 10. Observability and operations

<!-- Logs, metrics, traces and alerts, and what a person runs to operate the system. -->

## 11. Dependency layers

<!-- The build order, earliest first. The planning session turns each layer into epics, and no story
in a later layer starts before its dependencies in earlier ones are done. -->

```
LAYER_1 --> LAYER_2 --> LAYER_3
```

## 12. Risks and trade-offs

| Risk or trade-off | Why accepted | Mitigation |
|-------------------|--------------|------------|
| | | |

## 13. Open questions

| Question | Owner | Needed by |
|----------|-------|-----------|
| | | |

## Version log

| Version | Date | Decision | Summary | Commit |
|---------|------|----------|---------|--------|
| 1.1 | 2026-10-25 | template | the template's version 1.1 | template |
