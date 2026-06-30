# 🤖 SQL Buddy AI

<p align="center">

# Enterprise AI-Powered Text-to-SQL Assistant

### Natural Language → AI → Validated SQL → Enterprise Database

Built using **FastAPI • Python • PostgreSQL • ChromaDB • Groq Llama 3.3 • RAG**

</p>

---

## 📌 Overview

SQL Buddy AI is an **enterprise-grade AI-powered Text-to-SQL assistant** that enables business users to retrieve information from enterprise databases using natural language.

Instead of writing SQL manually, users can ask questions like:

> Show active employees

> Display deferred benefit participants

> Count terminated employees

The application automatically:

- Understands the user's intent
- Retrieves business metadata using Retrieval-Augmented Generation (RAG)
- Generates SQL using a Large Language Model (LLM)
- Validates generated SQL
- Detects AI hallucinations
- Executes only validated SQL
- Returns results instantly
- Logs every interaction for governance and auditing

Unlike conventional Text-to-SQL applications, SQL Buddy AI focuses heavily on **AI governance, validation, explainability, and enterprise readiness**.

---

# 🎯 Business Problem

Organizations possess vast amounts of enterprise data, but accessing it often requires SQL expertise.

Business users typically rely on technical teams for ad hoc reports, creating delays and reducing productivity.

Common challenges include:

- Dependency on SQL developers
- Slow report generation
- Manual SQL errors
- Inconsistent business logic
- Lack of AI governance
- Difficulty discovering enterprise metadata

---

# 💡 Solution

SQL Buddy AI bridges the gap between business users and enterprise databases through an AI-assisted query generation workflow.

```
Business User
      │
Natural Language Question
      │
      ▼
SQL Buddy AI
      │
      ▼
Validated SQL
      │
      ▼
Enterprise Database
      │
      ▼
Results
```

The solution combines **Generative AI**, **Retrieval-Augmented Generation (RAG)**, **schema validation**, and **hallucination detection** to provide reliable and governed SQL generation.

---

# ✨ Key Features

## 🤖 AI Capabilities

- Natural Language to SQL
- Retrieval-Augmented Generation (RAG)
- Groq Llama 3.3 Integration
- Business Metadata Search
- SQL Review

---

## 🛡 AI Governance

- Schema Validation
- Hallucination Detection
- SQL Validation
- Execution Monitoring
- Audit Logging

---

## 📊 Analytics

- AI KPI Dashboard
- SQL Validity Rate
- Execution Success Rate
- Hallucination Rate
- LLM Response Time
- Query History
- Audit Trail

---

## ⚡ Enterprise Features

- PostgreSQL Integration
- Modular Architecture
- FAST APIs
- Responsive Dashboard
- Secure Query Execution
- Extensible AI Pipeline

---

# 🚀 Demo

### Live Application

> **URL:** *https://sql-buddy-ai.onrender.com*

> **Note:** The application is hosted on the Render free tier. The first request may take approximately **30–60 seconds** while the application wakes up.

---

# 📸 Screenshots

Suggested sections:

- Dashboard
- AI KPI Dashboard
- Query Results
- Audit Logs
- SQL Review
- Metadata Search


---

# 🏗 Enterprise Architecture

SQL Buddy AI follows a modular, enterprise-ready architecture that separates AI generation, metadata retrieval, validation, governance, and database execution into independent components.

```text
                         +---------------------------+
                         |      Business User        |
                         +-------------+-------------+
                                       |
                                       |
                          Natural Language Query
                                       |
                                       ▼
                   +------------------------------------+
                   |      FastAPI Web Application       |
                   |------------------------------------|
                   |  • Prompt Processing               |
                   |  • SQL Generation                  |
                   |  • SQL Review                      |
                   |  • Schema Validation               |
                   |  • Hallucination Detection         |
                   |  • Audit Logging                   |
                   +----------------+-------------------+
                                    |
                 +------------------+-------------------+
                 |                                      |
                 ▼                                      ▼
      +----------------------+              +----------------------+
      |      ChromaDB        |              |    Groq Llama 3.3    |
      |----------------------|              |----------------------|
      | Business Metadata    |<-----------> | Natural Language AI  |
      | Table Metadata       |              | SQL Generation       |
      | Column Metadata      |              +----------------------+
      +----------------------+
                                    |
                                    ▼
                    +-------------------------------+
                    |      SQL Validation Layer     |
                    |-------------------------------|
                    | Schema Validator              |
                    | Hallucination Detector        |
                    | SQL Review                    |
                    +---------------+---------------+
                                    |
                                    ▼
                     +------------------------------+
                     | PostgreSQL Enterprise DB     |
                     +---------------+--------------+
                                     |
                                     ▼
                              Query Results
                                     |
                                     ▼
                           Dashboard & Audit Logs
```

