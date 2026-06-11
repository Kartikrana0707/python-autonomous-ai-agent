# 🚀 Autonomous AI Coding Agent for Python

An advanced, autonomous AI software engineering agent powered by **Gemini 2.5 Flash** and built specifically for **Python** development. 

Unlike simple code assistants, this agent is engineered to be a true digital engineer. Give it a high-level goal, and it can architect, create, test, and deliver an **entire Python project all on its own** from scratch. It explores directories, inspects code structures, writes scripts, and runs local tests iteratively, self-correcting any execution errors it encounters along the way.

> 🧠 **Roadmap Note:** Multi-turn tool tracking works perfectly during an execution loop. Persistent memory to remember past conversations across completely separate terminal sessions is currently under development and coming in an upcoming update!

---

## ✨ Features

* **Python Specialization:** Specifically tuned to handle Python syntax, virtual environments, dependency management, and testing workflows.
* **Full Project Generation:** Capable of generating entirely new directories, script files, configurations, and test suites from a single prompt.
* **Autonomous Error Correction:** Runs terminal tests locally. If a script crashes, the agent reads the `stderr` output, modifies its own code edits, and re-tests until it succeeds.
* **Dynamic Toolbelt:** Equipped with native tools to scan file trees, read code blocks, write/overwrite files, and execute scripts safely.
* **Rate-Limit Safeguards:** Pre-configured loop delays to run reliably on free-tier API limits.

---

## 📂 Project Structure

```text
├── calculator_app_for_agent/   # Example target workspace
│   ├── calculators.py          # Math logic rewritten by the agent
│   ├── render.py               # JSON output formatter
│   └── tests.py                # Automated test suite
├── functions/                  # Tool declarations for the Gemini toolbelt
│   ├── get_files_info.py       # Scans directories
│   ├── get_file_content.py     # Reads source code
│   ├── write_file.py           # Creates/edits python files
│   └── run_python_file.py      # Executes scripts locally
├── main.py                     # Main Agent control loop
├── .gitignore                  # Keeps secrets (.env) and virtual environments safe
└── README.md                   # Project documentation

Detailed Setup & Getting Started

Follow these step-by-step instructions to initialize and run your AI software engineering assistant locally.

1. Prerequisites
Ensure you have Python 3.10+ installed on your system. This project uses uv for lightning-fast environment management, but standard pip works too.

2. Clone the Repository
Open your terminal, navigate to your desired folder, and pull the code from GitHub:

Bash
git clone [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git)
cd AI_Agent_for_coding_in_python
3. Create a Virtual Environment
Isolate your dependencies by spinning up a clean environment:

Bash
# Using uv (Recommended)
uv venv

# Or using standard Python
python -m venv .venv
Note: Make sure to activate your environment based on your OS (.venv\Scripts\activate on Windows or source .venv/bin/activate on macOS/Linux).

4. Provide Your Gemini API Secret
The agent requires an API key from Google AI Studio to think and call tools.

Create a file named .env in the root folder of the project.

Open it in a text editor and add your key like this:

Plaintext
GEMINI_API_KEY=your_actual_gemini_api_key_here
(Don't worry, the .gitignore file is pre-configured to keep this file hidden from GitHub!)

🚀 How to Run and Test the Agent
You trigger the agent by executing main.py and passing your coding instructions as a string argument.

Example A: Fixing an Existing App
To have the agent inspect a folder, read the python files, fix broken logic, and run tests to verify:

Bash
uv run main.py "fix my calculator app in the folder calculator_app_for_agent, read all files, make changes, and verify with tests" --verbose
Example B: Creating a Project from Scratch
Because this agent can build complete applications on its own, you can command it to start something fresh:

Bash
uv run main.py "Create a brand new folder named weather_app, write a python script that fetches weather data from a mock API, and write a test file for it" --verbose
Adding the --verbose flag allows you to watch the agent's internal thought signatures and tool calls execute in real-time in your terminal.

💡 Suggestions & Improvements
This project is actively being developed! If you have ideas for:

Smarter file-editing strategies

Alternative Python testing framework integrations

Implementing the upcoming cross-session chat memory

Please feel free to open an Issue, submit a Pull Request, or drop your suggestions. All feedback is highly appreciated!