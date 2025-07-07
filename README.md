# 🧠 Deep Research AI Agentic System

An automated agentic system that performs deep web research and compiles structured reports using **LangGraph**, **Gemini 1.5 Pro**, and **Tavily Search API**. This multi-agent pipeline is designed to take a user query and return a detailed research draft, complete with key findings and supporting evidence.

---

## 🔧 Technologies Used

- **LangGraph** – for building a stateful multi-agent graph-based workflow  
- **LangChain Core** – for message passing between agents  
- **Gemini 1.5 Pro (Google Generative AI)** – for structured drafting of research content  
- **Tavily API** – for real-time web search and retrieval  
- **Python** – with `Typing`, `datetime`, and `os` modules

---

## 🧬 System Architecture

### 🔁 Agent Flow
```text
[START] → [Researcher Agent (Tavily)] → [Drafter Agent (Gemini)] → [END]
```

- **Researcher Agent**:  
  Uses Tavily API to perform deep web research and extract summarized and raw content.

- **Drafter Agent**:  
  Uses Gemini 1.5 Pro to convert research results into a formal report, structured into:
  1. Executive Summary  
  2. Key Findings  
  3. Supporting Evidence  
  4. Conclusions

---

## 📦 How to Use

### 1️⃣ Set your API keys as environment variables

```bash
export GEMINI_API_KEY=your_gemini_api_key
export TAVILY_API_KEY=your_tavily_api_key
```
### 2️⃣ Install the required packages

```bash
pip install langgraph langchain-core langchain-google-genai tavily
```

### 3️⃣ Run the system
```bash
from your_script import research_chain

result = research_chain.invoke({
    "query": "Who is the prime minister of India?"
})
print(result["draft"])
```
