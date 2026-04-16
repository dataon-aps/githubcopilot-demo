
# Setting Up Your Development Environment

## Creating a Python Virtual Environment

To get started with this project, create a Python virtual environment and install the required dependencies:

### On Windows (PowerShell):
```powershell
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.lock
```

### On macOS/Linux:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.lock
```

## Verifying the Installation

After activating the virtual environment and installing requirements, verify the setup:

```bash
# Check Python version
python --version

# List installed packages
pip list
```

## Deactivating the Virtual Environment

When you're done working on the project, deactivate the virtual environment:

```bash
deactivate
```

# SPECKIT - AI Agent for Software Specification and Implementation
╭─────────────────────────────────────────────── Agent Folder Security ────────────────────────────────────────────────╮
│                                                                                                                      │
│  Some agents may store credentials, auth tokens, or other identifying and private artifacts in the agent folder      │
│  within your project.                                                                                                │
│  Consider adding .github/ (or parts of it) to .gitignore to prevent accidental credential leakage.                   │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭───────────────────────────────────────────────────── Next Steps ─────────────────────────────────────────────────────╮
│                                                                                                                      │
│  1. Go to the project folder: cd githubcopilot-demo                                                                  │
│  2. Start using slash commands with your AI agent:                                                                   │
│     2.1 /speckit.constitution - Establish project principles                                                         │
│     2.2 /speckit.specify - Create baseline specification                                                             │
│     2.3 /speckit.plan - Create implementation plan                                                                   │
│     2.4 /speckit.tasks - Generate actionable tasks                                                                   │
│     2.5 /speckit.implement - Execute implementation                                                                  │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

╭──────────────────────────────────────────────── Enhancement Commands ────────────────────────────────────────────────╮
│                                                                                                                      │
│  Optional commands that you can use for your specs (improve quality & confidence)                                    │
│                                                                                                                      │
│  ○ /speckit.clarify (optional) - Ask structured questions to de-risk ambiguous areas before planning (run before     │
│  /speckit.plan if used)                                                                                              │
│  ○ /speckit.analyze (optional) - Cross-artifact consistency & alignment report (after /speckit.tasks, before         │
│  /speckit.implement)                                                                                                 │
│  ○ /speckit.checklist (optional) - Generate quality checklists to validate requirements completeness, clarity, and   │
│  consistency (after /speckit.plan)                                                                                   │
│                                                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
