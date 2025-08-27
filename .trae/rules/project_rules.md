---
title: "TRAE RULEBOOK: Documentation, Diagrams, Scripts/Tests, Env, Vanguard"
date: "2025-08-27"
author: "LANCELOTT"
change_type: ["doc"]
modules: [
  "docs/organization",
  "docs/diagrams",
  "scripts/",
  "tests/",
  "requirements.txt",
  "tools/security/vanguard"
]
links:
  pr: ""
  issues: []
summary: "Unified TRAE rulebook enforcing canonical structure and compliance for documentation, diagrams, scripts/tests, environment requirements, and tool obfuscation. Replaces and supersedes all prior QODER rules for these domains."
impact: "Ensures all project artifacts are consistently structured, discoverable, protected, and compliant. No undocumented or unprotected code or diagrams can land in the repo."
---

# TRAE RULEBOOK: Documentation, Diagrams, Scripts & Tests, Environment, Obfuscation

> **Applies to:** All code, documentation, diagrams, scripts, tests, requirements, and tools added or modified in the project, especially as part of any TRAE workflow or tracked via TRAE.
> **Goal:** Enforce unified, strict, and automated compliance for all key project metadata, security, and maintainability domains.
> **Blocking:** ALL these rules are hard gates; no PR or task can complete unless every rule below is satisfied.

---

## 1. Documentation Management (`trdocs_management`)

- **Every code change** must create or update at least one doc in `/docs/[type]/` with full frontmatter and required section skeleton.
- **Docs tree:**

  ```
  /docs/
    ├─ api/
    ├─ build/
    ├─ completion/
    ├─ diagrams/
    ├─ guides/
    ├─ integration/
    ├─ organization/
    ├─ setup/
    ├─ status/
    ├─ summary/
    ├─ tools/
    ├─ INDEX.md
    └─ README.md
  ```

- **Naming:** `YYYY-MM-DD--kebab-title.md`
- **Frontmatter:** See below for full frontmatter structure.
- **Aggregators:**
  - `/docs/INDEX.md` must link every doc by date & section.
  - Root `README.md` must prepend a summary entry in a managed **Recent Changes** block (trimmed to 15, older to `/docs/status/PROJECT_STATUS.md`).
- **No stray docs:** All docs must be under `/docs/` with correct links and reference fixes on move.
- **Blocking:** No code lands until all above are satisfied.

---

## 2. Mermaid Chart Creation (`mermaid_chart_creation`)

- **All Mermaid diagrams** (`.mmd`), previews (`.svg`/`.png`), and markdown integrations must live under:

  ```
  /docs/diagrams/[type]/YYYY-MM-DD--kebab-title.mmd
  ```

- **Types:** `architecture/`, `erd/`, `ownership/`, `dependencies/`, etc.
- **Embed diagrams** via mermaid code blocks or image links in relevant docs.
- **Link all diagrams** in a dedicated **Diagrams** section in `/docs/INDEX.md`.
- **Auto-regenerate:** If underlying code/config changes, diagram and preview must be updated.
- **AI-powered:** Prefer Mermaid extension AI features for ERD, cloud, ownership, and dependency diagrams.
- **Blocking:** No diagram or preview outside canonical path. All diagrams referenced in at least one doc and in `/docs/INDEX.md`.

---

## 3. Scripts & Tests Organization (`scripts_tests_organization`)

- **Test Python files** (`test_*.py`, `*_test.py`, or containing test classes) must be under `/tests/`.
- **Shell and utility scripts** (`.sh`, batch, etc.) must be under `/scripts/`.
- **Root allowlist:** Only files explicitly listed may be at project root; all others must move.
- **Update references:** All code, CI, and docs must reference new paths after move.
- **Blocking:** No unapproved `.sh`/`.py`/test/script remains at root. All tests/scripts in canonical dirs. `/docs/INDEX.md` and guides updated as needed.

---

## 4. Source Environment Requirements (`source_env_requirements`)

- **Only one requirements file:** `/requirements.txt` at root. No other requirements files may exist anywhere.
- **Merge/deduplicate:** If others are found, merge to `/requirements.txt` and delete the rest.
- **Docs/scripts:** Reference only `/requirements.txt` everywhere.
- **Blocking:** No other requirements* files in the repo.

---

## 5. Vanguard – Tool Obfuscation & Code Protection (`vanguard`)

- **Every tool/script under `/tools/` (except `/tools/security/vanguard/`) must be obfuscated/protected** using an approved tool:
  - Python: `pyarmor`
  - JS: `javascript-obfuscator`
  - Java: `skidfuscator-java-obfuscator`
  - .NET: `BitMono`
  - Binaries: `Hyperion`, `utls`
- **Metadata:** Each protected tool must have a `README.md` or doc block specifying:
  - Vanguard tool used
  - Date of obfuscation
  - Config summary (no secrets)
  - Responsible agent
- **Indexing:** `/docs/tools/TOOLS_REFERENCE.md` and `/docs/INDEX.md` must list all obfuscated tools and method used.
- **Recent Changes:** `/docs/README.md` Recent Changes must log each protection event.
- **Blocking:** No unprotected code in `/tools/` can be pushed, built, or released.

---

## Frontmatter Template

```yaml
---
title: "<Human Title>"
date: "YYYY-MM-DD"
author: "LANCELOTT"
change_type: ["integration" | "feature" | "fix" | "refactor" | "doc"]
modules: ["path/to/module1", "path/to/module2"]
links:
  pr: "<PR or commit URL if available>"
  issues: ["#123", "#456"]
summary: "<1–3 lines of what changed and why>"
impact: "<user/runtime/security impact in 1–2 lines>"
---
```

---

## Diagrams Section Example (`INDEX.md`)

```markdown
## Diagrams
- 2025-08-27 — [Firebase Integration Architecture](diagrams/architecture/2025-08-27--firebase-integration.mmd)
- 2025-08-27 — [Project ERD](diagrams/erd/2025-08-27--project-entities.mmd)
- 2025-08-27 — [Ownership Graph](diagrams/ownership/2025-08-27--ownership-graph.mmd)
```

---

## Vanguard Section Example (`TOOLS_REFERENCE.md`)

```markdown
## Obfuscated Tools (Vanguard)

- Argus (pyarmor, 2025-08-27)
- Kraken (skidfuscator-java-obfuscator, 2025-08-27)
- Web-Check (javascript-obfuscator, 2025-08-27)
```

---

## Acceptance Criteria (ALL ARE BLOCKING)

- Every code or doc change is documented under `/docs/`, properly indexed, and referenced in README.md.
- All Mermaid diagrams are in `/docs/diagrams/[type]/`, referenced in at least one doc and `/docs/INDEX.md`, and up-to-date with code/config.
- No stray scripts/tests at root except explicit allowlist; all others in `/scripts/` or `/tests/`.
- Only `/requirements.txt` exists; all dependencies merged there; all docs/scripts reference it.
- All `/tools/` code is obfuscated per Vanguard, with metadata in place, and indexed.
- Security: Never commit secrets/credentials; never expose sensitive info in diagrams or tool metadata.
- All aggregators and guides are up to date.

---

## Security & Compliance

- **Never log or commit secrets, credentials, or private configs.**
- Diagram and ownership/dependency diagrams must not expose private developer details.
- All obfuscation must be reproducible with the specified Vanguard tool/config.

---

## Meta

- **Owner:** LANCELOTT
- **Enforced since:** 2025-08-27
- **Review cadence:** weekly (docs), monthly (diagrams/scripts/env/vanguard); summarize drift in `/docs/status/PROJECT_STATUS.md`.

---
