---
trigger: always_on
alwaysApply: true
---

# QODER RULE: Scripts & Tests Organization (scripts_tests_organization)

> **Applies to:** All `.sh`, `.py`, and related script or test files created, updated, or moved within the project.  
> **Goal:** Enforce a clean project root and strict placement of scripts and tests to their canonical directories, with only essential files remaining at the top level.

---

## Canonical Locations (MANDATORY)

- **All test Python files** (`test_*.py`, `*_test.py`, or files containing test classes/functions) MUST be stored under:
  ```
  /tests/
  ```
  - No test scripts should reside in the project root or elsewhere.

- **All shell scripts** (`.sh`), batch, and other utility scripts (not required for direct root-level operation) MUST be stored under:
  ```
  /scripts/
  ```
  - No utility scripts should reside in the project root or elsewhere.

---

## Allowed Files in Project Root

Only the following files are permitted at the project root.  
**Any other `.sh`, `.py`, or script/test file in the root MUST be moved to `/scripts/` or `/tests/` as appropriate.**

```
.env
.env.example
.envrc
.firebaserc
.gitattributes
.gitignore
.zshrc_lancelott
app.py
crush
crush_orchestrator.py
dataconnect.rules
dataconnect.yaml
docker-compose.yml
Dockerfile
firebase-debug.log
firebase.json
firestore.indexes.json
firestore.rules
functions.rules
lancelott.py
main.py
Makefile
project.json
pyarmor.bug.log
README.md
requirements.txt
server.py
start.py
storage.rules
validate_project.py
```
> **NOTE:** This list is explicit. Any new or renamed file not in this list must be placed in `/scripts/` or `/tests/` as appropriate, or updated in this rule before being allowed at root.

---

## Qoder Enforcement Workflow

Qoder MUST:

1. **Identify all `.sh`, `.py`, and related scripts/test files** in the project.
2. **Move each file** to `/scripts/` or `/tests/` based on content/type unless it is named in the allowed root files list above.
3. **Update any references** (import paths, CI configs, Makefiles, docs) to the new file locations.
4. **Block completion** of any PR or task if unapproved files remain at root or scripts/tests are not in their canonical directories.
5. **Update `/docs/INDEX.md` and relevant guides** if files are moved or reorganized.

---

## Auto-Fix Routine

- For any mislocated file:
  1. Move `.sh` and utility scripts to `/scripts/`.
  2. Move all tests to `/tests/`.
  3. Update all references and imports.
  4. Block until root is clean per the above allowlist.

---

## Acceptance Criteria (Hard Gates)

Qoder MUST block completion until ALL are true:

- No `.sh`, `.py`, or test/script file remains at root except those explicitly allowed above.
- All tests are in `/tests/`.
- All scripts/utilities are in `/scripts/`.
- All references in code, CI, and docs are updated.
- `/docs/INDEX.md` and onboarding guides are updated if new scripts/tests are added or moved.

---

## Security & Compliance

- Never move or expose sensitive environment files (`.env*`) or credential files.
- Do not alter file permissions unless required for execution in `/scripts/`.

---

## Meta

- **Owner:** QODER
- **Enforced since:** 2025-08-27
- **Review cadence:** monthly; summarize drift in `/docs/status/PROJECT_STATUS.md`
