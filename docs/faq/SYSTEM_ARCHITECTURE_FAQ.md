# CodeAssist System Architecture FAQ

This document captures deep architectural questions, design decisions, and potential doubts regarding how CodeAssist operates at an enterprise scale. It serves as a reference for engineers and contributors to understand the philosophy and mechanics behind the system.

---

## 1. The RAG Context Problem: How do we prevent Vector DB Hallucinations?

**Question:** 
*Vector Databases often return results that are conceptually similar to the query but structurally incorrect. For example, returning a similar-sounding method instead of the exact one needed. Since Vector DBs struggle with retrieving deterministic logic, how does CodeAssist resolve this?*

**Answer:** 
CodeAssist solves this by using a **Dual-Database (Hybrid) Architecture**. We never rely on the Vector Database as the source of truth for code structure.

1.  **The Graph DB (Source of Truth):** When the AST extractors parse the code, they draw mathematical, hard-linked edges (e.g., `OrderController` `CALLS` `PaymentService`) into a SQLite Graph Database. If the AI needs to know how a feature executes, our skills force it to use `query_architecture_graph`. This returns deterministic facts with 0-hallucination.
2.  **The Vector DB (The Compass):** The ChromaDB Vector store is used *only* for fuzzy entry-point discovery. If the AI asks "How are taxes calculated?", the Vector DB returns semantic matches from comments and docstrings. 
3.  **The Validation Loop:** The AI treats Vector DB results purely as *hints*. Once a hint is found, the AI immediately uses the Graph DB or `get_source_code` to mathematically verify the structure before documenting it.

---

## 2. Comment Rot: Handling Stale or Incorrect Comments

**Question:**
*Do comments in the codebase have the same weightage as code? In large codebases, developers often modify code but forget to update the comments, leading to contradictions. How does CodeAssist address this?*

**Answer:**
This phenomenon is known as **Comment Rot**. If an AI gives stale comments the same weight as code, it will confidently generate incorrect documentation. CodeAssist prevents this by enforcing strict rules:

1.  **Code Dictates Structure, Comments Dictate Intent:** The AST structural parser ignores comments entirely when drawing the Graph Database edges. If a stale comment says *"This method calls Stripe,"* but the AST sees that the code actually calls `PayPalGateway`, the Graph DB will mathematically prove PayPal is used. The Graph (Code) always overrules the Vector (Comment).
2.  **Anti-Hallucination Guardrails:** Our playbooks (`generate_architecture.md`, `generate_lld.md`) contain explicit instructions forbidding the LLM from blindly trusting comments for critical workflows. If a comment claims a specific architectural routing (e.g., CQRS EventBus), the AI is instructed to use `get_source_code` to read the raw implementation and verify reality.

---

## 3. SQL Parsing & The "FOO Collision"

**Question:**
*When extracting database schemas, how does the system prevent naming collisions (e.g., a database table named `Users` and a C# class named `Users`)? Furthermore, how does Differential Indexing handle modified SQL files without disconnecting backend application files?*

**Answer:**
1.  **Fully Qualified Names (FQNs):** To prevent FOO collisions, the `SqlExtractor` maps database entities using distinct labels (`DatabaseTable`, `StoredProcedure`) rather than generic `Class` or `Method` labels. The unique Node IDs are prefixed strictly (e.g., `table:dbo.users` vs. `class:Users`). This guarantees the Graph Database never confuses an application class with a database table.
2.  **Safe Differential Updates:** CodeAssist's Differential Indexing (v2.2.0) ensures that when a file is modified, the indexer *only deletes the nodes and edges that were originally created by that specific file*. If a Java file created a `CALLS` edge pointing to a SQL Stored Procedure, that edge is owned by the Java file. Re-indexing the SQL file will safely leave the Java file's outgoing connections completely intact.
