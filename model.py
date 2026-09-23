import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, MessagesState
from fastapi import FastAPI
import uvicorn
import threading

# Initialize the Llama3.2 model via local Ollama server
llm = ChatOllama(model="llama3.2", temperature=0.7)

# Define the workflow state graph for the agentic chatbot
workflow = StateGraph(MessagesState)

def call_model(state: MessagesState):
    # System prompt to give the agent its persona
    system_message = SystemMessage(content="You are an autonomous, helpful Agentic AI assistant powered by Llama 3.2.")
    messages = [system_message] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# Add node and edges to the agent graph
workflow.add_node("agent", call_model)
workflow.set_entry_point("agent")
workflow.set_finish_point("agent")

# Compile the agent app
app_agent = workflow.compile()

# Setup FastAPI for the User Interface / API deployment
app = FastAPI(title="Agentic AI Llama3.2 Chatbot")

@app.post("/chat")
def chat_endpoint(prompt: str):
    initial_state = {"messages": [HumanMessage(content=prompt)]}
    result = app_agent.invoke(initial_state)
    latest_message = result["messages"][-1]
    return {"response": latest_message.content}

@app.get("/")
def root():
    return {"message": "Agentic AI Llama3.2 Ollama Server is running. Use /chat?prompt=your_message to interact."}

if __name__ == "__main__":
    print("Starting Agentic AI Chatbot with Llama3.2 and Ollama...")
    print("Deployed URL: http://127.0.0.1:8000")
    print("API documentation available at: http://127.0.0.1:8000/docs")
    
    # Run the FastAPI application using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
