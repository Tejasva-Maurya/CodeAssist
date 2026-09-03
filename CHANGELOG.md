# CodeAssist Changelog

All notable changes to the CodeAssist project will be documented in this file.

## [2.6.0] - Global Standardization & Tool Constraints
This release finalizes the transformation of CodeAssist into an Enterprise-Grade 0-hallucination engine by locking down LLM markdown variance and strictly enforcing MCP tool boundaries.

### Changed
- **Global Shell Ban (Tool Constraints):** Injected a `CRITICAL TOOL CONSTRAINT` into every single playbook. The AI is now explicitly forbidden from using OS-level shell commands, scripts, or `grep`/`cat` tools to bypass the Data Warehouse, forcing 100% reliance on the MCP graph/vector tools.
- **Strict BRS Template:** The `generate_brs.md` skill now forces the LLM to output a rigid Business Requirement Specification, including Markdown tables for Domain Capabilities/Metrics and mandated Sub-headers for Critical Workflows.
- **Strict API Spec Template:** The `generate_api_spec.md` skill now enforces a rigid REST/gRPC Markdown template, forcing the LLM to map routes, payloads, and DTO validations strictly inside Markdown Tables.
- **Strict Feature List Template:** The `generate_feature_list.md` skill now enforces a strict 3-tier Header mapping (H2/H3/List) to completely eliminate output variance.
- **Architecture FAQ:** Added `docs/faq/SYSTEM_ARCHITECTURE_FAQ.md` to formally document deep architectural decisions regarding Vector DB hallucinations, Comment Rot, and SQL FOO collisions.

---

## [2.5.0] - Enterprise Agile Workflow Upgrade
This release upgrades the Agile Backlog capabilities, allowing CodeAssist to act as a Senior Technical Product Manager by distinguishing between functional needs, backend system requirements, and estimating complexity.

### Changed
- **Functional vs. Technical Stories:** The `generate_agile_backlog.md` playbook now explicitly generates both Functional Stories (user-facing value) and Technical Stories (backend refactoring/migrations) based on Graph dependencies.
- **Pluggable Story Point Estimation:** Added dynamic Story Point estimation to Level 2 tickets. The AI will look for a custom `.codeassist/estimation_template.md` to use organizational rules (e.g., T-Shirt sizing), gracefully falling back to mathematical Fibonacci sequence estimation if the template is absent.
- **Time-Boxed Spikes:** Formalized Spikes as Level 2 Research tickets with strict Time-boxes and Expected Outcomes to prevent runaway research tasks.
- **CSV Export Upgrade:** The automated Jira/Azure DevOps CSV export now includes a `StoryPoints` column for seamless Sprint capacity planning.

---

## [2.4.0] - Database Integration & Technical Debt Analysis
This release integrates database schemas and stored procedures directly into the CodeAssist Data Warehouse, and introduces mathematical dead code detection.

### Added
- **SQL Hybrid Extractor:** Added `sqlglot` dependency and `SqlExtractor`. The system now parses `.sql` files using a hybrid approach: structural AST extraction for Tables, Views, and Procedures (avoiding FOO collisions via FQNs), and a robust Vector fallback that embeds raw DDL logic into ChromaDB to ensure no business logic is missed.
- **Technical Debt & Dead Code Report Skill:** Added `generate_technical_debt_report.md`. This playbook instructs the AI to mathematically identify dead code by querying the graph database for orphaned nodes (e.g., Tables or Methods with an in-degree of 0), significantly aiding in repository cleanup and migration scoping.

---

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
