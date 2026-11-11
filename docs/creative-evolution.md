# Creative code evolution contract

The C# planner consumes parsed declarations and compares normalized token sets to identify potential shared implementations. It emits review proposals only.

Each language worker must provide a Tree-sitter adapter for its pinned grammar and ABI. A production adapter must report the exact source byte ranges, syntax kind, symbol name and normalized declaration body. Grammar versions and native library digests belong in the component manifest.

Patch generation is a separate stage. It must produce a unified diff, bind the patch to a base commit, validate syntax using the same grammar version, run static policy checks and execute tests only inside an isolated sandbox. The API process must never load or execute a generated patch.

Human approval is required before patch application. The system should preserve the proposal, AST fingerprints, test report and resulting commit SHA as the causal record for each accepted evolution.