---

# 🧠 AI Pipeline

SQL Buddy AI performs multiple validation steps before executing any SQL against the database.

```text
User Question
      │
      ▼
Retrieve Business Metadata
      │
      ▼
Retrieval-Augmented Generation (RAG)
      │
      ▼
Groq LLM (Llama 3.3)
      │
      ▼
Generate SQL
      │
      ▼
SQL Review
      │
      ▼
Schema Validation
      │
      ▼
Hallucination Detection
      │
      ▼
Execute SQL
      │
      ▼
Display Results
      │
      ▼
Store Audit Logs & KPIs
```

---

# 🔍 Retrieval-Augmented Generation (RAG)

Rather than relying solely on the LLM's internal knowledge, SQL Buddy AI retrieves enterprise-specific metadata before SQL generation.

Metadata stored in ChromaDB includes:

- Business definitions
- Table descriptions
- Column descriptions
- Data dictionary
- Business terminology
- Entity relationships

This significantly improves SQL accuracy while reducing hallucinations.

---

# 🛡 AI Governance

A major objective of SQL Buddy AI is to make AI-generated SQL safe for enterprise environments.

The following governance mechanisms are implemented:

### ✅ Schema Validation

Validates every generated table and column against the actual PostgreSQL schema.

---

### 🚫 Hallucination Detection

Detects:

- Non-existent tables
- Invalid columns
- Unsupported database objects

Execution is blocked when hallucinations are detected.

---

### 🔎 SQL Review

Every generated SQL statement undergoes automated review before execution.

---

### 📝 Audit Logging

Every request stores:

- User Question
- Generated SQL
- Execution Time
- Row Count
- SQL Validity
- Execution Status
- Hallucination Status
- Timestamp

---

### 📈 AI Performance Dashboard

The application continuously tracks AI quality using enterprise KPIs.

Current KPIs include:

- SQL Validity Rate
- Execution Success Rate
- Hallucination Rate
- Average LLM Response Time
- Query Volume
- Query History

---

# 💻 Technology Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python 3.x |
| Backend Framework | FastAPI |
| Frontend | HTML5, CSS3 |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| Vector Database | ChromaDB |
| AI Model | Groq Llama 3.3 70B Versatile |
| AI Framework | Retrieval-Augmented Generation (RAG) |
| Validation | Custom Schema Validator |
| Governance | Hallucination Detection Engine |
| Deployment | Render |
| Version Control | Git & GitHub |

---

# 📁 Project Structure

```text
SQL_Buddy_AI
│
├── app
│   ├── database
│   │   ├── models.py
│   │   ├── db.py
│   │   ├── schema_cache.py
│   │   ├── schema_validator.py
│   │
│   ├── llm
│   │   ├── generate_sql.py
│   │   ├── review_sql.py
│   │   ├── hallucination_detector.py
│   │
│   ├── static
│   │
│   ├── templates
│   │
│   └── main.py
│
├── chroma_db
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

## Prerequisites

Before running the application, ensure you have:

- Python 3.11+
- PostgreSQL
- Git
- Virtual Environment
- Groq API Key

---

## Clone Repository

```bash
git clone https://github.com/BharatArora2006/SQL_Buddy_AI.git

cd SQL_Buddy_AI
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a **.env** file

```text
DATABASE_URL=postgresql://username:password@localhost/database

GROQ_API_KEY=xxxxxxxxxxxxxxxx

CHROMA_DB_PATH=./chroma_db
```

