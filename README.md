# CodeAssist Reverse Engineering Engine (v2.3.0)

A highly scalable, stateful, and 0-hallucination engine for reverse-engineering massive codebases into actionable insights, Business Requirements, Architecture Documents, and Agile pipelines.

## 🌟 How It Works

CodeAssist solves the "massive codebase LLM context window" problem by parsing a target repository locally into a **Data Warehouse** before the LLM ever sees it. 

1. **Tree-sitter AST Extraction:** Scripts parse C#, Java, HTML, and CSS to extract structural metadata (classes, methods, relationships).
2. **Local Storage:** The structure is stored in a fast **SQLite Graph Database**, while docstrings and comments are vectorized into a **ChromaDB Vector Database**.
3. **MCP Server:** A FastMCP-powered Python server connects to your LLM (Claude Desktop, Cursor, Antigravity) and exposes surgical tools (`get_node_details`, `query_architecture_graph`, `get_source_code`).
4. **Skills / Playbooks:** We provide highly tuned Markdown instructions in the `skills/` folder that act as generic algorithms, forcing the LLM to traverse the graph and document distributed sagas and enterprise architectures without hallucinating.

## 🚀 Key Features (v2.0 - v2.3 Updates)

CodeAssist has evolved from a basic document generator into a persistent project management engine:

*   **⚡ Differential Indexing (v2.2):** Re-indexing a codebase is now lightning fast. The indexer uses OS timestamps to surgically skip unchanged files and wipe/re-insert data only for modified or deleted files. Update your knowledge base on-demand!
*   **📚 Standardized Documentation (v2.3):** All generation skills (`generate_architecture`, `generate_lld`) strictly adhere to industry-standard C4 and UML templates. The AI cannot hallucinate or skip critical sections like Non-Functional Requirements, DB Entities, or Security strategies.
*   **🎨 Semantic Visuals (v2.3):** Automatically generates stunning, color-coded Mermaid flowcharts and C4 diagrams (e.g., databases are blue, external APIs are gray, internal services are green).
*   **💬 Ask Codebase (v2.1):** Interact conversationally with your repository using the `ask_codebase` skill, powered by intelligent tool selection and strict anti-hallucination guardrails.
*   **💾 Document Lifecycle (v2.1):** All AI-generated documents are cached in a JSON registry (`.codeassist/docs/registry.json`), preventing duplicate work and maintaining strict version control (Git Hash tracking).
*   **🛠️ Agile Pipeline Engine (v2.0):** Converts vague business ideas into complete Jira/Azure DevOps ready backlogs (Epics, Stories, Tasks) via the `generate_agile_backlog` skill, complete with CSV exports.

### Architecture Note: Extractors vs. Config Registry
You may notice that CodeAssist has **AST Extractors** for languages like C# and Java, but the **Configuration Registry** (`language_registry.py`) also includes Node, Python, and Docker. This is intentional:
*   **AST Extractors** (`scripts/extractors/`) perform deep structural parsing (finding classes, methods, endpoints). This is heavy-duty analysis currently supported for C#, Java, HTML, and CSS.
*   **Configuration Registry** (`src/language_registry.py`) performs lightweight infrastructure mapping by simply reading manifest files (like `package.json`, `requirements.txt`, or `docker-compose.yml`). Even without a deep AST extractor for Python, the system can still read `requirements.txt` to tell the LLM what frameworks (e.g., Django, Celery) the repo relies on.

---

## 🚀 Setup & Usage

### 1. Installation
Clone this repository and install the dependencies.
```bash
pip install -r requirements.txt
```

### 2. Index the Target Repository
Point the indexer at any repository you want to analyze. It will walk the directory and construct the local Data Warehouse.
```bash
python scripts/indexer.py /path/to/target/repository
```
*Note: Run this again anytime code changes. The Differential Indexer will only process modified files!*

### 3. Run the MCP Server
Set the `TARGET_REPO` environment variable so the server knows where to read the `.codeassist/` databases.

**Windows (PowerShell):**
```powershell
$env:TARGET_REPO="C:\path\to\target\repository"
python src/server.py
```

**Linux/Mac:**
```bash
TARGET_REPO=/path/to/target/repository python src/server.py
```

### 4. Scoped Documentation Generation
CodeAssist natively supports generating documentation for specific modules, folders, or single microservices! For an in-depth explanation of how CodeAssist handles Graph Boundaries, Monorepos vs. Microservice Repos, and Frontend-only scoping, please read the **[`SCOPING_AND_BOUNDARIES.md`](./SCOPING_AND_BOUNDARIES.md)** guide.

---

## 🛠️ Extending CodeAssist

CodeAssist is designed to be easily extensible by other developers or AI Agents. If you want to add new capabilities, here is how the system is structured:

### 1. Adding a New Language Parser
1. Create a new Tree-sitter extraction script in `scripts/extractors/`.
2. Write rules to capture class declarations, method calls, and comments.
3. Update `scripts/indexer.py` to route the new file extension to your new extractor.

### 2. Adding a New Tool
1. Open `src/server.py`.
2. Define a new Python function and decorate it with `@mcp.tool()`.
3. The tool will instantly become available to any connected LLM client.

### 3. Creating a New Skill (Playbook)
1. Create a new Markdown file in the `skills/` directory (e.g., `generate_security_audit.md`).
2. Write a step-by-step generic algorithm instructing the AI on which MCP tools to call.
3. Ensure you add strict **Anti-Hallucination Rules** (e.g., "Do not assume X, use `get_source_code` to verify").
4. The FastMCP server dynamically reads the `skills/` directory on boot and exposes them as MCP Prompts.

### 4. Updating Infrastructure Mapping
1. Open `src/language_registry.py`.
2. Create a new class inheriting from `LanguageManifestParser` (e.g., `RubyParser` or `RustParser`).
3. Define the glob patterns for the configuration files (e.g., `Cargo.toml`).
4. Write a simple regex or JSON parser to extract the `dependencies` or `frameworks`.
5. Add your new class to the `PARSERS` list at the bottom of the file.

---
*Built for Enterprise-Grade Documentation automation.*
