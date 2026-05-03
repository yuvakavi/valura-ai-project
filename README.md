# Valura AI — Financial Co-Investor Microservice

## Overview

This project implements the **core intelligence layer** for Valura’s AI co-investor system.
It enables novice investors to **build, monitor, grow, and protect** their portfolios through a modular AI agent architecture.

The system processes user queries, ensures safety, classifies intent, routes to the appropriate agent, and streams responses in real time.

---

## System Architecture

```
User Query
   ↓
Safety Guard (No LLM, <10ms)
   ↓
Intent Classifier (LLM / Rule-based)
   ↓
Router
   ↓
Agent (Portfolio Health / Stub Agents)
   ↓
SSE Streaming Response
```

---

## Key Components

### 1. Safety Guard (`src/safety.py`)

* Fully local (no LLM, no network)
* Detects:

  * Insider trading
  * Market manipulation
  * Guaranteed returns
  * Illegal financial activity
* Ensures **high recall (≥95%)**
* Allows educational queries

---

### 2. Intent Classifier (`src/classifier.py`)

* Single decision point for routing
* Extracts:

  * intent
  * entities (tickers, etc.)
  * target agent
* Handles:

  * follow-up queries
  * financial terminology
* Achieves:

  * **89.1% accuracy**

---

### 3. Portfolio Health Agent (`src/agents/portfolio_health.py`)

* Core implemented agent (MONITOR + PROTECT)
* Provides:

  * concentration risk
  * performance metrics
  * benchmark comparison
  * actionable insights
* Handles:

  * empty portfolios gracefully
* Returns structured output + disclaimer

---

### 4. Router (`src/core/router.py`)

* Routes request to correct agent
* Supports:

  * full agent execution
  * stub fallback for unimplemented agents

---

### 5. Streaming Layer (`src/core/streaming.py`)

* Implements **Server-Sent Events (SSE)**
* Streams:

  * status updates
  * final response
* Ensures real-time UX

---

### 6. FastAPI Application (`src/main.py`)

* Single endpoint: `/query`
* End-to-end pipeline execution
* Structured SSE response
* Error-safe handling

---

## Why SSE (Streaming)?

* Reduces perceived latency
* First token < 2s
* Real-time feedback to user
* Better UX than blocking APIs

---

## Setup Instructions

### 1. Clone repository

```bash
git clone <repo-url>
cd valura-ai-project
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment variables

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

*(Note: tests run without API key using mocks)*

---

### 5. Run the server

```bash
python -m uvicorn src.main:app --reload
```

---

### 6. Test API

Open:

```
http://127.0.0.1:8000/docs
```

---

## Running Tests

```bash
pytest tests/ -v
```

### Results

* Classifier Accuracy: **89.1%**
* Safety Recall: **100%**
* All tests passing ✅

---

## Design Decisions

### Why FastAPI?

* Async support
* High performance
* Easy SSE integration

---

### Why Rule-Based Classifier?

* Lower cost (no LLM dependency)
* Deterministic behavior
* Faster (<100ms)

---

### Why SSE?

* Real-time streaming
* Better UX for conversational AI

---

### Why In-Memory Data?

* Simplicity for demo
* No external dependency
* Faster development cycle

---

## Tradeoffs

| Decision                 | Tradeoff               |
| ------------------------ | ---------------------- |
| Rule-based classifier    | Less flexible than LLM |
| No DB persistence        | No long-term storage   |
| Simple entity extraction | Limited NLP capability |

---

## Safety Considerations

* Blocks harmful financial intent
* Allows educational queries
* Prevents:

  * insider trading
  * manipulation
  * illegal activities

---

## Future Improvements

* LLM-based classifier fallback
* Embedding-based intent detection
* Multi-agent orchestration
* Persistent storage (Postgres)
* Real-time market data integration

---

## Defence Video

🔗 https://drive.google.com/file/d/1zFPWb0-WgX7qT8k7cKkWWwA_Ik_5sApG/view?usp=sharing

---

## Conclusion

This system provides a **scalable, safe, and modular foundation** for Valura’s AI co-investor platform.
It balances **performance, cost, and user safety**, while being extensible for future agents.

---