---

## Start Application

```bash
uvicorn app.main:app --reload
```

Application URL

```
http://localhost:8000
```

---

# ☁ Deployment

Current deployment uses

- Render
- PostgreSQL
- ChromaDB
- Groq API

Future deployment options

- Azure App Service
- Azure OpenAI
- AWS ECS
- Docker
- Kubernetes

---

# 📸 Screenshots

## Home Dashboard

*<img width="1361" height="599" alt="image" src="https://github.com/user-attachments/assets/7008b94e-9624-4dda-8550-1d8494b73045" />
*

---

## AI KPI Dashboard

*<img width="1433" height="768" alt="image" src="https://github.com/user-attachments/assets/74162a2b-90bd-46e8-acc6-0a9be9397c54" />
*

---

## SQL Results

*<img width="1372" height="462" alt="image" src="https://github.com/user-attachments/assets/542fa0a7-b60d-4454-a199-1d046604f39c" />
*

---

# 🧪 Example Queries

### Active Employees

```
Show active employees
```

---

### Deferred Benefit Participants

```
Show all active deferred benefit participants.
```

---

### Employee Count

```
How many terminated employees do we have?
```

---

### Payroll

```
Show payroll details for active employees.
```

---

### Custom SQL Generation

```
Show employees hired after 2022 with active benefits.
```

---

# 📊 AI Performance Metrics

The application continuously evaluates AI quality using enterprise KPIs.

Current KPIs include

| KPI | Description |
|------|-------------|
| SQL Validity Rate | Percentage of syntactically valid SQL generated |
| Execution Success Rate | Successful SQL execution percentage |
| Hallucination Rate | Invalid table/column detection rate |
| LLM Response Time | Average response time of AI model |
| Query History | Historical execution log |
| Audit Trail | Governance and monitoring |

---

# 🚀 Enterprise Capabilities

Unlike traditional Text-to-SQL demos, SQL Buddy AI includes enterprise-grade controls.

✅ Retrieval-Augmented Generation (RAG)

✅ Schema Validation

✅ Hallucination Detection

✅ SQL Review

✅ AI Governance

✅ Audit Logging

✅ Performance Monitoring

✅ Production-ready Architecture

---

# 🎯 Business Benefits

Organizations adopting SQL Buddy AI can achieve:

- Reduced dependency on technical teams
- Faster access to enterprise information
- Self-service analytics
- Improved AI governance
- Reduced SQL errors
- Better compliance and auditability
- Increased business productivity

---

# 🔮 Future Roadmap

## Phase 2

- Multi-Database Support
- Oracle
- SQL Server
- Snowflake
- Azure SQL

---

## Phase 3

- Power BI Integration

- Interactive Charts

- Voice Assistant

- Azure OpenAI

- Role-Based Access Control (RBAC)

- Enterprise SSO

- Docker Deployment

- Kubernetes

- AI Query Explanation

---


# ⭐ Why SQL Buddy AI?

Most open-source Text-to-SQL applications focus only on SQL generation.

SQL Buddy AI goes significantly further by incorporating:

- Enterprise Architecture
- AI Governance
- Schema Validation
- Hallucination Prevention
- Audit Logging
- KPI Monitoring
- Production Deployment
- Modular Design

This makes it a strong foundation for enterprise AI copilots.

---

# 👨‍💻 Author

## Bharat Arora

**Machine Learning & AI Engineer**

MS in Machine Learning & AI

### Areas of Interest

- Generative AI
- Enterprise AI
- Retrieval-Augmented Generation
- LLM Applications
- AI Agents
- Machine Learning
- MLOps
- Data Engineering

---

# 📄 License

This project is released under the MIT License.

---

# 🙏 Acknowledgements

Special thanks to

- Groq
- FastAPI
- PostgreSQL
- SQLAlchemy
- ChromaDB
- Bootstrap
- OpenAI research community
- Scaler School of Technology

---

# 🌟 If you found this project useful

Please consider giving the repository a ⭐ on GitHub.

It helps others discover the project and supports continued development.
