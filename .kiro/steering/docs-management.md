---
trigger: always_on
alwaysApply: true
---

rules:

- name: Documentation Management
    id: docs_management
    applies_to: |
      Every integration, addition, modification, feature, bugfix, refactor, or tool added to the project.
    goal: |
      All documentation must be committed within the canonical LANCELOTT documentation tree.
      The root README.md must be updated to reflect all such changes.
    enforcement:
      owner: KNIGHTPROJEKS-0
      since: 2025-08-27
      review_cadence: weekly
      drift_reporting: docs/status/PROJECT_STATUS.md<!------------------------------------------------------------------------------------
   Add Rules to this file or a short description and have Kiro refine them for you:
------------------------------------------------------------------------------------->
