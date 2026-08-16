# Generate Agile Backlog

**Description:**
Use this skill to convert a vague business idea into a fully mature, CodeAssist-backed Agile Backlog. The process is broken into asynchronous Phases (Epic -> Story -> Spike -> Task). You will generate only the specific document requested for the current phase and then STOP, allowing the user to seek human approval before proceeding to the next phase.

**Strict Algorithmic Playbook:**

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

### Phase 2: User Story Generation (Definition / Hybrid)
*Triggered when the user provides an approved Epic and asks for User Stories.*

1.  **Translation:** Break down the Epic into distinct, testable User Stories.
2.  **Output Rules:**
    *   The document is **hybrid**. It translates business needs into technical expectations.
    *   Use the standard format: "As a [user], I want to [action], so that [benefit]."
    *   Define clear Acceptance Criteria for each story.
    *   Include the Version Control Block at the very top.
3.  **Stop:** Do not generate Tasks.

---

### Phase 3: Spike & Task Generation (Execution / Purely Technical)
*Triggered when the user provides approved User Stories and asks for Technical Tasks or Spikes.*

1.  **Deep Codebase Tracing:** Use `query_architecture_graph` and `semantic_code_search` to map the exact files, controllers, services, and databases that need to be created or modified to fulfill the User Stories.
2.  **Spikes (Architectural Planning):** If the architecture is ambiguous, output a "Spike" task that outlines exactly what research needs to be done.
3.  **Tasks (Purely Technical):** 
    *   Write the Task instructions in plain English, explaining the logic that needs to be added (e.g., "Add a validation check to ensure the cart total is positive before checkout.").
    *   **Readability Rule:** Do NOT inject raw physical file paths into the sentence paragraphs. 
    *   **Technical Citations:** At the end of each Task section, append a blockquote labeled `> Technical Citations:` and list the exact file paths and class names discovered in your graph search (e.g., `BasketItem.cs`, `UpdateBasketCommandHandler`).
4.  **Output Rules:**
    *   Include the Version Control Block at the very top.
    *   **CSV Export Block:** At the very end of the document, generate a markdown code block containing CSV (Comma Separated Values) data representing all the generated items (Epic, Stories, Tasks) so the user can easily copy and import it directly into Jira or Azure DevOps. Format columns as: `IssueType, Summary, Description, Parent`.
5.  **Stop.**
