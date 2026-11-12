# Contributing to 9circ

This repository currently contains a minimal README and a repository-hygiene workflow. No application language, runtime, build system, test framework, or release artifact has been declared.

## Contribution rules

1. Open or link an Issue before introducing a new application, runtime, dependency, or architecture.
2. Propose the project's purpose, supported platform, language, licensing model, and ownership boundaries in the pull request.
3. Do not copy a neighboring repository's source or build system merely to make this repository appear active.
4. Keep credentials, generated binaries, private data, and local environment files out of Git.
5. Do not claim a production build or test suite exists until an executable project and reproducible tests are committed.

## Current validation

```bash
git diff --check
test -s README.md
```

These checks verify repository hygiene only. They are not application tests.

## Commits and releases

Use Conventional Commit subjects (`feat:`, `fix:`, `docs:`, `refactor:`, `perf:`, `test:`, `build:`, `ci:`, `chore:`). Use SemVer only after a versioned product contract exists. Document the release contents and limitations before creating a tag.

## Pull request checklist

- State the proposed purpose and ownership boundary.
- Explain any new language/runtime/build dependencies.
- Add meaningful tests with the implementation.
- Update this file once a supported toolchain is adopted.
