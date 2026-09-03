# Generate Agile Backlog

**Description:**
Use this skill to convert a vague business idea into a fully mature, CodeAssist-backed Agile Backlog. The process is broken into asynchronous Phases (Epic -> Story -> Spike -> Task). You will generate only the specific document requested for the current phase and then STOP, allowing the user to seek human approval before proceeding to the next phase.

**Strict Algorithmic Playbook:**
> **CRITICAL TOOL CONSTRAINT:** You are strictly forbidden from using shell scripts, terminal commands, or local file-reading tools (like `grep`, `cat`, or `run_command`) to extract codebase information or Git hashes. You MUST exclusively use the CodeAssist MCP tools (`query_architecture_graph`, `semantic_code_search`, `get_node_details`, `get_source_code`, `get_project_context`). If an MCP tool fails or returns empty data, you MUST report the failure directly to the user instead of attempting to bypass it with terminal commands.


**Step 1: Phase Identification**
Read the user's prompt carefully to determine the requested Phase. If the user does not specify a Phase, assume Phase 1. 

**Step 2: Execution Based on Phase**
Execute ONLY the instructions for the identified Phase.

---

### Phase 1: Epic Generation (Strategic / Purely Business)
*Triggered when the user provides a vague idea or asks for an Epic.*

1.  **Context Search:** Use `semantic_code_search` and `get_project_context` to understand the general domain the idea will impact.
2.  **Output Rules:**
    *   The document must be **purely business**. Do NOT include technical information, code file paths, or architecture details.
    *   Focus on the User Journey, Strategic Goals, and Core Capabilities. Write in plain English.
    *   Include a Mermaid Flowchart illustrating the High-Level User Journey.
    *   Include the Version Control Block at the very top.
3.  **Stop:** Do not generate User Stories.

---

### Phase 2: Story Generation (Functional & Technical)
*Triggered when the user provides an approved Epic and asks for Stories.*

1.  **Translation & Discovery:** Break down the Epic into distinct, testable stories. Use `query_architecture_graph` to understand the dependencies of the requested features.
2.  **Story Types (Level 2 Tickets):** Generate BOTH types of stories as needed:
    *   **Functional Stories:** User-facing features. Must use the standard format: "As a [user], I want to [action], so that [benefit]." Include strict Acceptance Criteria.
    *   **Technical Stories:** Backend/System requirements (e.g., database migrations, security upgrades, refactoring) required to support the Functional Stories.
3.  **Story Point Estimation (Pluggable & Deterministic):** 
    *   **Custom Template:** Use `get_project_context` to check for `.codeassist/estimation_template.md`. If it exists, you MUST strictly use its scoring rubric.
    *   **Fallback (Mathematical Fibonacci):** If no custom template exists, you MUST use the following strict scoring table based on the Graph dependency depth (the number of nodes/files the feature touches):
        *   **1 Point (Trivial):** Modifies 1 isolated method or UI file. No database changes. (Graph Nodes Touched: 1-2)
        *   **2 Points (Simple):** Modifies a single class/controller. (Graph Nodes Touched: 3-4)
        *   **3 Points (Moderate):** Modifies an end-to-end slice in one service (e.g., Controller -> Service -> existing Repository). (Graph Nodes Touched: 5-7)
        *   **5 Points (Complex):** Creates new Database Tables/Entities alongside new APIs. (Graph Nodes Touched: 8-12)
        *   **8 Points (Very Complex):** Cross-boundary changes involving multiple microservices, Event Buses, or heavy legacy refactoring. (Graph Nodes Touched: 13+)
        *   **13+ Points:** The story is too large. Break it down into smaller stories. Do NOT assign 13 points to a single story.
4.  **Output Rules:**
    *   Include the Version Control Block at the very top.
    *   Clearly label Functional vs. Technical stories and their Estimated Points.
5.  **Stop:** Do not generate Tasks.

---

### Phase 3: Spike & Task Generation (Execution / Purely Technical)
*Triggered when the user provides approved Stories and asks for Technical Tasks or Spikes.*

1.  **Deep Codebase Tracing:** Use `query_architecture_graph` and `semantic_code_search` to map the exact files, controllers, services, and databases that need to be created or modified to fulfill the Stories.
2.  **Spikes (Research Tasks):** If the architecture or API integration is highly ambiguous and cannot be estimated, output a **Spike** (a Level 2 Research ticket).
    *   *Mandatory Format:* A Spike MUST include a strict **Time-box** (e.g., "Time-box: 8 Hours") and an **Expected Outcome** (e.g., "A technical plan for Stripe integration").
3.  **Tasks (Purely Technical - Level 3):** 
    *   Write the Task instructions in plain English, explaining the granular logic that needs to be coded.
    *   **Readability Rule:** Do NOT inject raw physical file paths into the sentence paragraphs. 
    *   **Technical Citations:** At the end of each Task section, append a blockquote labeled `> Technical Citations:` and list the exact file paths and class names discovered in your graph search (e.g., `BasketItem.cs`, `UpdateBasketCommandHandler`).
4.  **Output Rules:**
    *   Include the Version Control Block at the very top.
    *   **CSV Export Block:** At the very end of the document, generate a markdown code block containing CSV data representing all the generated items (Epic, Stories, Spikes, Tasks) so the user can import it directly into Jira or Azure DevOps. Format columns exactly as: `IssueType, Summary, Description, Parent, StoryPoints`.
5.  **Stop.**
