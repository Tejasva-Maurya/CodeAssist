# How to Connect CodeAssist to Your AI (Beginner's Guide)

The **Model Context Protocol (MCP)** is a standard that allows AI assistants (like Claude Desktop) to connect to local tools. By connecting CodeAssist to your AI, the AI will gain the ability to instantly understand massive codebases without needing you to copy-paste code!

Here is a step-by-step guide on how to configure this.

## Step 1: Index Your Target Repository
Before the AI can read your codebase, CodeAssist needs to index it.
Open your terminal (PowerShell or Command Prompt) and run the `indexer.py` script, pointing it at the folder containing the code you want to analyze:

```bash
# Example
python "D:\TEJASVA\Antigravity Projects\CodeAssist\scripts\indexer.py" "C:\path\to\your\project"
```
*You only need to do this once per project. It creates a hidden `.codeassist` database folder inside your project.*

## Step 2: Configure Claude Desktop
We need to tell Claude Desktop how to launch the CodeAssist server in the background.

1. Open the Claude Desktop app.
2. Click the **Settings** gear icon (usually in the bottom left).
3. Navigate to the **Developer** section.
4. Click **Edit Config**. This will open a file called `claude_desktop_config.json`.

Update the JSON file to include the CodeAssist server. Replace the `TARGET_REPO` path with the path to the project you indexed in Step 1.

```json
{
  "mcpServers": {
    "CodeAssist": {
      "command": "python",
      "args": [
        "D:\\TEJASVA\\Antigravity Projects\\CodeAssist\\src\\server.py"
      ],
      "env": {
        "TARGET_REPO": "C:\\path\\to\\your\\project"
      }
    }
  }
}
```

5. Save the file and **Restart Claude Desktop**.

## Step 3: Use the Skills!
Once Claude reboots, it will automatically connect to CodeAssist. You will notice a "Plug" icon indicating tools are available.

You can now drag and drop one of the Markdown templates from the `skills/` folder (like `skills/generate_brs.md` or `skills/generate_architecture.md`) directly into the Claude chatbox and say:

> *"Please execute the instructions in this file."*

Claude will automatically use the CodeAssist tools (`query_architecture_graph`, `semantic_code_search`) to pull exactly the data it needs and generate your document perfectly!
