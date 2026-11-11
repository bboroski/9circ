# Semantic Autonomy: Naming and Migration Contract

**Status:** proposal for review  
**Revision:** 1  
**Applies to:** 9circ  
**Branch:** feat/semantic-autonomy-2026-11-11

## Purpose

This contract defines a controlled policy for clear native-language names in this project. It seeks semantic independence in user-facing language while preserving interoperability, discoverability, and compatibility.

This is a specification, not a claim that code has already been translated or renamed. No production identifier changes merely by adding this document.

## 1. Principles

1. **Meaning before purity:** prefer precise native-language terms, but never replace accurate technical vocabulary with ambiguous inventions.
2. **Endogenous naming:** coin new product concepts from native roots or concise descriptive phrases; record definitions, scope, and examples.
3. **One concept, one canonical name:** the glossary is authoritative; synonyms remain search aliases only.
4. **Context-aware names:** operations are actions, resources are things, statuses are states.
5. **Interoperability:** preserve standards-defined fields, wire tokens, file formats, CLI flags, environment variables, third-party symbols, and externally consumed API fields unless all consumers follow an explicit migration plan.
6. **Truthful status:** distinguish proposed, accepted, experimental, deprecated, and supported terms. A plan is not an implementation.

## 2. Naming layers

| Layer | Policy |
|---|---|
| User interface | Prefer native-language labels; retain conventional terms in help where useful |
| Documentation | Define the preferred term and mention the conventional term for searchability |
| Internal identifiers | Preserve existing names; new identifiers follow repository conventions |
| Public APIs and data | Preserve published names and schemas; aliases require a versioned compatibility plan |
| Standards and dependencies | Preserve canonical spelling, capitalization, and wire representation |

## 3. Initial glossary

Candidate labels, not unconditional replacements:

| Conventional term | Preferred label | Boundary |
|---|---|---|
| interface | сопряжение; поверхность взаимодействия | Boundary for exchange between components |
| bug | ошибка; сбой | Defect vs observed failure |
| feature | возможность; функция | Capability vs callable behavior |
| deploy | ввод в действие; развёртывание | Releasing a verified build into an environment |
| commit | фиксация изменения | Version-control record; do not rename Git command |
| repository | хранилище исходных материалов | Versioned project files and history |
| token | ключ; маркер | Credential vs parser/protocol unit |
| cloud | удалённая среда; распределённая среда | Choose based on actual topology |
| stream | поток | Ordered data or event sequence |
| link | связь; ссылка | Relation vs navigable reference |
| client | потребитель; запрашивающая сторона | Only when role is accurate |
| endpoint | конечная точка; адрес операции | Network address vs operation |
| runtime | среда исполнения | Execution environment |
| build | сборка | Artifact or production process |
| test | проверка; испытание | Automated assertion vs broad validation |

## 4. Term review record

Each proposal records: stable concept ID; current term and source location; preferred label; definition and non-meanings; affected layers; alternatives and rejection reasons; compatibility impact; evidence from code/tests/schemas/consumers; decision state; owner and review date.

Inspect call sites, schemas, tests, and consumers. Do not infer meaning from spelling alone.

## 5. Migration sequence

A. **Inventory:** scan source, documentation, UI resources, examples, schemas, generated files, and API descriptions. Classify occurrences by meaning and layer. Exclude vendored/generated files from direct edits.

B. **Semantic review:** group by concept, not string match. Resolve homonyms and false positives. Identify public names.

C. **Parallel naming:** introduce accepted labels in documentation and user-facing surfaces; show conventional terms parenthetically during transition where useful.

D. **Compatible adoption:** use language-aware refactoring for internal identifiers. For public surfaces, use versioned aliases, adapters, or deprecation notices. Never silently change serialized keys or command syntax.

E. **Removal review:** remove aliases only after usage evidence, a published migration window, compatibility tests, and explicit maintainer approval. Keep historical release notes searchable.

## 6. Safety gates

- Meaning remains unchanged and the label is unambiguous.
- Unicode normalization, case, locale, and transliteration are defined.
- Imports, reflection, serialization, plugin discovery, configuration, scripts, and generated references are checked.
- Public API and data compatibility are tested.
- Docs, links, examples, CLI help, accessibility labels, and localization are updated.
- A rollback path exists.
- Credentials, protocol keywords, vendor identifiers, and third-party license text are never rewritten.
- Review every diff; blind global substitutions are forbidden.

A failed gate blocks migration.

## 7. Validation

This first stage is documentation-only. Before executable renames, add relevant glossary validation, inventory allowlists, renamed-symbol and call-site tests, API compatibility tests, UI/localization/accessibility checks, and the full supported build/lint/test suite.

Report only tests actually run. If no test harness exists, say so and define manual review.

## 8. Governance

- Review glossary changes like source code.
- Reject awkward, misleading, or conflicting terms.
- Native-language naming must not conceal conventional terms from contributors or partners.
- Keep existing code-identifier conventions until a separate tested policy is approved.
- Repository-specific vocabulary is owned locally; shared concepts use consistent ecosystem-wide definitions.
- This policy does not alter licensing, authorship, provenance, copyright, or trademark rights.

## 9. Acceptance criteria

- [ ] Maintainers approve glossary and naming layers.
- [ ] Terms are mapped to real source locations.
- [ ] Public interfaces and external dependencies are identified.
- [ ] Each executable migration has tests and rollback.
- [ ] No breaking rename is merged without a versioned decision.

**Current implementation state:** specification only. No source-code, API, schema, command, or UI names have been changed.
