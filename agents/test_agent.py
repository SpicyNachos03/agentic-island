"""
Test agent for LangChain/LangGraph with Gemma.
This demonstrates a simple agent that can answer questions using Gemma.
"""

from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import operator
from gemma_llm import create_gemma_llm


# Define the state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


def create_test_agent(base_url: str = "http://localhost:8000"):
    """
    Create a simple test agent that uses Gemma.
    
    Args:
        base_url: The base URL of the Gemma HTTP API endpoint
    
    Returns:
        A compiled LangGraph agent
    """
    
    # Create the Gemma LLM
    llm = create_gemma_llm(
        base_url=base_url,
        temperature=0.7,
        max_new_tokens=512,
    )
    
    # Define the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant powered by Gemma. Answer the user's questions clearly and concisely."),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    # Create the chain
    chain = prompt | llm | StrOutputParser()
    
    # Define the agent function
    def agent_node(state: AgentState):
        messages = state["messages"]
        response = chain.invoke({"messages": messages})
        return {"messages": [AIMessage(content=response)]}
    
    # Build the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    
    # Add edges
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def run_test_agent(query: str, base_url: str = "http://localhost:8000"):
    """
    Run the test agent with a query.
    
    Args:
        query: The user's query
        base_url: The base URL of the Gemma HTTP API endpoint
    """
    print(f"Creating agent with Gemma at {base_url}...")
    app = create_test_agent(base_url=base_url)
    
    print(f"\nQuery: {query}")
    print("=" * 50)
    
    # Run the agent
    result = app.invoke({
        "messages": [HumanMessage(content=query)]
    })
    
    print("\nResponse:")
    print(result["messages"][-1].content)
    print("=" * 50)


if __name__ == "__main__":
    # Test the agent
    test_query = "What is the capital of France? Please explain briefly."
    
    print("=== Gemma Test Agent ===\n")
    print("Note: Make sure Gemma HTTP API is running at http://localhost:8000")
    print("If running on remote ASUS, update the base_url parameter.\n")
    
    try:
        run_test_agent(test_query, base_url="http://localhost:8000")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Gemma HTTP API server is running")
        print("2. Check the base_url is correct")
        print("3. If connecting to ASUS, use the ASUS IP address")
        print("   Example: base_url='http://<ASUS_IP>:8000'")
