---
trigger: always_on
alwaysApply: true
---

rules:
  - name: Source Environment Requirements Management
    id: source_env_requirements
    applies_to: |
      All dependency, environment, or tool installation/upgrade tasks affecting the project’s Python or system requirements.
    goal: |
      Guarantee that all package requirements are tracked in a single, authoritative requirements file or equivalent configuration, ensuring consistency and traceability across the project.
    enforcement:
      owner: KNIGHTPROJEKS-0
      since: 2025-08-27
      review_cadence: monthly
      drift_reporting: /docs/status/PROJECT_STATUS.md
