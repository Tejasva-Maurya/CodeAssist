# CodeAssist: Scope & Boundary Analysis

You have asked critical questions about how CodeAssist behaves when we restrict the scope of generation (e.g., a single folder, frontend-only, or a single microservice repository).

Because CodeAssist uses a **Graph Database** coupled with **Vector Semantic Search**, it handles scoping incredibly well. Here is an analysis of exactly how the data is stored, retrieved, and how it behaves in these scenarios.

## 1. Scoped Generation (Module, Folder, or Feature)
**Scenario:** The repository is a massive monolith, but you ask the AI to "Generate a BRS only for the `Catalog` folder."

**How it works:**
The CodeAssist Graph DB contains every file in the repository. When you scope the prompt, the AI uses `semantic_code_search("Catalog API entry points")`. It gets back the nodes *only* for that module. 
When it calls `query_architecture_graph(direction="out")`, it starts tracing downward from the `Catalog` controllers. 
*   **Accuracy:** The accuracy actually **increases**! Because the AI is only pulling graph paths relevant to `Catalog`, the context window remains extremely clean, preventing the AI from getting confused by unrelated modules.
*   **External Links:** If `Catalog` calls a shared utility or an external module, the graph database *will* return that edge. The AI will see that it connects to an outside node, and can accurately document it as a boundary dependency.

## 2. Frontend vs. Backend Isolation
**Scenario:** Generating an Architecture Document for the Frontend UI only.

**How it works:**
The AI will search for frontend framework files (e.g., Angular components or raw HTML/CSS). The Tree-sitter extractors parsed these into the database.
When tracing the frontend's outbound dependencies, the graph will eventually point to HTTP API calls hitting your Backend Controllers. 
Because your prompt restricted the scope to "Frontend only", the AI knows to treat those Backend Controllers as the absolute boundary. It will generate a diagram showing the Frontend components pointing to a generic "Backend API" black-box, without traversing deeply into the backend database layers.

## 3. Microservice Repos vs. Monorepos
**Scenario:** The CodeAssist indexer ran on a repository that only contains *one* microservice, not the whole system.

**How it works:**
In an Event-Driven Architecture, microservices communicate via RabbitMQ/Kafka. 
*   **Monorepo:** If the whole system is indexed (like eShop), when Microservice A publishes `EventX`, the AI will use semantic search to find `EventX` and discover that Microservice B subscribes to it. It can map the full cross-service Saga perfectly.
*   **Single Microservice Repo:** If the indexer only ran on Microservice A, Microservice B literally does not exist in the local SQLite/Chroma databases. 
*   **The Result:** The AI will trace Microservice A's execution and see it publish `EventX` to RabbitMQ. It will attempt to semantic search for subscribers to `EventX`, but it will get **zero results**. 
*   **Output:** The AI handles this gracefully. It will output: *"This module publishes `EventX` to the message broker. No internal subscribers were found."* It accurately treats the message broker as the edge of the known universe. It will not hallucinate fake subscribers.

## Summary
The system handles scoping dynamically. The entire repository exists as a giant web (graph) in the database. 
**You don't need to change CodeAssist's code to scope the documentation.** You simply change your prompt to the AI (e.g., `/mcp:CodeAssist:generate_architecture Please restrict this document to only cover the Payment module`). The AI uses that prompt to determine exactly where to start its graph traversal and where to stop!
