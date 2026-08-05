# 🚀 Nexus AI

An Autonomous AI Research Assistant built using **LangChain**, **Ollama**, and **Tavily Search**.

The goal of this project is to build a production-style AI Research Assistant step by step while learning modern Generative AI technologies.

---

# ✨ Current Features

- Research query validation
- Tavily web search integration
- Context formatting
- LangChain LCEL pipeline
- Ollama LLM integration
- Structured research report generation
- Automatic Markdown report saving
- Unit testing with Pytest
- Professional project structure

---

# 🏗️ Current Architecture

```
                User
                  │
                  ▼
             main.py
                  │
                  ▼
        Research Pipeline
                  │
                  ▼
         Query Validator
                  │
                  ▼
        Tavily Web Search
                  │
                  ▼
        Search Formatter
                  │
                  ▼
         Research Prompt
                  │
                  ▼
           Ollama (LLM)
                  │
                  ▼
        Structured Report
                  │
                  ▼
       Markdown Report File
```

---

# 📁 Project Structure

```
nexus-ai/

│

├── app/

│   ├── chains/

│   ├── config/

│   ├── planner/

│   ├── prompts/

│   ├── services/

│   ├── tools/

│   └── utils/

│

├── reports/

├── tests/

│

├── main.py

├── requirements.txt

├── pytest.ini

└── README.md
```

---

# ⚙️ Tech Stack

- Python
- LangChain
- Ollama
- Tavily Search API
- Pytest

---

# ▶️ Installation

Clone the repository

```bash
git clone <repository-url>
```

Go inside project

```bash
cd nexus-ai
```

Create virtual environment

```bash
python -m venv myenv
```

Activate environment

Mac/Linux

```bash
source myenv/bin/activate
```

Install packages

```bash
pip install -r requirements.txt
```

Run

```bash
python main.py
```

---

# 📌 Current Project Status

✅ Phase 1 Completed

Current capabilities:

- Research Generation
- Web Search
- Report Generation
- Markdown Export
- Error Handling
- Unit Testing

---

# 🚧 Upcoming Features

- Autonomous Research Planner
- Parallel Web Search
- Reflection Agent
- LangGraph Workflow
- FastAPI Integration
- Streamlit Dashboard
- MCP Integration
- Docker Deployment
- AWS Deployment

---

# 👨‍💻 Author

Arjun Singh Pundir

Computer Science Engineering (AI & ML)

Building production-ready Generative AI projects.