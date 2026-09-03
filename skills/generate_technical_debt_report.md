# Generate Technical Debt & Dead Code Report

**Description:**
Use this skill to scan the graph database and identify dead code, orphaned database tables, and unreferenced methods/classes across the repository.

**Strict Algorithmic Playbook:**

**Step 1: Graph Query (The Mathematical Approach)**
- Use the `query_architecture_graph` MCP tool to query the entire graph for nodes. 
- You are looking specifically for nodes of type `Class`, `Method`, `DatabaseTable`, or `StoredProcedure` that have an **in-degree of 0** (i.e., no incoming `CALLS` or `DEPENDS_ON` edges).
- *Exception:* Ignore root-level entry points such as API Controllers, `main` methods, or scheduled job runners, as these naturally have 0 incoming edges from within the codebase.

**Step 2: Semantic Verification**
- If you find a massive block of unreferenced code, use `semantic_code_search` or `get_source_code` to quickly verify if it's dynamically invoked (e.g., via Reflection, Dependency Injection magic strings, or framework routing).

**Step 3: Output Generation**
Format the output strictly as Markdown, containing:
1. **Executive Summary:** A brief summary of the technical debt health of the system.
2. **Orphaned Database Entities:** List all `DatabaseTable` or `StoredProcedure` nodes that have no application code pointing to them. This represents schemas that are safe to drop or investigate.
3. **Dead Code (Classes/Methods):** List the application classes and methods with 0 incoming references.
4. **Actionable Recommendations:** Recommend which areas should be deleted vs. which areas might just be missing test coverage.

**Anti-Hallucination Guardrails:**
- Do not list a node as dead code if it has incoming edges in the graph. 
- Do not hallucinate files or classes that are not returned by the graph tool. If the graph is fully connected and healthy, state clearly: "No dead code detected."
