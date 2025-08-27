---
trigger: always_on
alwaysApply: true
---

# QODER RULE: Documentation Management (docs_management)

> **Applies to:** every integration, addition, modification, feature, bugfix, refactor, or tool added to the project.  
> **Goal:** All docs must land in the canonical LANCELOTT docs tree, and the root `README.md` gets a fresh summary entry every time.

---

## Canonical Docs Paths (MANDATORY)

All documentation MUST reside only under `/docs/` and its subfolders.  
If a doc appears outside these paths, Qoder MUST **move** it into the appropriate subfolder and fix all affected links.

## Canonical Structure
```
/docs/
├─ api/
├─ build/
├─ completion/
│  └─ re-completion/
├─ guides/
├─ integration/
├─ organization/
│  └─ re-organization/
├─ setup/
├─ status/
├─ summary/
├─ tools/
├─ INDEX.md
├─ README.md
```Examples of enforced files:
- `docs/api/API_REFERENCE.md`
- `docs/build/BUILD_COMPLETE.md`
- `docs/completion/SCAFFOLDING_COMPLETE.md`
- `docs/completion/re-completion/GITHUB_COMPLETION.md`
- `docs/guides/CONFIGURATION_GUIDE.md`
- `docs/integration/FIREBASE_INTEGRATION_COMPLETE.md`
- `docs/integration/LANGCHAIN_INTEGRATION_SUMMARY.md`
- `docs/organization/re-organization/PROJECT_ORGANIZATION.md`
- `docs/setup/FIREBASE_SERVICE_ACCOUNT_SETUP.md`
- `docs/status/PROJECT_STATUS.md`
- `docs/summary/FINAL_INTEGRATION_SUMMARY.md`
- `docs/summary/re-summary/PROJECT_COMPLETION_SUMMARY.md`
- `docs/tools/TOOLS_REFERENCE.md`
- `docs/INDEX.md`
- `docs/README.md`

---

## When to Document (ALWAYS)

On **every** code-producing action (integration, addition, modification, refactor, bugfix):

1. **Create/Update doc(s)** in:
   - `docs/integration/` – new services, SDKs, APIs, auth, cloud, or 3rd-party wiring (e.g. Firebase, n8n, LangChain)
   - `docs/api/` – public/internal API surfaces, endpoints/contracts
   - `docs/guides/` – how-to guides, onboarding, workflows
   - `docs/tools/` – internal CLIs, scripts, generators

2. **Update these aggregators**:
   - `docs/INDEX.md` – add/refresh link to the new/updated doc
   - `README.md` (project root) – prepend a summary entry (see below)

---

## File Naming & Frontmatter (MANDATORY)

- **File name:** `YYYY-MM-DD--kebab-title.md` (update same file if it exists)
- **Frontmatter:** Every doc must start with:

```yaml
---
title: "<Human Title>"
date: "YYYY-MM-DD"
author: "QODER"
change_type: ["integration" | "feature" | "fix" | "refactor" | "doc"]
modules: ["path/to/module1", "path/to/module2"]
links:
  pr: "<PR or commit URL if available>"
  issues: ["#123", "#456"]
summary: "<1–3 lines of what changed and why>"
impact: "<user/runtime/security impact in 1–2 lines>"
---
```
- **Section skeletons:** (each doc type must use its required section headings)

### integration/
- Overview
- Architecture / Data Flow
- Setup Steps
- Configuration
- Security Notes
- Validation / Test Plan
- Rollback Plan

### api/
- Summary
- Endpoints / Contracts
- Request / Response Schemas
- Auth / Rate Limits
- Breaking Changes
- Examples

### guides/
- Goal
- Prereqs
- Step-by-step
- Troubleshooting

### tools/
- Purpose
- Install / Usage
- Inputs / Outputs
- Examples
- Limitations

---

## INDEX.md (Aggregator - MUST keep updated)

Qoder must insert/update a dated link under the correct section, in reverse-chronological order.

