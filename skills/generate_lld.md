# Generate Low-Level Design (LLD)

**Description:**
Use this skill to reverse-engineer a highly granular Low-Level Design (LLD) document for a specific component, module, or package. This dives into class relationships, DTOs, Database Entities, and algorithmic workflows.

**Strict Algorithmic Playbook:**

**Step 1: Scope Definition & Discovery**
- Use `semantic_code_search` and `query_architecture_graph` to isolate the specific classes and files belonging to the target module. Do not scan the entire repository.

**Step 2: Class & Interface Extraction**
- Use `get_node_details` on the discovered classes to extract their methods, signatures, and exact properties.

**Step 3: Data Model Identification**
- Search for DTOs and Database Entities. You MUST extract the exact fields and validation rules present in the code.

**Step 4: Flow Tracing**
- Trace the internal method calls (e.g., Controller -> Service -> Repository) for the core functionality using `query_architecture_graph`.

**ANTI-HALLUCINATION RULES (CRITICAL):**
- Do NOT invent or guess class names, methods, or DTO properties. You must only document what you find in the graph database or source code.
- If a section's data cannot be found, you MUST state "Data unavailable in codebase". Do not fabricate default behaviors.
- Do NOT draw edges in Mermaid diagrams unless a `CALLS` or `DEPENDS_ON` relationship actually exists in the graph.

**Step 5: Output Generation (STRICT TEMPLATE)**
Format the output strictly as Markdown, copying the exact structure below. Do NOT skip sections.

```markdown
> **Version Control:** Git Commit [HASH] on Branch [BRANCH]

## 1. Introduction & Scope
*   **Target Module:** [Module Name]
*   **Responsibility:** [Single responsibility]

## 2. Structural Design (Class Level)
*(Insert UML Class Diagram - Mermaid classDiagram with semantic coloring)*

### 2.1 Core Interfaces & Implementations
| Interface | Implementing Class | Responsibility | Design Pattern Used |
| :--- | :--- | :--- | :--- |

### 2.2 Key Classes (Domain Logic)
*   **`[ClassName]`**: 
    *   *Purpose:* [Purpose]
    *   *State:* [Stateful/Stateless]

## 3. Data Models & State
### 3.1 Database Entities (e.g., JPA / ORM Models)
| Entity Class | Database Table | Primary Key | Key Relationships |
| :--- | :--- | :--- | :--- |

### 3.2 Data Transfer Objects (DTOs)
| DTO Name | Direction | Properties (Name : Type) | Validation Rules |
| :--- | :--- | :--- | :--- |

## 4. Component Interfaces (APIs & Methods)
### 4.1 Exposed Endpoints (REST / Controllers)
*   **Endpoint:** [URL]
*   **Controller Method:** [Method]
*   **Request Payload:** [DTO]
*   **Success Response:** [Response]

### 4.2 Internal Public Methods
*   **Method Signature:** [Signature]
*   **Expected Behavior:** [Behavior]

## 5. Algorithmic Flow & Business Logic
*(Insert UML Activity or Sequence Diagram - Mermaid sequenceDiagram showing internal method calls)*

### 5.1 Flow: [Flow Name]
1. [Step 1]
2. [Step 2]

## 6. Exception Handling & Validation
### 6.1 Custom Exceptions
| Exception Class | HTTP Mapping | Trigger Condition |
| :--- | :--- | :--- |

## 7. Configuration & Environment Variables
| Key | Description | Default Value / Example | Secret? |
| :--- | :--- | :--- | :--- |

## 8. Dependencies
*   **Internal:** [Internal packages]
*   **External:** [External libs from get_project_context]
```
