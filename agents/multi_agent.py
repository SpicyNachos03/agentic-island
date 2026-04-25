"""
Multi-agent orchestration using LangGraph with Gemma.
This demonstrates multiple specialized agents working together.
"""

from typing import TypedDict, Annotated, Sequence, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import operator
from gemma_llm import create_gemma_llm


# Define the state
class MultiAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    current_agent: str
    research_data: str
    analysis_data: str


def create_research_agent(base_url: str):
    """Create a research agent that gathers information."""
    
    llm = create_gemma_llm(base_url=base_url, temperature=0.5, max_new_tokens=512)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a research agent. Your job is to gather and summarize information on the given topic. Provide factual, well-organized information."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    def research_node(state: MultiAgentState):
        messages = state["messages"]
        response = chain.invoke({"messages": messages})
        return {
            "messages": [AIMessage(content=f"[RESEARCH AGENT]: {response}")],
            "research_data": response,
            "current_agent": "analysis"
        }
    
    return research_node


def create_analysis_agent(base_url: str):
    """Create an analysis agent that processes research data."""
    
    llm = create_gemma_llm(base_url=base_url, temperature=0.3, max_new_tokens=512)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an analysis agent. Your job is to analyze the research data and provide insights, conclusions, and recommendations. Be critical and thorough."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    def analysis_node(state: MultiAgentState):
        messages = state["messages"]
        response = chain.invoke({"messages": messages})
        return {
            "messages": [AIMessage(content=f"[ANALYSIS AGENT]: {response}")],
            "analysis_data": response,
            "current_agent": "summary"
        }
    
    return analysis_node


def create_summary_agent(base_url: str):
    """Create a summary agent that provides final conclusions."""
    
    llm = create_gemma_llm(base_url=base_url, temperature=0.4, max_new_tokens=512)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a summary agent. Your job is to synthesize the research and analysis into a clear, actionable summary. Highlight key findings and recommendations."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    def summary_node(state: MultiAgentState):
        messages = state["messages"]
        response = chain.invoke({"messages": messages})
        return {
            "messages": [AIMessage(content=f"[SUMMARY AGENT]: {response}")],
            "current_agent": "end"
        }
    
    return summary_node


def create_multi_agent_system(base_url: str = "http://localhost:8000"):
    """
    Create a multi-agent system with specialized agents.
    
    Args:
        base_url: The base URL of the Gemma HTTP API endpoint
    
    Returns:
        A compiled LangGraph multi-agent system
    """
    
    # Create the agents
    research_node = create_research_agent(base_url)
    analysis_node = create_analysis_agent(base_url)
    summary_node = create_summary_agent(base_url)
    
    # Build the graph
    workflow = StateGraph(MultiAgentState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("summary", summary_node)
    
    # Add edges
    workflow.set_entry_point("research")
    workflow.add_edge("research", "analysis")
    workflow.add_edge("analysis", "summary")
    workflow.add_edge("summary", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def run_multi_agent(query: str, base_url: str = "http://localhost:8000"):
    """
    Run the multi-agent system with a query.
    
    Args:
        query: The user's query
        base_url: The base URL of the Gemma HTTP API endpoint
    """
    print(f"Creating multi-agent system with Gemma at {base_url}...")
    app = create_multi_agent_system(base_url=base_url)
    
    print(f"\nQuery: {query}")
    print("=" * 70)
    
    # Run the multi-agent system
    result = app.invoke({
        "messages": [HumanMessage(content=query)],
        "current_agent": "research",
        "research_data": "",
        "analysis_data": ""
    })
    
    print("\nMulti-Agent Collaboration Results:")
    print("=" * 70)
    
    for msg in result["messages"]:
        print(f"\n{msg.content}\n")
    
    print("=" * 70)


if __name__ == "__main__":
    # Test the multi-agent system
    test_query = "Analyze the impact of artificial intelligence on modern healthcare."
    
    print("=== Gemma Multi-Agent System ===\n")
    print("This system uses three specialized agents:")
    print("1. Research Agent - Gathers information")
    print("2. Analysis Agent - Analyzes the data")
    print("3. Summary Agent - Provides final conclusions\n")
    
    print("Note: Make sure Gemma HTTP API is running at http://localhost:8000")
    print("If running on remote ASUS, update the base_url parameter.\n")
    
    try:
        run_multi_agent(test_query, base_url="http://localhost:8000")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Gemma HTTP API server is running")
        print("2. Check the base_url is correct")
        print("3. If connecting to ASUS, use the ASUS IP address")
        print("   Example: base_url='http://<ASUS_IP>:8000'")
