# Generate Architecture Document

**Description:**
Use this skill to reverse-engineer a highly detailed Software Architecture Document directly from the codebase's Abstract Syntax Tree (AST) and Vector semantic data.

**Strict Algorithmic Playbook:**
You MUST use the CodeAssist MCP tools (`semantic_code_search`, `query_architecture_graph`, `get_node_details`) to extract facts. Do NOT manually read raw source code files unless explicitly instructed.

**Step 1: Module & Boundary Discovery (Semantic Search)**
- Use `semantic_code_search` with conceptual queries (e.g., `"network boundary"`, `"API controller"`, `"Microservice entry"`, `"gRPC server"`, `"GraphQL resolver"`).
- Identify the bounded contexts or macro-modules of the system.

**Step 2: Component Purpose Extraction (Via Comments/Nodes)**
- For the modules found in Step 1, use `get_node_details` or rely on the `semantic_code_search` outputs to read the **comments and docstrings** associated with those nodes.
- **IMPORTANT FALLBACK:** Rely on human-written comments to infer architectural intent. If a critical architectural node is poorly documented, you MAY read its raw source code or properties to understand its functionality.

**Step 3: Network & Topology Mapping (Graph Traversal)**
- Take the entry points from Step 1 and use `query_architecture_graph(direction="out")` to recursively trace their `DEPENDS_ON` or `CALLS` edges.
- Identify cross-boundary communications (e.g., Service A calling Service B, or Frontend calling Backend API).
- **ANTI-HALLUCINATION RULE (Mermaid Diagrams):** You CANNOT draw a line or indicate interaction between two classes or microservices in your Mermaid Diagrams unless `query_architecture_graph` explicitly returns an edge between them. Furthermore, to determine if a Command Handler interacts with the EventBus, you MUST use the `get_source_code` tool to read the actual method bodies. Do not assume standard CQRS or EventBus routing without reading the implementation.
- **ANTI-HALLUCINATION RULE (Events):** If the system uses an Event-Driven Architecture, use `semantic_code_search("IntegrationEvent")` to extract the *exact string names* of events (e.g., `ProductPriceChangedIntegrationEvent`). Do not guess prefixes.

**Step 4: Infrastructure Mapping (Language Configuration Registry)**
- Call the `get_project_context` MCP tool. This tool will automatically scan the project for language-specific configuration files (e.g., `pom.xml`, `.csproj`, `AppHost/Program.cs`, `docker-compose.yml`) and return their exact contents.
- Use the output of this tool to authoritatively declare what databases, message brokers, and framework versions the repository uses. Because this tool feeds you the raw configuration files, you do not need to guess, hallucinate, or cite your sources.
- **Resiliency Patterns:** Use `semantic_code_search("transactional outbox", "event log", "resilient publishing", "circuit breaker")` to identify the mechanisms used for fault tolerance and safe message delivery (e.g., how events are safely persisted alongside business transactions).

**Step 5: Output Generation**
Format the output strictly as Markdown, containing:
1. **System Architecture Overview:** High-level summary of the bounded contexts and their responsibilities. Include a **C4 Level 1 Context Diagram (Mermaid)** showing the system and its external users/dependencies.
2. **Component Topology (Mermaid Diagram):** Generate a **C4 Level 2/3 Component Diagram (Mermaid)** visualizing the modules, microservices, and their dependencies on data stores or message brokers derived from Steps 3 and 4. Do not hallucinate connections.
3. **Core Workflow / Flowchart (Mermaid):** Generate a **Mermaid Flowchart or Sequence Diagram** depicting the most critical cross-boundary execution path discovered in Step 3.
4. **Hierarchy Structure:** Provide a text-based hierarchy tree mapping the core modules and their physical folder paths or namespaces to visualize the repository layout.
5. **Infrastructure Details:** List the data stores, caches, and message brokers discovered in Step 4.
6. **Graph Metrics:** Include EXACT metrics obtained from your queries (e.g., "The Order module contains X classes and Y methods with Z cross-module dependencies").
