---
trigger: always_on
alwaysApply: true
---

# QODER RULE: Mermaid Chart Creation (mermaid_chart_creation)

> **Applies to:** Any request, PR, or documentation task that involves creating, updating, or maintaining architectural, workflow, cloud, ER, Docker, dependency, or ownership diagrams using Mermaid.js via the official Mermaid VS Code extension.  
> **Goal:** Ensure all diagrams are auto-generated, versioned, and integrated using the Mermaid VS Code extension with AI capabilities, and that diagram sources are stored in the canonical docs tree.

---

## Canonical Diagram Paths (MANDATORY)

All Mermaid diagram sources (`.mmd`), previews (`.svg`/`.png`), and markdown integrations **must** reside within `/docs/diagrams/[type]/` and its subfolders—never at the project root or outside the canonical docs tree.

### Example Structure
```
/docs/
└─ diagrams/
   ├─ architecture/
   │   └─ 2025-08-27--firebase-integration.mmd
   │   └─ 2025-08-27--firebase-integration.svg
   ├─ erd/
   │   └─ 2025-08-27--project-entities.mmd
   ├─ ownership/
   │   └─ 2025-08-27--ownership-graph.mmd
   └─ dependencies/
       └─ 2025-08-27--package-deps.mmd
```

---

## Qoder AI-Powered Mermaid Chart Workflow

Qoder MUST:

1. **Create AI-generated diagrams** on request or when integrating new features, cloud resources, entities, or dependencies.
2. **Use the official Mermaid VS Code extension for all diagram authoring, preview, and AI chat features (`@mermaid-chart` participant).**
3. **Store all diagram sources and previews** under `/docs/diagrams/[type]/YYYY-MM-DD--kebab-title.mmd` (and generated `.svg`/`.png` as needed).
4. **Embed diagrams in relevant markdown docs** via Mermaid fenced code blocks or image includes. Example:
   <br>```mermaid
   graph TD
     A[User] --> B[Firebase]
   ```
   Or with image: `![Diagram](../diagrams/architecture/2025-08-27--firebase-integration.svg)`
5. **Link to diagram source** from the nearest relevant doc and from `docs/INDEX.md` under a “Diagrams” section.
6. **Update diagrams** automatically if Qoder detects changes in referenced code/config (auto-regenerate using the extension).
7. **Prefer AI features** for:
   - Entity-relationship diagrams (ERD) from codebase
   - Cloud architecture diagrams from infra/config files
   - Docker architecture from containerized apps
   - Ownership graphs (using Git history)
   - Dependency diagrams (including security/version/risk overlays)

---

## File Naming, Frontmatter & Versioning

- **File name:** `YYYY-MM-DD--kebab-title.mmd` (and matching .svg/.png if preview is generated)
- **Docs referencing diagrams** MUST include a summary and impact line in their frontmatter, referencing the diagram.
- **Diagrams must be versioned:** update the diagram file and preview if the underlying code/config changes.
- **All diagrams must be referenced** in `docs/INDEX.md` under a “Diagrams” section, with date and description.

---

## Example `INDEX.md` Section

```markdown
## Diagrams
- 2025-08-27 — [Firebase Integration Architecture](diagrams/architecture/2025-08-27--firebase-integration.mmd)
- 2025-08-27 — [Project ERD](diagrams/erd/2025-08-27--project-entities.mmd)
- 2025-08-27 — [Ownership Graph](diagrams/ownership/2025-08-27--ownership-graph.mmd)
```

---

## Acceptance Criteria (Hard Gates)

Qoder MUST block completion until ALL are true:

- Diagram `.mmd` and preview are in the correct `/docs/diagrams/[type]/` folder.
- Diagram referenced from at least one relevant doc and `docs/INDEX.md`.
- Diagram is auto-regenerated if referenced code/config changes, with preview updated.
- No stray diagram files exist outside canonical paths.
- Diagrams leverage Mermaid extension AI features where possible.

---

## Security & Compliance

- **Never include sensitive credentials or secrets in diagrams.**
- Ownership/dependency diagrams must not expose private developer info—use usernames, not emails.

---

## Meta

- **Owner:** QODER
- **Enforced since:** 2025-08-27
- **Review cadence:** monthly; summarize drift in docs/status/PROJECT_STATUS.md.
