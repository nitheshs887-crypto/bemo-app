import os
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, MessagesState
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
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

@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Llama 3.2 Chatbot</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .chat-container { width: 400px; background: white; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: flex; flexDirection: column; overflow: hidden; height: 500px; }
            .chat-header { background: #007bff; color: white; padding: 15px; text-align: center; font-weight: bold; }
            .chat-messages { flex: 1; padding: 15px; overflow-y: auto; display: flex; flexDirection: column; gap: 10px; }
            .message { max-width: 80%; padding: 10px; border-radius: 5px; line-height: 1.4; }
            .user-message { background: #007bff; color: white; align-self: flex-end; }
            .bot-message { background: #e9ecef; color: #333; align-self: flex-start; }
            .chat-input-area { display: flex; border-top: 1px solid #ddd; padding: 10px; background: #fff; }
            .chat-input-area input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 4px; outline: none; }
            .chat-input-area button { background: #007bff; color: white; border: none; padding: 10px 15px; margin-left: 5px; border-radius: 4px; cursor: pointer; }
            .chat-input-area button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">Llama 3.2 Chatbot</div>
            <div class="chat-messages" id="chatMessages">
                <div class="message bot-message">Hello! I am your Llama 3.2 assistant. How can I help you today?</div>
            </div>
            <div class="chat-input-area">
                <input type="text" id="userInput" placeholder="Type a message..." onkeydown="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script>
            async function sendMessage() {
                const inputField = document.getElementById('userInput');
                const chatMessages = document.getElementById('chatMessages');
                const prompt = inputField.value.trim();

                if (!prompt) return;

                // Append user message
                const userMsgDiv = document.createElement('div');
                userMsgDiv.className = 'message user-message';
                userMsgDiv.textContent = prompt;
                chatMessages.appendChild(userMsgDiv);

                inputField.value = '';
                chatMessages.scrollTop = chatMessages.scrollHeight;

                // Append temporary loading message
                const botMsgDiv = document.createElement('div');
                botMsgDiv.className = 'message bot-message';
                botMsgDiv.textContent = 'Thinking...';
                chatMessages.appendChild(botMsgDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;

                try {
                    const response = await fetch(`/chat?prompt=${encodeURIComponent(prompt)}`, {
                        method: 'POST'
                    });
                    const data = await response.json();
                    botMsgDiv.textContent = data.response;
                } catch (error) {
                    botMsgDiv.textContent = 'Error connecting to the server.';
                }
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    print("Starting Agentic AI Chatbot with Llama3.2 and Ollama...")
    print("Deployed URL: http://127.0.0.1:8000")
    print("API documentation available at: http://127.0.0.1:8000/docs")
    
    # Run the FastAPI application using uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
