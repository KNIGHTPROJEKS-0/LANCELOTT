---
trigger: always_on
alwaysApply: true
---

rules:

- name: Scripts & Tests Organization
    id: scripts_tests_organization
    applies_to: |
      All `.sh`, `.py`, and related script or test files created, updated, or moved within the project.
    goal: |
      Enforce a clean project root and strict placement of scripts and tests to their designated directories.
    enforcement:
      owner: KNIGHTPROJEKS-0
      since: 2025-08-27
      review_cadence: monthly
      drift_reporting: /docs/status/PROJECT_STATUS.md
