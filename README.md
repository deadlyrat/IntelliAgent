# IntelliAgent 🤖

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&logo=langchain&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)

> **Multi-agent AI system for automated research, summarization, data extraction, and task management.**

IntelliAgent orchestrates a pipeline of AI agents that take a research topic, gather information from the web, synthesize it, extract structured data, and automatically push results to Trello and email — all from a web dashboard.

---

## 🧠 What It Does

```
User submits a topic
        │
        ▼
 [Web Research Agent] ── searches and gathers sources
        │
        ▼
 [Summarization Agent] ── condenses findings into a concise summary
        │
        ▼
 [Extraction Agent] ── structures key data as JSON
        │
        ├──► [Trello Agent] ── creates task cards in your Trello board
        │
        └──► [Email Agent] ── delivers results to your inbox
                │
                ▼
      [Dashboard] ── view and manage all investigations
```

---

## ✨ Features

- **Automated web research** — searches multiple sources and aggregates findings on any topic
- **Intelligent summarization** — condenses lengthy content into actionable overviews
- **Structured data extraction** — outputs key entities and facts as clean JSON
- **Trello integration** — automatically creates task cards from extracted data
- **Email delivery** — sends summarized results directly to your inbox
- **Result persistence** — stores all investigations in PostgreSQL for later review
- **Web dashboard** — React UI to submit topics, track investigation status, and browse results

---

## 🏗️ Architecture

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **Agent Orchestration** | LangGraph + LangChain |
| **LLM** | OpenAI GPT-4 |
| **Backend API** | Python 3.12 · FastAPI · SQLModel |
| **Database** | PostgreSQL |
| **Frontend** | React 18 · Vite · Axios |
| **Infrastructure** | Docker · Docker Compose · Nginx |

---

## ⚙️ Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- OpenAI API key
- Trello API key + token (for task creation)
- SMTP credentials (for email delivery)

---

## 🚀 Quick Start

**1. Clone the repository**
```bash
git clone https://github.com/deadlyrat/IntelliAgent.git
cd IntelliAgent
```

**2. Configure environment variables**
```bash
cp .env.example .env
# Edit .env and fill in your API keys:
# OPENAI_API_KEY=
# TRELLO_API_KEY=
# TRELLO_TOKEN=
# TRELLO_BOARD_ID=
# SMTP_HOST=
# SMTP_USER=
# SMTP_PASSWORD=
# DATABASE_URL=postgresql://...
```

**3. Start the application**
```bash
docker-compose up --build
```

The app will be available at `http://localhost:3000`.

---

## 📸 Screenshots

> _Screenshots coming soon — add them here after running the app locally._

---

## 🎓 Academic Context

This project was developed as the **capstone project** for a programming languages course at **Universidad Tecnológica de Panamá**. It demonstrates multi-agent LLM orchestration, full-stack development, external API integration, and containerized deployment.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
