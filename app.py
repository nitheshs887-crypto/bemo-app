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
    <title>Llama 3.2 Local Chatbot running inside Flask</title>
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
                { role: 'assistant', content: 'Hello! I am your local Llama 3.2 chatbot. How can I help you today?' }
            ]);
            const [input, setInput] = React.useState('');
            const [loading, setLoading] = React.useState(false);
            const messagesEndRef = React.useRef(null);

            const scrollToBottom = () => {
                messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
            };

            React.useEffect(() => {
                scrollToBottom();
            }, [messages, loading]);

            const sendMessage = async (e) => {
                e.preventDefault();
                if (!input.trim() || loading) return;

                const userMessage = input.trim();
                setInput('');
                const newMessages = [...messages, { role: 'user', content: userMessage }];
                setMessages(newMessages);
                setLoading(true);

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ messages: newMessages })
                    });
                    const data = await response.json();
                    if (data.error) {
                        setMessages([...newMessages, { role: 'assistant', content: 'Error: ' + data.error }]);
                    } else {
                        setMessages([...newMessages, { role: 'assistant', content: data.reply }]);
                    }
                } catch (err) {
                    setMessages([...newMessages, { role: 'assistant', content: 'Error connecting to local Ollama server.' }]);
                } finally {
                    setLoading(false);
                }
            };

            return (
                <div className="flex flex-col h-screen max-w-4xl mx-auto w-full p-4">
                    <header className="bg-slate-900 border border-slate-800 p-4 rounded-t-2xl shadow-xl flex justify-between items-center">
                        <h1 className="text-xl font-bold text-cyan-400 font-mono">Llama 3.2 Chatbot (Ollama)</h1>
                        <span className="text-xs font-mono text-emerald-400 bg-emerald-950/50 px-2.5 py-1 rounded-full border border-emerald-800">● Connected</span>
                    </header>

                    <div className="flex-1 bg-slate-900/50 border-x border-slate-800 p-4 overflow-y-auto space-y-4 font-mono text-sm">
                        {messages.map((msg, index) => (
                            <div key={index} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-4 rounded-2xl ${msg.role === 'user' ? 'bg-cyan-600 text-white rounded-br-none' : 'bg-slate-800 text-slate-200 border border-slate-700 rounded-bl-none'}`}>
                                    <p className="whitespace-pre-wrap">{msg.content}</p>
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-slate-800 text-slate-400 border border-slate-700 p-4 rounded-2xl rounded-bl-none animate-pulse">
                                    Thinking...
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    <form onSubmit={sendMessage} className="bg-slate-900 border border-slate-800 p-4 rounded-b-2xl shadow-xl flex gap-3">
                        <input 
                            type="text" 
                            placeholder="Message Llama 3.2..." 
                            value={input} 
                            onChange={(e) => setInput(e.target.value)}
                            className="flex-1 bg-slate-950 border border-slate-700 p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 text-slate-200 font-mono text-sm"
                        />
                        <button 
                            type="submit"
                            disabled={loading}
                            className="bg-cyan-600 hover:bg-cyan-500 disabled:opacity-50 text-white font-mono font-bold py-3 px-6 rounded-xl shadow transition"
                        >
                            Send
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
    messages = data.get("messages", [])
    
    ollama_payload = {
        "model": "llama3.2",
        "messages": messages,
        "stream": False
    }

    req = urllib.request.Request(
        "http://localhost:11434/api/chat",
        data=json.dumps(ollama_payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            reply = res_data.get("message", {}).get("content", "")
            return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": f"Failed to connect to Ollama. Make sure Ollama is running locally and 'llama3.2' is installed. Details: {str(e)}"}), 500

if __name__ == "__main__":
    print(" * Running Llama 3.2 Chatbot application...")
    print(" * Serving application at http://127.0.0.1:5000")
    print(" * Ensure Ollama is running locally at http://localhost:11434 with 'llama3.2'")
    app.run(host="0.0.0.0", port=5000, debug=True)
