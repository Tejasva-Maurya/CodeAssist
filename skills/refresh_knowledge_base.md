# Refresh Knowledge Base

**Description:**
Use this skill when the user asks you to update, refresh, or rebuild the Data Warehouse/Knowledge Base (because they pulled new code or modified files).

**Execution Steps:**

1. **Inform the User:** Acknowledge the request and let them know you are starting the Differential Indexing Engine.
2. **Run the Indexer:** Use your `run_command` tool to execute the indexer script on the target repository.
    *   Command: `python scripts/indexer.py <TARGET_REPO>`
    *   *Note: If `TARGET_REPO` is not explicitly known, use the current working directory or ask the user.*
3. **Analyze Output:** The command output will tell you exactly how many files were unchanged, new, modified, or deleted (orphaned).
4. **Report Back:** Summarize the results for the user. Because of the Delta Engine, unchanged files are skipped, making the process extremely fast. Let the user know the knowledge base is now fully synchronized with their latest code changes.
