<!------------------------------------------------------------------------------------
   Add Rules to this file or a short description and have Kiro refine them for you:
-------------------------------------------------------------------------------------> ---

trigger: always_on
alwaysApply: true
---

rules:

- name: Vanguard – Project Obfuscation & Code Protection
    id: vanguard
    applies_to: |
      ALL code, tools, scripts, and distributions under `/tools/` and its subfolders, including all security/obfuscation submodules.
    goal: |
      Ensure every tool, script, and sensitive or distributable component is protected by project-standard obfuscation and code protection mechanisms. All obfuscation must be reproducible with the correct Vanguard tool and configuration.
    enforcement:
      owner: KNIGHTPROJEKS-0
      since: 2025-08-27
      review_cadence: monthly
      drift_reporting: /docs/status/PROJECT_STATUS.md
