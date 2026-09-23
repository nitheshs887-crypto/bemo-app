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
    <title>React.js User Interface Interactive component running inside Flask</title>
    <!-- Load React, ReactDOM, and Babel for in-browser JSX transformation -->
    <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 text-slate-100 min-h-screen flex flex-col justify-between">
    <div id="root" class="w-full flex flex-col items-center justify-center p-4 my-auto"></div>

    <script type="text/babel">
        function App() {
            const [count, setCount] = React.useState(0);
            const [text, setText] = React.useState('');
            const [items, setItems] = React.useState(['Explore UI', 'Build React component', 'Deploy with Flask']);

            const addItem = () => {
                if (text.trim()) {
                    setItems([...items, text.trim()]);
                    setText('');
                }
            };

            return (
                <div className="flex flex-col items-center justify-center max-w-lg mx-auto w-full space-y-6">
                    <div className="text-center space-y-2">
                        <span className="bg-purple-500/10 border border-purple-500/30 text-purple-400 text-xs font-mono px-3 py-1 rounded-full uppercase tracking-widest">Enhanced Dashboard</span>
                        <h1 className="text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 font-mono">
                            React.js User Interface Interactive component running inside Flask
                        </h1>
                    </div>
                    
                    <div className="bg-slate-900/80 backdrop-blur border border-purple-500/20 p-6 rounded-2xl shadow-2xl w-full flex flex-col items-center space-y-4">
                        <div className="text-sm font-mono text-slate-400 uppercase tracking-wider">Interactive Counter</div>
                        <div className="text-4xl font-black text-cyan-400 font-mono">{count}</div>
                        <div className="flex space-x-3 w-full">
                            <button 
                                onClick={() => setCount(count - 1)}
                                className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono font-bold py-2.5 px-4 rounded-xl shadow border border-slate-700 transition"
                            >
                                Decrease
                            </button>
                            <button 
                                onClick={() => setCount(count + 1)}
                                className="flex-1 bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 text-white font-mono font-bold py-2.5 px-4 rounded-xl shadow-lg shadow-purple-900/30 transition"
                            >
                                Increment
                            </button>
                        </div>
                    </div>

                    <div className="bg-slate-900/80 backdrop-blur border border-purple-500/20 p-6 rounded-2xl shadow-2xl w-full flex flex-col space-y-4">
                        <div className="text-sm font-mono text-slate-400 uppercase tracking-wider">Dynamic Item Manager</div>
                        <div className="flex space-x-2">
                            <input 
                                type="text" 
                                placeholder="Add a new task or item..." 
                                value={text} 
                                onChange={(e) => setText(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && addItem()}
                                className="flex-1 bg-slate-950 border border-slate-700 p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 text-slate-200 font-mono text-sm"
                            />
                            <button 
                                onClick={addItem}
                                className="bg-purple-600 hover:bg-purple-500 text-white font-mono font-bold px-5 rounded-xl shadow transition"
                            >
                                Add
                            </button>
                        </div>
                        <div className="space-y-2 max-h-40 overflow-y-auto pr-1">
                            {items.map((item, index) => (
                                <div key={index} className="bg-slate-950/60 border border-slate-800/80 px-4 py-2.5 rounded-xl text-sm font-mono text-slate-300 flex items-center justify-between">
                                    <span>{item}</span>
                                    <span className="text-xs text-purple-400 bg-purple-950/50 px-2 py-0.5 rounded-md">#{index + 1}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            );
        }

        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
    <footer className="text-center py-4 text-xs font-mono text-slate-500">
        Flask &bull; React &bull; Tailwind CSS
    </footer>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    print(" * Running application...")
    print(" * Serving application at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
