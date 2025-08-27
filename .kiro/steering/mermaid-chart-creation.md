---
trigger: always_on
alwaysApply: true
---

rules:

- name: Mermaid Chart Creation
    id: mermaid_chart_creation
    applies_to: |
      Any request, PR, or documentation task that involves creating, updating, or maintaining architectural, workflow, cloud, ER, Docker, dependency, or ownership diagrams using Mermaid.js via the official Mermaid VS Code extension.
    goal: |
      All such diagrams must be created or updated using Mermaid.js and maintained in the documentation as appropriate. Ensure diagrams are included in relevant docs and coordinated via emails as needed.
    enforcement:
      owner: KNIGHTPROJEKS-0
      since: 2025-08-27
      review_cadence: monthly
      drift_reporting: docs/status/PROJECT_STATUS.md
