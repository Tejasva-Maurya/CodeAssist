# Ask Codebase

**Description:**
Use this skill to answer user queries about the codebase. Queries can range from non-technical (e.g., "how does payment work?") to deeply technical (e.g., "what services depend on the OrderRepository?").

**Strict Algorithmic Playbook:**
> **CRITICAL TOOL CONSTRAINT:** You are strictly forbidden from using shell scripts, terminal commands, or local file-reading tools (like `grep`, `cat`, or `run_command`) to extract codebase information or Git hashes. You MUST exclusively use the CodeAssist MCP tools (`query_architecture_graph`, `semantic_code_search`, `get_node_details`, `get_source_code`, `get_project_context`). If an MCP tool fails or returns empty data, you MUST report the failure directly to the user instead of attempting to bypass it with terminal commands.


**Step 1: Intent & Persona Analysis**
*   Analyze the user's prompt to determine their intent and technical depth.
*   If the question is non-technical/business-oriented, prepare to answer with flowcharts and plain English.
*   If the question is technical, prepare to answer with code snippets, physical file paths, and architectural relationships.

**Step 2: Dynamic Tool Selection**
Do NOT guess or hallucinate. You MUST gather facts using the CodeAssist MCP tools based on the nature of the query:
*   *Conceptual Queries:* Use `semantic_code_search` to find relevant comments and docstrings.
*   *Structural Queries:* Use `query_architecture_graph` to find dependencies or callers.
*   *Implementation Details:* Use `get_node_details` or `get_source_code` to read exactly how a function or class operates.
*   *Architecture Stack:* Use `get_project_context` if the user asks about frameworks, dependencies, or versions.

**Step 3: Anti-Hallucination Guardrails (CRITICAL)**
*   If your tool searches return NO results, or if the feature/code does NOT exist in the repository, you are strictly forbidden from inventing an answer.
*   Instead, you must reply: *"I cannot find this exact feature in the codebase."*
*   You must then provide a list of structurally or semantically similar items you *did* find (if any) and ask the user for clarification. Treat this as a conversational chat.

**Step 4: Output Generation**
*   Format your response according to the persona determined in Step 1.
*   Be concise but thorough. Do not explain *how* you used the tools, just provide the final, factual answer derived from the graph database.
