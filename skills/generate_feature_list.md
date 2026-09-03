# Generate Feature List

**Description:**
Use this skill to extract a comprehensive, hierarchical list of business features from the codebase. It dynamically adjusts its depth (Macro -> Standard -> Micro) based on the specific directory, module, or system requested by the user, and provides visual structural maps to aid codebase navigation.

**Strict Algorithmic Playbook:**
> **CRITICAL TOOL CONSTRAINT:** You are strictly forbidden from using shell scripts, terminal commands, or local file-reading tools (like `grep`, `cat`, or `run_command`) to extract codebase information or Git hashes. You MUST exclusively use the CodeAssist MCP tools (`query_architecture_graph`, `semantic_code_search`, `get_node_details`, `get_source_code`, `get_project_context`). If an MCP tool fails or returns empty data, you MUST report the failure directly to the user instead of attempting to bypass it with terminal commands.

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

**Step 5: Output Generation (STRICT TEMPLATE)**
Format the output strictly as Markdown, copying the exact structure below. Do NOT skip sections.

```markdown
> **Version Control:** Git Commit [HASH] on Branch [BRANCH] (Retrieved via get_project_context)

## 1. Executive Summary
[Brief summary of the domain capabilities discovered in this directory]

## 2. Feature Folder Topology
```text
root_folder
|-- macro_feature_folder
|   |-- standard_feature_folder
|       |-- micro_feature.cs
```

## 3. Detailed Feature Hierarchy Map
*(Use exactly this H2/H3/List format)*

## 3.1 [Macro Feature / Domain] (e.g., Order Management)
*Description of the domain.*

### 3.1.1 [Standard Feature] (e.g., Create New Order)
*   **[Micro Feature]:** Validate User Basket.
*   **[Micro Feature]:** Dispatch Order Started Event.
```