**Example:**
```markdown
# Documentation Index

## Integration
- 2025-08-27 — [Firebase Integration Complete](integration/FIREBASE_INTEGRATION_COMPLETE.md)
- 2025-08-27 — [LangChain Integration Summary](integration/LANGCHAIN_INTEGRATION_SUMMARY.md)
## API
- 2025-08-27 — [API Reference](api/API_REFERENCE.md)
## Guides
- 2025-08-27 — [Configuration Guide](guides/CONFIGURATION_GUIDE.md)
- 2025-08-27 — [Deployment Guide](guides/DEPLOYMENT_GUIDE.md)
## Tools
- 2025-08-27 — [Tools Reference](tools/TOOLS_REFERENCE.md)
```

---

## Root README.md — Recent Changes Block

After docs are created or updated, Qoder MUST append/update an entry in the root README.md under a managed block:

```
## Recent Changes
<!-- QODER:RECENT_CHANGES:BEGIN -->
- 2025-08-27 — **Integration:** Firebase Integration Complete → `docs/integration/FIREBASE_INTEGRATION_COMPLETE.md`  
  Impact: Validates that all Firebase services are properly integrated and tested.
- 2025-08-27 — **Integration:** LangChain Integration Summary → `docs/integration/LANGCHAIN_INTEGRATION_SUMMARY.md`  
  Impact: Details LangChain setup and workflow integration.
<!-- QODER:RECENT_CHANGES:END -->
```
- **Placement:** After the primary description section.
- **Prepend today's entries (most recent at top).**
- **Trim to 15 most recent entries** (older ones move to docs/status/PROJECT_STATUS.md).
- **Block markers must remain intact.**

---

## Auto-Fix Routine (Qoder MUST run)

If any .md appears outside the canonical docs tree:
1. Classify by content (integration/api/guides/tools).
2. Move file into correct subfolder (create if missing).
3. Rename to `YYYY-MM-DD--kebab-title.md` if needed.
4. Fix internal links in moved file and any known referrers.
5. Update docs/INDEX.md and root README.md managed block.

**POSIX Example:**
```bash
mkdir -p "docs/"{api,build,completion,guides,integration,organization,setup,status,tools}
mv "$SRC" "$DEST_DIR/$DEST_FILE"
```

---

## Acceptance Criteria (Hard Gates)

Qoder MUST block completion of any code task UNTIL ALL are true:
- At least one doc created/updated in correct subfolder.
- Doc contains valid frontmatter and required section skeleton.
- docs/INDEX.md updated with dated link(s).
- Root README.md has updated Recent Changes block with today's entries.
- No stray docs left outside canonical path.

---

## Security & Compliance Notes

- **NEVER include secrets/service-account JSON in docs.**
- Reference `docs/setup/FIREBASE_SERVICE_ACCOUNT_SETUP.md` for service account setup.
- For GitHub wiring, reference `docs/setup/GITHUB_SETUP.md`.
- For LangChain/model changes, update `docs/integration/LANGCHAIN_INTEGRATION_SUMMARY.md`.

---

## Examples

**New integration doc (skeleton):**
```markdown
---
title: "Firebase Integration Complete"
date: "2025-08-27"
author: "QODER"
change_type: ["integration"]
modules: ["firebase"]
links:
  pr: ""
  issues: []
summary: "Firebase integration finalized and validated."
impact: "All Firebase services are ready and tested."
---

## Overview
## Architecture / Data Flow
## Setup Steps
## Configuration
## Security Notes
## Validation / Test Plan
## Rollback Plan
```

**README.md recent change line:**
```
- 2025-08-27 — **Integration:** Firebase Integration Complete → `docs/integration/FIREBASE_INTEGRATION_COMPLETE.md`  
  Impact: All Firebase services ready and tested.
```

---

## Meta

- **Owner:** QODER
- **Enforced since:** 2025-08-27
- **Review cadence:** weekly; summarize drift in docs/status/PROJECT_STATUS.md.
```