# Generate API Specification

**Description:**
Use this skill to reverse-engineer a comprehensive API Specification Document (REST, gRPC, or GraphQL) directly from the codebase's Abstract Syntax Tree (AST) and Vector semantic data.

**Strict Algorithmic Playbook:**
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

**Step 5: Output Generation**
Format the output strictly as Markdown, containing:
1. **Version Control Block:** Include a blockquote at the very beginning of the document specifying the Git Commit Hash and Branch used to generate this document (obtained from `get_project_context`).
2. **API Overview:** High-level summary of the API surface (e.g., total number of endpoints, protocols used like HTTP/gRPC).
3. **Authentication/Security:** The security mechanisms discovered in Step 4.
4. **Endpoint Reference:** 
   - A detailed list of all discovered APIs. 
   - Group them by Module or Controller.
   - For each endpoint, include: `[HTTP Method] /route/path` (if REST), the Request Payload schema, and the Response format.
   - Summarize the business logic of each endpoint based on the comments retrieved in Step 2.
5. **Data Models (DTOs):** A brief reference of the core JSON/Protobuf data shapes exchanged.
