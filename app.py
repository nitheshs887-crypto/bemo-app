import os
import subprocess
import sys
import json
import urllib.request

try:
    import flask
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])

from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Agentic AI - Llama 3.2 Ollama Chatbot</title>
    <!-- Load React, ReactDOM, and Babel for in-browser JSX transformation -->
    <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 h-screen flex flex-col">
    <div id="root" class="h-full flex flex-col"></div>

    <script type="text/babel">
        function App() {
            const [messages, setMessages] = React.useState([
                { role: 'agent', content: 'Hello! I am your Llama 3.2 Agentic AI assistant running locally via Ollama. How can I assist you with your code or tasks today?' }
            ]);
            const [input, setInput] = React.useState('');
            const [loading, setLoading] = React.useState(false);
            const messagesEndRef = React.useRef(null);

            const scrollToBottom = () => {
                messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
            };

            React.useEffect(() => {
                scrollToBottom();
            }, [messages, loading]);

            const handleSubmit = async (e) => {
                e.preventDefault();
                if (!input.trim() || loading) return;

                const userMessage = input.trim();
                setInput('');
                setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
                setLoading(true);

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: userMessage })
                    });
                    const data = await response.json();
                    
                    if (data.error) {
                        setMessages(prev => [...prev, { role: 'agent', content: 'Error: ' + data.error }]);
                    } else {
                        setMessages(prev => [...prev, { role: 'agent', content: data.reply }]);
                    }
                } catch (err) {
                    setMessages(prev => [...prev, { role: 'agent', content: 'Failed to connect to local Ollama agent server.' }]);
                } finally {
                    setLoading(false);
                }
            };

            return (
                <div className="flex flex-col h-screen max-w-4xl mx-auto w-full p-4">
                    <!-- Header -->
                    <header className="bg-slate-900/85 backdrop-blur-xl border border-cyan-500/40 p-4 rounded-2xl shadow-[0_0_35px_rgba(6,182,212,0.15)] flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-3">
                            <div className="w-3 h-3 bg-cyan-400 rounded-full animate-ping"></div>
                            <h1 className="text-xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-fuchsia-500 font-mono">Llama 3.2 Agentic AI Chatbot</h1>
                        </div>
                        <div className="text-xs font-mono text-cyan-300 bg-cyan-950/80 px-3 py-1 rounded-full border border-cyan-500/30">
                            Active Agent
                        </div>
                    </header>

                    <!-- Chat Container -->
                    <div className="flex-1 bg-slate-900/50 backdrop-blur-md border border-slate-800 rounded-2xl p-4 overflow-y-auto mb-4 flex flex-col space-y-4 shadow-inner">
                        {messages.map((msg, index) => (
                            <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-4 rounded-2xl font-mono text-sm leading-relaxed ${
                                    msg.role === 'user' 
                                        ? 'bg-cyan-600/20 text-cyan-100 border border-cyan-500/30 rounded-br-none' 
                                        : 'bg-slate-800/80 text-slate-200 border border-slate-700 rounded-bl-none shadow'
                                }`}>
                                    <div className="text-xs text-slate-400 mb-1 font-bold uppercase tracking-wider">
                                        {msg.role === 'user' ? 'User' : 'Agentic AI'}
                                    </div>
                                    <div className="whitespace-pre-wrap">{msg.content}</div>
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-slate-800/80 border border-slate-700 p-4 rounded-2xl rounded-bl-none font-mono text-sm text-cyan-400 flex items-center space-x-2">
                                    <span>Agent is reasoning</span>
                                    <span className="animate-pulse">...</span>
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <!-- Input Form -->
                    <form onSubmit={handleSubmit} className="flex gap-2">
                        <input 
                            type="text" 
                            placeholder="Ask the Llama 3.2 agentic model anything..." 
                            value={input} 
                            onChange={(e) => setInput(e.target.value)}
                            className="flex-1 bg-slate-900 border border-slate-700 p-4 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 text-slate-200 font-mono text-sm shadow-inner transition"
                        />
                        <button 
                            type="submit"
                            disabled={loading}
                            className="bg-gradient-to-r from-cyan-600 to-fuchsia-600 hover:from-cyan-500 hover:to-fuchsia-500 text-white font-mono font-bold px-6 py-4 rounded-xl shadow transition transform active:scale-95 disabled:opacity-50 border border-cyan-500/40"
                        >
                            SEND
                        </button>
                    </form>
                </div>
            );
        }

        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    # Payload for local Ollama running llama3.2
    ollama_payload = {
        "model": "llama3.2",
        "prompt": f"You are an advanced agentic AI assistant. Answer accurately and assist with coding and tasks.\n\nUser: {user_message}\nAgent:",
        "stream": False
    }

    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(ollama_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            reply = result.get("response", "No response generated from model.")
            return jsonify({"reply": reply})
    except Exception as e:
        # Fallback simulation response if local ollama server is not active
        fallback_reply = f"[Simulated Agentic Response - Ollama offline] I received your prompt: '{user_message}'. To use local Llama 3.2, ensure 'ollama run llama3.2' or 'ollama serve' is running on your machine."
        return jsonify({"reply": fallback_reply})

if __name__ == "__main__":
    print(" * Running agentic chat bot application...")
    print(" * Serving application at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
