# 🤖 KPI Insight Agent

An **agentic KPI intelligence platform** that continuously monitors business metrics, detects anomalies, performs **causal analysis**, answers **natural-language data questions**, and generates **actionable business recommendations** — all in one unified system.

This project demonstrates how **LLM-powered agents** can be combined with classical analytics to build **decision‑ready intelligence systems** rather than simple dashboards.

---

## 🚀 What This Project Does

The KPI Insight Agent acts like a **virtual business analyst**:

* 📊 **Monitors KPIs** (revenue, trends, alerts)
* 🧠 **Explains why changes happened** using causal analysis
* 💬 **Answers business questions** in natural language ("What was the avg revenue in last 30 days?")
* 💡 **Recommends concrete actions** when issues are detected
* 🤖 **Autonomous agent workflow** that ties everything together

Instead of just showing numbers, it tells you:

> *What changed, why it changed, and what to do next.*

---

## 🧠 Core Capabilities

### 1️⃣ KPI Monitoring

* Computes total revenue and average daily revenue
* Tracks daily trends
* Detects revenue drops and flags alerts automatically

### 2️⃣ Talk to Your Data (Natural Language Queries)

Ask questions like:

* *What was the average revenue in the last 10 days?*
* *Which category performed worst last week?*
* *Show revenue trend for the last month*

The system:

* Converts questions into Pandas logic
* Executes safely on the dataset
* Returns **answer + explanation + generated code**

### 3️⃣ Causal Analysis

When KPIs change, the system:

* Compares recent vs previous windows
* Identifies **top contributing factors**
* Quantifies impact per category
* Explains *why* the KPI moved

Example output:

```json
{
  "kpi": "Overall Revenue",
  "change_percent": -2.91,
  "top_causes": [
    {"factor": "Sports & Outdoors", "impact": -63800}
  ]
}
```

### 4️⃣ Actionable Recommendations

Based on causal signals:

* Generates prioritized actions
* Explains reasoning
* Estimates expected impact

Example:

```json
{
  "action": "Increase promotions for Beauty & Health",
  "priority": "High"
}
```

### 5️⃣ KPI Intelligence Agent

A single agent endpoint that:

1. Runs KPI monitoring
2. Triggers causal analysis on deviations
3. Generates recommendations
4. Returns a unified intelligence report

---

## 🏗️ System Architecture

```
frontend (Next.js + shadcn/ui)
   │
   ▼
backend (FastAPI)
   │
   ├── KPI Monitor
   ├── Talk-to-Data Engine
   ├── Causal Analyzer
   ├── Recommendation Engine
   └── Agent Orchestrator
```

---

## 🧰 Tech Stack

### Frontend

* **Next.js (App Router)**
* **TypeScript**
* **shadcn/ui + Tailwind CSS**
* **Recharts** (charts)
* **Framer Motion** (animations)

### Backend

* **FastAPI**
* **Pandas / NumPy**
* **Pydantic**
* **LLM integration (OpenAI‑style)**

### Data

* CSV‑based KPI dataset (easily replaceable with DB)

---

## 📁 Project Structure

```
kpi-insight-agent/
│
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── monitor.py
│   │   ├── ask.py
│   │   ├── causal.py
│   │   ├── recommend.py
│   │   └── agent.py
│   ├── kpi_intel/
│   │   ├── core/
│   │   ├── services/
│   │   └── data/
│
├── frontend/
│   ├── src/app/
│   │   ├── page.tsx
│   │   ├── dashboard/
│   │   ├── chat/
│   │   ├── causal/
│   │   ├── recommendations/
│   │   └── agent/
│   ├── src/lib/api.ts
│   └── src/components/ui/
```

---

## ▶️ How to Run Locally

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:3000
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

---

## 🔌 API Endpoints

| Method | Endpoint     | Description                 |
| ------ | ------------ | --------------------------- |
| POST   | `/monitor`   | KPI monitoring              |
| POST   | `/ask`       | Natural language data Q&A   |
| POST   | `/causal`    | Causal analysis             |
| POST   | `/recommend` | Actionable recommendations  |
| POST   | `/agent`     | Full KPI intelligence agent |

---

## 📊 Example Agent Output

```json
{
  "summary": "Revenue deviation detected",
  "monitor": {...},
  "causal_analysis": {...},
  "recommendations": [...]
}
```

---

## 🎯 Why This Project Matters

This project goes beyond dashboards:

* ❌ Not just charts
* ❌ Not just SQL queries
* ✅ **Autonomous decision intelligence**

It demonstrates:

* Agentic workflows
* Explainable analytics
* Business‑ready AI systems

Perfect for **AI Engineer / ML Engineer / Backend Engineer** portfolios.

---

## 🔮 Future Enhancements

* Database integration (PostgreSQL / BigQuery)
* Streaming KPIs
* Multi‑agent architecture
* Role‑based access
* Forecasting & scenario simulation

---

## 🧑‍💻 Author

Built with ❤️ as an end‑to‑end **AI + Analytics system**.

---

⭐ If you found this useful, give the repo a star!
