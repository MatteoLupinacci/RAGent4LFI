## 🛡️ RAGent4LFI: AI-Powered Local File Inclusion Vulnerability Agent

Dive into the future of cybersecurity with **RAGent4LFI**! This project leverages the power of Retrieval Augmented Generation (RAG) and LLM agent to automate the detection of Local File Inclusion (LFI) vulnerabilities. 🚀 By integrating with powerful scanning tools like Gobuster and Wfuzz, and fortified with OWASP knowledge, RAGent4LFI provides robust, context-aware security assessments. Deploy our lightweight Flask API on your Kali Linux environment to orchestrate sophisticated vulnerability scans, making web security smarter and more efficient. ✨

## Disclaimer ⚠️

This project is intended solely for academic, educational, and research purposes in the field of cybersecurity. It is designed for use in:
*	🧑‍🎓 Learning and training (e.g., university courses, security research, labs)
*	🎯 Controlled environments such as CTFs and legal penetration testing platforms
*	🔍 Forensic analysis or security testing only on devices you own or are explicitly authorized to test

The author assumes no responsibility for improper or unlawful use of the software. ❌ Any misuse of this tool for illegal activities, unauthorized access, or violation of privacy is strictly prohibited. Use this tool responsibly and ethically. 🔒

## Getting Started

Follow these steps to set up and run RAGent4LFI locally.

### Installation

To get started with RAGent4LFI, clone the repository and set up your environment:

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/MatteoLupinacci/RAGent4LFI.git
    cd RAGent4LFI
    ```

2.  **Create a Virtual Environment**:
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    Install all required Python packages.
    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

The RAGent4LFI project requires the following environment variables to be set for the LangChain agent and Langsmith tracing. Create a `.env` file in the project root or set these in your shell.

| Variable             | Description                                          | Example Value         |
| :------------------- | :--------------------------------------------------- | :-------------------- |
| `LANGSMITH_TRACING`  | Enables Langsmith tracing for observability.         | `true`                |
| `LANGSMITH_API_KEY`  | Your API key for Langsmith.                          | `ls__...`             |
| `OPENAI_API_KEY`     | Your OpenAI API key for accessing the GPT-4o-mini model. | `sk-...`              |

## Usage

RAGent4LFI operates in two parts: a Flask API server (preferably on a Kali Linux machine due to `gobuster` and `wfuzz` dependencies) and the LLM agent script.

1.  **Start the Flask API Server (on a Kali Linux environment):**
    Open a terminal and navigate to your project directory. Run the `api.py` script:
    ```bash
    python api.py
    ```
    This will start the API server on `http://0.0.0.0:5000`. Ensure that `gobuster` and `wfuzz` are installed and accessible in your Kali environment.

2.  **Run the RAGent4LFI Agent:**
    Open a separate terminal and navigate to your project directory. Ensure your virtual environment is activated and run the `RAGent4LFI.py` script:
    ```bash
    python RAGent4LFI.py
    ```
    The agent will prompt you for input.

3.  **Interact with the Agent:**
    You can now interact with the AI agent by providing it with a target URL to analyze for LFI vulnerabilities.
    **Example Input:**
    ```
    🤖 How can I help you today? 💡 Analyze http://testphp.vulnweb.com for LFI vulnerabilities.
    ```

## Features

*   **AI-Powered LFI Assessment**: Utilizes a sophisticated LangChain agent for intelligent and automated detection of Local File Inclusion vulnerabilities.
*   **Retrieval Augmented Generation (RAG)**: Integrates an in-memory vector store, enriched with OWASP PDF documentation, to provide the agent with relevant security context for enhanced analysis.
*   **Dynamic Web Scanning**: Seamlessly employs industry-standard tools like `gobuster` for efficient web path discovery and `wfuzz` for precise query parameter identification.
*   **Remote Command Execution**: Features a secure Flask API endpoint to execute system commands on a remote machine (typically a Kali Linux instance), enabling powerful, agent-driven penetration testing actions.

## Badges

[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.x-black?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![LangChain](https://img.shields.io/badge/LangChain-latest-green?style=for-the-badge&logo=openai&logoColor=white)](https://www.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)](https://github.com/yourusername/RAGent4LFI)

---

[![Readme was generated by Dokugen](https://img.shields.io/badge/Readme%20was%20generated%20by-Dokugen-brightgreen)](https://www.npmjs.com/package/dokugen)
