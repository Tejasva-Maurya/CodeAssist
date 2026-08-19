# CodeAssist Changelog

All notable changes to the CodeAssist project will be documented in this file.

## [2.3.0] - Design Standardization & LLD
This release focuses on eliminating LLM document hallucination and variance by enforcing strict, industry-standard architectural templates and visually appealing diagrams.

### Added
- **Low-Level Design (LLD) Skill (`generate_lld.md`):** A granular documentation playbook designed to analyze a specific component or package. It forces the AI to map out Class Interfaces, DB Entities, DTO validation rules, and algorithmic flows. Includes strict anti-hallucination guardrails and mandatory Mermaid workflow diagrams.
- **Strict Enterprise Architecture Template:** Completely overhauled `generate_architecture.md`. It now explicitly requires the AI to populate a rigid C4-model template containing sections for Non-Functional Requirements, Security strategies, ERDs, and ADRs (Architecture Decision Records).

### Changed
- **Colorful Mermaid Diagrams:** Upgraded `DOCUMENT_LIFECYCLE.md` to enforce semantic color-coding in all AI-generated Mermaid flowcharts and diagrams using `classDef` (e.g., Databases in blue, External APIs in gray, Internal services in green).

---

## [2.2.0] - Differential Indexing & Mermaid Fix
This update addresses severe scaling bottlenecks by converting the indexer into a differential engine, while also squashing a persistent Mermaid diagram rendering bug.

### Added
- **Differential Indexing Engine:** `indexer.py` now acts as a Delta Engine using OS `last_modified` timestamps. It instantly skips unchanged files, turning massive repository updates from a multi-minute operation into a sub-second task.
- **Node Tracking & Surgical Deletions:** Upgraded `sqlite_graph.py` and `vector_db.py` to support tracking metadata. If a file is modified or deleted, the system surgically wipes its old nodes and ChromaDB embeddings before re-indexing, preventing "ghost" nodes and data duplication.
- **On-Demand Update Skill (`refresh_knowledge_base.md`):** Users can now tell the AI to "refresh the knowledge base," triggering the differential indexer automatically.

### Fixed
- **Mermaid Syntax Parsing Errors:** Added a strict instruction to `DOCUMENT_LIFECYCLE.md` forcing the AI to enclose all Mermaid node labels in double quotes. This completely resolves catastrophic Markdown parsing errors caused by commas, spaces, or parentheses in generated diagrams.

---

## [2.1.0] - Statefulness & Q&A Update
This release transforms CodeAssist from a basic document generator into a persistent, stateful project management engine with built-in caching and conversational codebase querying.

### Added
- **Master Document Lifecycle (`DOCUMENT_LIFECYCLE.md`):** A strict, universal rulebook automatically injected into all generation skills. It enforces JSON registry caching, surgical document editing, and standardized saving (`[ID]-[Project]-[Scope]-[Type].md`).
- **JSON Registry Caching:** Introduced `.codeassist/docs/registry.json`. CodeAssist now checks this registry before generating documents, preventing duplicate work and allowing instant retrieval of existing architecture/BRS files.
- **Agile Subfolders:** Agile documents (Epics, Stories, Tasks) are now intelligently organized into dedicated subfolders based on Epic ID (e.g., `.codeassist/docs/Agile/[Epic-ID]/`) to prevent directory clutter.
- **Ask Codebase Skill (`ask_codebase.md`):** A new playbook enabling users to ask plain-English or highly technical questions about the codebase. Includes dynamic MCP tool selection and strict anti-hallucination guardrails.

---

## [2.0.1] - Performance & Stability Overhaul
This patch focuses on eliminating I/O bottlenecks, resolving JSON-RPC socket corruption, and optimizing memory usage when analyzing project infrastructure.

### Fixed
- **JSON-RPC Stdio Corruption:** Replaced unbounded Git subprocess calls with `subprocess.run(capture_output=True)` to completely isolate the IDE connection from terminal output. This prevents fatal crashes when running CodeAssist on untracked repositories or directories with dubious ownership.

### Changed
- **I/O Performance Optimization:** Refactored `get_project_context` to use a single-pass `os.walk` with aggressive directory pruning. The server now completely skips ignored directories (like `node_modules` and `.git`), reducing repository scan times from minutes to milliseconds.
- **Deep Manifest Parsing (Memory Optimization):** Upgraded `language_registry.py` to natively parse `requirements.txt`, `pyproject.toml`, and `Dockerfile` configurations instead of dumping raw file contents. This significantly reduces token consumption and memory bloat within the LLM's context window.

---

## [2.0.0] - The Agile & Tracking Update
This release focuses on making CodeAssist an enterprise-ready project management and documentation tool, introducing dynamic scoping, strict version tracking, and Agile pipeline generation.

### Added
- **Document-Level Git Versioning:** All core generated documents (BRS, Architecture, API Specs) now strictly require a "Version Control Block" at the top, stamping the document with the exact Git Commit Hash and branch for traceability.
- **Hierarchical Feature List Skill (`generate_feature_list.md`):** A new playbook that extracts macro, standard, and micro features from the codebase. Supports dynamic scoping (root vs module level) and outputs a visual directory tree structure for easy repository navigation.
- **Agile Backlog Pipeline Skill (`generate_agile_backlog.md`):** A powerful new state-machine playbook that converts a vague business idea into a full agile backlog. Features asynchronous, non-blocking execution across 3 distinct phases: Epic (Business), User Story (Hybrid), and Spikes/Tasks (Technical).
- **Jira/ADO CSV Export:** The Agile Backlog skill now automatically formats all generated Epics, Stories, and Tasks into a CSV code block at the end of execution for instant bulk-import into Jira or Azure DevOps.
- **Scope & Boundaries Guide (`SCOPING_AND_BOUNDARIES.md`):** Comprehensive documentation explaining how the system behaves when isolated to a specific module, frontend vs backend, or a single microservice repository.

### Changed
- Refactored the core Language Configuration Registry in `server.py` to use a Strategy Pattern (`language_registry.py`), cleanly isolating manifest parsers and ensuring OCP compliance for future language support.

---

## [1.0.0] - Base Version
The foundational release establishing the Map-Reduce reverse engineering engine.

### Added
- **Tree-sitter AST Extractors:** Full structural parsing support for C#, Java, HTML, and CSS.
- **Local Data Warehouse:** SQLite Graph Database for relationships (Nodes/Edges) and ChromaDB Vector Database for semantic search over docstrings and comments.
- **FastMCP Python Server:** Core MCP tools enabling LLMs to safely query the local database without hallucinating (`get_node_details`, `query_architecture_graph`, `get_source_code`, `get_project_context`).
- **Core Playbooks (Skills):**
  - `generate_brs.md`: Reverse engineers a Business Requirements Specification.
  - `generate_architecture.md`: Generates Enterprise Architecture Documentation with C4 Context/Component diagrams and execution flowcharts.
  - `generate_api_spec.md`: Reverse engineers an API Specification document (REST/gRPC/GraphQL).
- **Language Registry Support:** Out-of-the-box infrastructure parsing for Java, C#, Node, Python, and Docker manifests.
