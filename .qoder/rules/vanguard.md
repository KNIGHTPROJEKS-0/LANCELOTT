---
trigger: always_on
alwaysApply: true
---

# QODER RULE: Vanguard – Project Obfuscation & Code Protection (vanguard)

> **Applies to:** ALL code, tools, scripts, and distributions under `/tools/` and its subfolders, including all security/obfuscation submodules.  
> **Goal:** Ensure every tool, script, and sensitive or distributable component is protected using modern obfuscation and code-hardening utilities.  
> **Scope:** Applies to any push, build, release, integration, or code change affecting `/tools/` or its descendants.

---

## Canonical Obfuscation Tools Path

All official obfuscators, protectors, and code hardening utilities must reside under:

```
/tools/security/vanguard/
├─ BitMono
├─ BOAZ
├─ de4py
├─ FakeHTTP
├─ Hyperion
├─ javascript-obfuscator
├─ pyarmor
├─ skidfuscator-java-obfuscator
├─ utls
```
> **NOTE:** Only tools in this canonical `vanguard` path are authorized for obfuscation/protection.

---

## Qoder Enforcement Workflow

Qoder MUST:

1. **Ensure Every Tool/Script in `/tools/` is Obfuscated/Protected**  
   - Prior to merge, build, or release, verify that the code for every tool under `/tools/` (except `/tools/security/vanguard/` itself) is protected using one or more of the official Vanguard tools.
   - For Python: use `pyarmor` or equivalent.
   - For JavaScript: use `javascript-obfuscator` or equivalent.
   - For Java: use `skidfuscator-java-obfuscator` or equivalent.
   - For .NET: use `BitMono` or equivalent.
   - For binaries: use `Hyperion`, `utls`, or equivalent.

2. **NEVER allow un-obfuscated code** for any tool in `/tools/` to be pushed, built, or released.
   - If unprotected: Qoder MUST block completion and auto-trigger obfuscation with the correct Vanguard tool.
   - If obfuscation fails: Block the task and require manual intervention.

3. **Track Obfuscation Metadata:**  
   - Each obfuscated tool must include a `README.md` or doc block specifying:
     - Which Vanguard tool was used
     - Date of obfuscation
     - Obfuscation configuration (summary, not keys/secrets)
     - Responsible agent (QODER, or manual override)

4. **Update Documentation:**  
   - Update `/docs/tools/TOOLS_REFERENCE.md` and `/docs/INDEX.md` to indicate which tools are protected, and by which obfuscator.
   - Document any new/updated protection in `/docs/README.md` Recent Changes.

---

## Example: Vanguard Section in TOOLS_REFERENCE.md

```markdown
## Obfuscated Tools (Vanguard)

- Argus (pyarmor, 2025-08-27)
- Kraken (skidfuscator-java-obfuscator, 2025-08-27)
- Web-Check (javascript-obfuscator, 2025-08-27)
```

---

## Acceptance Criteria (Hard Gates)

Qoder MUST block completion until ALL are true:

- All code in `/tools/` (except `/tools/security/vanguard/`) is obfuscated/protected using an approved Vanguard tool.
- Each protected tool has a metadata block or `README.md` specifying obfuscator and date.
- `/docs/tools/TOOLS_REFERENCE.md` and `/docs/INDEX.md` list all obfuscated tools and their Vanguard method.
- `/docs/README.md` Recent Changes documents the protection event.
- No unprotected code or bypass of the Vanguard directory structure is present.

---

## Security & Compliance

- **Never** log, commit, or expose obfuscation keys, passwords, or private configs.
- All obfuscation must be reproducible with the correct Vanguard tool and configuration.

---

## Meta

- **Owner:** QODER
- **Enforced since:** 2025-08-27
- **Review cadence:** monthly; summarize drift in `/docs/status/PROJECT_STATUS.md`
