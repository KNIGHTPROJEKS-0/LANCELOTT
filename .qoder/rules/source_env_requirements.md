---
trigger: always_on
alwaysApply: true
---

# QODER RULE: Source Environment Requirements Management (source_env_requirements)

> **Applies to:** All dependency, environment, or tool installation/upgrade tasks affecting the project’s Python or system requirements.  
> **Goal:** Guarantee that all package requirements are tracked in a single, authoritative file and avoid fragmentation or duplication of environment specs.

---

## Canonical Path (MANDATORY)

- The **only** permitted requirements file is:
  ```
  requirements.txt
  ```
  located at the **project root** (e.g., `/requirements.txt`).

- Any other requirements files (such as `requirements-core.txt`, `requirements-dev.txt`, `requirements.in`, `requirements-prod.txt`, etc) MUST NOT be created, updated, or referenced by Qoder.

---

## Qoder Enforcement

Qoder MUST:

1. **Add, update, or remove dependencies** exclusively in the root `requirements.txt`.
2. **NEVER** create or modify any alternative requirements files, even if prompted by a user or detected in the repo.
3. **Merge all necessary requirements** (for frameworks, production, dev, and tools) into the single `requirements.txt`.
4. **Refactor**: If any requirements file exists elsewhere, Qoder must:
    - Move its content to the main `requirements.txt` (deduplicate as needed)
    - Remove the redundant/fragmented file from the repo
    - Update any scripts or docs to reference only `requirements.txt`
    - Block task completion until this is enforced

---

## Example Structure

```
/requirements.txt   # <-- Only this file is allowed and must be complete
```

**Forbidden:**
- `/requirements-core.txt`
- `/requirements-dev.txt`
- `/requirements.in`
- `/env/requirements.txt`
- `/tools/requirements.txt`
- `/docs/requirements.txt`
- Any other requirements or pip-related files outside `/requirements.txt`

---

## Indexing & Documentation

- `requirements.txt` must be referenced in any onboarding or installation guides (see `/docs/guides/CONFIGURATION_GUIDE.md`).
- Any mention of requirements files elsewhere in docs must refer only to `/requirements.txt`.

---

## Acceptance Criteria (Hard Gates)

Qoder MUST block completion until ALL are true:

- Only one requirements file exists: `/requirements.txt`
- No other requirements* files are present anywhere in the repo
- All dependencies are tracked and updated in `/requirements.txt`
- All scripts/docs reference only `/requirements.txt`
- If any other requirements files are found, Qoder must merge/delete/refactor as above before completing the task

---

## Security & Compliance

- **Never** include secrets or credentials in `requirements.txt`
- Always keep the file under version control

---

## Meta

- **Owner:** QODER
- **Enforced since:** 2025-08-27
- **Review cadence:** monthly; summarize drift in `/docs/status/PROJECT_STATUS.md`
