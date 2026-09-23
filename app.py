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
<body class="bg-slate-950 text-slate-100 h-screen flex flex-col">
    <div id="root" class="h-full flex flex-col"></div>

    <script type="text/babel">
        function App() {
            const [count, setCount] = React.useState(0);
            const [text, setText] = React.useState('');
            const currentUrl = window.location.href;

            return (
                <div className="flex flex-col h-screen max-w-4xl mx-auto w-full p-4 justify-center items-center">
                    <div className="bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl w-full max-w-md flex flex-col space-y-6">
                        <h1 className="text-xl font-bold text-cyan-400 text-center font-mono">React.js User Interface Interactive component running inside Flask</h1>
                        
                        <div className="text-center font-mono">
                            <span className="text-slate-400">Count: </span>
                            <span className="text-2xl font-bold text-fuchsia-400">{count}</span>
                        </div>

                        <button 
                            onClick={() => setCount(count + 1)}
                            className="bg-cyan-600 hover:bg-cyan-500 text-white font-mono font-bold py-3 px-4 rounded-xl shadow transition"
                        >
                            Increment
                        </button>

                        <div className="flex flex-col space-y-2">
                            <input 
                                type="text" 
                                placeholder="Type something..." 
                                value={text} 
                                onChange={(e) => setText(e.target.value)}
                                className="bg-slate-950 border border-slate-700 p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 text-slate-200 font-mono text-sm"
                            />
                            <div className="font-mono text-sm text-slate-300">
                                You typed: <span className="text-cyan-400">{text || 'error'}</span>
                            </div>
                        </div>

                        <div className="text-xs font-mono text-slate-500 text-center break-all pt-2 border-t border-slate-800">
                            Current URL: <a href={currentUrl} className="text-cyan-400 underline">{currentUrl}</a>
                        </div>
                    </div>
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

if __name__ == "__main__":
    print(" * Running React component application...")
    print(" * Serving application at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
