# Generate Feature List

**Description:**
Use this skill to extract a comprehensive, hierarchical list of business features from the codebase. It dynamically adjusts its depth (Macro -> Standard -> Micro) based on the specific directory, module, or system requested by the user, and provides visual structural maps to aid codebase navigation.

**Strict Algorithmic Playbook:**
You MUST use the CodeAssist MCP tools (`semantic_code_search`, `query_architecture_graph`, `get_node_details`) to extract facts. Do NOT manually read raw source code files unless explicitly instructed.

**Step 1: Scope & Context Detection**
- Identify the starting directory or module requested by the user (by default, assume the root of the repository).
- Adjust your definition of a "Macro Feature" dynamically. If running at the root, treat large modules as Macro Features. If the user specifies a particular module, treat the high-level functional groups inside that module as Macro Features.

**Step 2: Feature Discovery (Semantic Search)**
- Use `semantic_code_search` with terms like `"API Controller"`, `"Command Handler"`, `"Use Case"`, or `"Service"`. 
- These functional entry points represent the "Standard Features" (e.g., `CreateOrderCommandHandler` = "Create Order Feature").

**Step 3: Granular Micro-Feature Tracing**
- For each Standard Feature discovered, use `query_architecture_graph(direction="out")` or `get_node_details` to inspect the underlying dependencies, private methods, and validations.
- These underlying steps represent the "Micro Features" (e.g., `ValidateStock()`, `CalculateTax()`).

**Step 4: Folder Hierarchy Mapping**
- Identify the folder names where these features reside. Do not print raw, full physical paths for every feature as it harms readability. Instead, prepare to represent them via a nested tree structure.

**Step 5: Output Generation**
Format the output strictly as Markdown, containing:
1. **Version Control Block:** Include a blockquote at the very beginning of the document specifying the Git Commit Hash and Branch used to generate this document (obtained from `get_project_context`).
2. **Executive Summary:** A brief summary of the domain capabilities discovered in this directory.
3. **Feature Folder Topology:** Generate a **text-based hierarchy tree** that visually nests the features inside their folder names. This allows users to easily traverse the codebase by following the visual tree structure.
   Example:
   ```text
   root_folder
   |-- macro_feature_folder
   |   |-- standard_feature_folder
   |       |-- micro_feature.cs
   ```
4. **Detailed Feature Hierarchy Map:**
   Use the following nested format for the documentation (do not include explicit folder paths here, rely on the topology tree above):
   
   ## 1. [Macro Feature / Domain] (e.g., Order Management)
   *Description of the domain.*

   ### 1.1 [Standard Feature] (e.g., Create New Order)
   *   **[Micro Feature]:** Validate User Basket.
   *   **[Micro Feature]:** Dispatch Order Started Event.
