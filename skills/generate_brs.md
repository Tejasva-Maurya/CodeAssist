# Generate Business Requirement Specification (BRS)

**Description:**
Use this skill to reverse-engineer an Enterprise-Level Business Requirement Specification (BRS) document dynamically, regardless of the underlying language or framework.

**Strict Algorithmic Playbook:**
You MUST use the CodeAssist MCP tools (`semantic_code_search`, `query_architecture_graph`, `get_node_details`) to extract facts. Do NOT manually read raw source code files unless explicitly instructed by this algorithm.

**Step 1: Domain & Entry Point Discovery (Conceptual Semantic Search)**
- Use `semantic_code_search` with generic conceptual queries (e.g., `"core business logic"`, `"API entry points"`, `"routing"`, `"domain entities"`, or `"main execution path"`).
- Identify the top-level classes or components (e.g., Controllers, Resolvers, or Aggregates).

**Step 2: Business Logic Extraction (Via Comments/Nodes)**
- For the key nodes identified in Step 1, use `get_node_details` to read the **comments and docstrings** attached to those nodes.
- **ANTI-HALLUCINATION RULE (DDD & State Machines):** If you identify an Aggregate Root or Domain Entity (like `Order`), AST metadata is insufficient. You MUST extract the `file_path` from `get_node_details` and use the `get_source_code` tool to read the actual method bodies and internal fields. DO NOT guess the entity's lifecycle or state machine based solely on method names (e.g., guessing `Draft` from `NewDraft()`). Read the actual code to determine valid database states.
- **ANTI-HALLUCINATION RULE (Events):** If the system uses an Event-Driven Architecture, use `semantic_code_search("IntegrationEvent")` to extract the *exact string names* of events (e.g., `ProductPriceChangedIntegrationEvent`). Do not guess prefixes.

**Step 3: Dependency Graph Traversal (Follow the execution)**
- Take the entry point nodes from Step 1 and use `query_architecture_graph(direction="out")` to recursively trace their `CALLS` and `DEPENDS_ON` edges.
- Document exactly how the data flows from the entry points down to the data access or event publishing layers.
- **ANTI-HALLUCINATION RULE (Sequence Diagrams & Actors):** Do not assume a simplified flow. If the codebase separates Command Handling, Domain Event Handling, and Integration Event Publishing into distinct classes, your sequence diagram must reflect these as distinct actors based ONLY on the actual edges found in `query_architecture_graph` or `get_source_code`.
- **Pipeline Behaviors / Middleware:** When tracing event publishing, check if events are dispatched synchronously or via background middleware/pipelines (e.g., search for 'pipeline behavior', 'middleware', or 'outbox worker'). If a background publisher exists, represent it as a separate actor in your sequence diagram and **explicitly name the exact class or component** (e.g., `TransactionBehavior` or `EventDispatcher`) in the document text to explain how it executes the Transactional Outbox pattern.
- **Distributed Sagas (Event Chains):** When mapping Sequence Diagrams for distributed processes across microservices, you MUST trace the full chain of events. Use `semantic_code_search` to find all subscribers to an event, and then check if those subscribers publish new events. Document the complete multi-service saga (e.g., Service A -> Event X -> Service B -> Event Y -> Service C).
- **Hidden Business Rules:** When you discover Domain Event Handlers, use `get_source_code` to read their implementation. Look for hidden business rules (e.g., dynamically creating a user profile or 'Buyer' aggregate if one does not exist) and document them.
- **External Notifications:** Use `semantic_code_search("webhook subscriptions", "external integrations")` to identify if any modules act purely as external notifiers for state changes.

**Step 4: Infrastructure Mapping (Language Configuration Registry)**
- Call the `get_project_context` MCP tool. This tool will automatically scan the project for language-specific configuration files (e.g., `pom.xml`, `.csproj`, `AppHost/Program.cs`, `docker-compose.yml`) and return their exact contents.
- Use the output of this tool to authoritatively declare what databases, message brokers, and framework versions the repository uses. Because this tool feeds you the raw configuration files, you do not need to guess, hallucinate, or cite your sources.

**Step 5: Output Generation**
Format the output strictly as Markdown, containing:
1. **Executive Summary:** High-level summary of what the system does based on your semantic searches.
2. **Business Domain:** Core capabilities derived from the domain entities.
3. **Microservices / Module Breakdown:** Include EXACT metrics (e.g., "Module X contains Y classes and Z methods") and list the key classes based on the Graph DB.
4. **Data Flows:** Detail the execution paths you traced in Step 3. Include Mermaid diagrams to visualize `CALLS` flows.
5. **Data Architecture:** The infrastructure you discovered in Step 4.
