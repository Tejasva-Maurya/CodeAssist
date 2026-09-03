# Generate Architecture Document

**Description:**
Use this skill to reverse-engineer a highly detailed Software Architecture Document directly from the codebase's Abstract Syntax Tree (AST) and Vector semantic data.

**Strict Algorithmic Playbook:**
> **CRITICAL TOOL CONSTRAINT:** You are strictly forbidden from using shell scripts, terminal commands, or local file-reading tools (like `grep`, `cat`, or `run_command`) to extract codebase information or Git hashes. You MUST exclusively use the CodeAssist MCP tools (`query_architecture_graph`, `semantic_code_search`, `get_node_details`, `get_source_code`, `get_project_context`). If an MCP tool fails or returns empty data, you MUST report the failure directly to the user instead of attempting to bypass it with terminal commands.

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

**Step 5: Output Generation (STRICT TEMPLATE)**
Format the output strictly as Markdown, copying the exact structure of the Enterprise Architecture Template below. Do NOT skip sections. If data is unavailable, write "Data unavailable in codebase".

```markdown
> **Version Control:** Git Commit [HASH] on Branch [BRANCH]

## 1. Executive Summary & Business Context
*   **Purpose:** [Why the system exists]
*   **Business Capabilities:** [Core functions]
*   **Target Audience/Users:** [Who uses it]

## 2. System Context & Scope
*(Insert C4 Level 1 Context Diagram - Mermaid flowchart with semantic coloring)*

### 2.1 External Systems Inventory
| System Name | Direction (In/Out) | Protocol | Purpose / Business Function |
| :--- | :--- | :--- | :--- |
| [System] | [Direction] | [Protocol] | [Purpose] |

## 3. Architecture Overview & Strategy
*   **Architecture Style:** [e.g., Microservices, Modular Monolith]
*   **Technology Stack:** [Languages, Frameworks, DBs, Brokers from get_project_context]

### 3.1 Non-Functional Requirements (Architectural Characteristics)
| Attribute | Target / Strategy |
| :--- | :--- |
| Scalability | [Derived strategy] |
| Security | [Derived strategy] |

## 4. Container & Component Breakdown
*(Insert C4 Level 2 Container Diagram - Mermaid flowchart with semantic coloring)*

### 4.1 Deployable Units (Containers)
**Container Name:** [Name]
*   **Responsibility:** [Purpose]
*   **Key Internal Components:** [List internal modules]
*   **Owned Data:** [Databases it owns]

## 5. Integration & APIs
### 5.1 Synchronous APIs (REST / GraphQL / gRPC)
| API / Endpoint | Consumer | Method/Protocol | Purpose |
| :--- | :--- | :--- | :--- |

### 5.2 Asynchronous Messaging (Events / Queues)
| Topic / Queue Name | Producer | Consumer | Payload/Schema Focus |
| :--- | :--- | :--- | :--- |

## 6. Runtime Workflows & Data Flow
*(Insert UML Sequence Diagram - Mermaid sequenceDiagram showing step-by-step calls)*

### 6.1 Primary Flow: [Flow Name]
*   **Trigger:** [Action]
*   **Flow Description:** [Step by step logic]

## 7. Data & Information Architecture
*(Insert Entity Relationship Diagram (ERD) - Mermaid erDiagram)*

### 7.1 Core Domain Entities
| Entity | Description | Owner Service |
| :--- | :--- | :--- |

### 7.2 Data Integrity & Storage Strategy
*   **Databases Used:** [List databases and purpose]
*   **Caching Strategy:** [Caching approach]

## 8. Deployment & Infrastructure View
*   **Hosting Environment:** [e.g., K8s, Docker]
*   **CI/CD Pipeline:** [Deployment flow if known]

## 9. Cross-Cutting Concepts
### 9.1 Security
*   **Authentication/Authorization:** [Auth strategy]

### 9.2 Observability & Monitoring
*   **Logging/Metrics:** [Observability stack]

## 10. Architecture Decision Records (ADRs)
| ADR # | Date | Context / Problem | Decision Made | Consequences / Trade-offs |
| :--- | :--- | :--- | :--- | :--- |
```
