# CodeAssist MCP Server Usage Guidelines

You have access to the **CodeAssist** MCP Server tools (`query_architecture_graph`, `semantic_code_search`, `get_node_details`). These tools interface with a powerful reverse-engineering Data Warehouse (Graph DB + Vector DB) containing the complete structure of the target codebase.

## When to use these tools
You should AUTOMATICALLY use these tools WITHOUT the user explicitly asking when:
1. You are asked to explore, reverse-engineer, or document an unfamiliar codebase (e.g., generating Architecture documents or Business Requirement Specs).
2. You need to understand how different components interact (e.g., "What does the Login Controller call?").
3. You need to map frontend HTML elements to backend logic.

## How to use the tools
- Start by querying the entry points or key components using `semantic_code_search`.
- Use `query_architecture_graph` on specific nodes (like `class:ControllerName` or `html:...`) to discover exact dependencies (`CALLS`, `HAS_INTERACTION`, `DEPENDS_ON`).
- Do NOT try to read the raw `.codeassist` SQLite database files yourself. Always use these MCP tools to extract the data cleanly.
- If you need detailed properties of a node (like its code signature or attributes), use `get_node_details`.
