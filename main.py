from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from tavily import TavilyClient
from typing import TypedDict, Annotated, Dict, Union
from datetime import datetime
from langgraph.graph import START
import os

# Initialize components
tavily = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",  # Updated model name [3][5]
    google_api_key=os.environ.get("GEMINI_API_KEY"),
    temperature=0.3,
    max_output_tokens=2048,
    http_options={"api_version": "v1","timeout": 30.0}  # Force stable API [2][6]
)

class ResearchState(TypedDict):
    query: str
    research_data: Dict[str, Union[str, list]]
    draft: str

def research_agent(state: ResearchState):
    """Agent that performs web research using Tavily"""
    results = tavily.search(
        query=state["query"],
        search_depth="advanced",
        max_results=5,
        include_answer=True,
        include_raw_content=True
    )
    
    return {
        "research_data": {
            "answer": results.get("answer", ""),
            "results": results.get("results", []),
            "raw_content": results.get("raw_content", "")
        }
    }

def draft_agent(state: ResearchState):
    """Agent that structures research findings"""
    system_prompt = f"""Today's date: {datetime.now().strftime('%Y-%m-%d')}
    Structure research findings into a formal report with:
    1. Executive Summary
    2. Key Findings
    3. Supporting Evidence
    4. Conclusions"""
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=str(state["research_data"]))
    ])
    
    return {"draft": response.content}

# Define workflow
workflow = StateGraph(ResearchState)
workflow.add_node("researcher", research_agent)
workflow.add_node("drafter", draft_agent)

# Set up edges
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "drafter")
workflow.add_edge("drafter", END)

# Compile the graph
research_chain = workflow.compile()

# Run the system
result = research_chain.invoke({
    "query": "Who is the prime minister of India?"
})

print(result["draft"])
