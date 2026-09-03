# Generate API Specification

**Description:**
Use this skill to reverse-engineer a comprehensive API Specification Document (REST, gRPC, or GraphQL) directly from the codebase's Abstract Syntax Tree (AST) and Vector semantic data.

**Strict Algorithmic Playbook:**
> **CRITICAL TOOL CONSTRAINT:** You are strictly forbidden from using shell scripts, terminal commands, or local file-reading tools (like `grep`, `cat`, or `run_command`) to extract codebase information or Git hashes. You MUST exclusively use the CodeAssist MCP tools (`query_architecture_graph`, `semantic_code_search`, `get_node_details`, `get_source_code`, `get_project_context`). If an MCP tool fails or returns empty data, you MUST report the failure directly to the user instead of attempting to bypass it with terminal commands.

You MUST use the CodeAssist MCP tools (`semantic_code_search`, `query_architecture_graph`, `get_node_details`) to extract facts. Do NOT manually read raw source code files unless explicitly instructed.

**Step 1: API Discovery (Semantic Search)**
- Use `semantic_code_search` with conceptual queries (e.g., `"API controller"`, `"HTTP endpoints"`, `"gRPC service"`, `"GraphQL query"`, `"API routing"`).
- Identify the classes and methods that expose network endpoints.

**Step 2: Contract Extraction (Via Comments/Nodes)**
- For the API endpoints found in Step 1, use `get_node_details` or rely on the `semantic_code_search` outputs to read the **comments, docstrings, and property annotations** attached to those nodes.
- Use these human-written comments to infer the HTTP Method, Route Path, Request Payload, and Response Type. 
- **IMPORTANT FALLBACK:** If an endpoint is poorly documented, you MAY read its raw source code or its method signature properties to infer the request/response shapes.

**Step 3: Data Model Tracing (Graph Traversal)**
- Take the API entry points and use `query_architecture_graph(direction="out")` to trace their `CALLS` or `DEPENDS_ON` edges specifically to identify the Data Transfer Objects (DTOs), Payloads, or Domain Models returned by the API.

**Step 4: Infrastructure & Security Mapping (Language Configuration Registry)**
- Call the `get_project_context` MCP tool to retrieve global configuration files. 
- Use the output to identify exactly what security, authentication (e.g., JWT, OAuth), and API frameworks are configured in the project's root setup.

**Step 5: Output Generation (STRICT TEMPLATE)**
Format the output strictly as Markdown, copying the exact structure below. Do NOT skip sections.

```markdown
> **Version Control:** Git Commit [HASH] on Branch [BRANCH] (Retrieved via get_project_context)

## 1. API Overview
*   **Total Endpoints Discovered:** [Count]
*   **Primary Protocols:** [HTTP, gRPC, etc.]

## 2. Authentication & Security
*   **Security Mechanisms:** [JWT, OAuth, etc. - From Step 4]

## 3. Endpoint Reference
*(Group by Controller/Module)*

### 3.1 Module: [Module Name]

| HTTP Method | Route/Path | Request Payload | Response Model | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/resource` | `None` | `ResourceDTO` | [Purpose] |

## 4. Data Models (DTOs)
| Schema Name | Field Name | Data Type | Validation / Rules |
| :--- | :--- | :--- | :--- |
| `ResourceDTO` | `id` | `UUID` | Required |
```
