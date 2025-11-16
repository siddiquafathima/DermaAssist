📌 DermaAssist — AI Multi-Agent Skincare Recommendation System
A LangGraph + OpenAI-based Intelligent Dermatology Assistant
🚀 Overview

DermaAssist is a multi-agent AI system designed to collect user skin profiles, store memory, analyze patterns, and generate personalized skincare recommendations.

Built with:

LangChain / LangGraph

Python

Multi-Agent Orchestration

Memory-Based Profile Matching

Validations + Error Handling

🧠 System Architecture
User → Intake Agent → Validation → Memory Agent → Orchestrator → Recommendation Agent → Output

DermaAssist-AI:

DermaAssist-AI/
│── README.md
│── requirements.txt
│── .gitignore
│
├── dermaassist/
│   ├── agents/
│   │   ├── intake_agent.py
│   │   ├── memory_agent.py
│   │   ├── recommendation_agent.py
│   │   ├── orchestrator_agent.py
│   │
│   ├── utils/
│   │   ├── validation.py
│   │   ├── memory_storage.json
│   │
│   ├── main.py
│
├── notebooks/
│   ├── DermaAssist_Kaggle_Notebook.ipynb
