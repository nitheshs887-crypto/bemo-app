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

            return (
                <div className="flex flex-col items-center justify-center h-screen max-w-md mx-auto w-full p-4 space-y-6">
                    <h1 className="text-xl font-bold text-cyan-400 font-mono text-center">React.js User Interface Interactive component running inside Flask</h1>
                    
                    <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl w-full flex flex-col items-center space-y-4">
                        <p className="text-lg font-mono">Count: {count}</p>
                        <button 
                            onClick={() => setCount(count + 1)}
                            className="bg-cyan-600 hover:bg-cyan-500 text-white font-mono font-bold py-2 px-4 rounded-xl shadow transition"
                        >
                            Increment
                        </button>
                    </div>

                    <div className="bg-slate-900 border border-slate-800 p-6 rounded-2xl shadow-xl w-full flex flex-col space-y-3">
                        <input 
                            type="text" 
                            placeholder="Type something..." 
                            value={text} 
                            onChange={(e) => setText(e.target.value)}
                            className="w-full bg-slate-950 border border-slate-700 p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 text-slate-200 font-mono text-sm"
                        />
                        <p className="text-sm font-mono text-slate-300">You typed: {text}</p>
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
    print(" * Running application...")
    print(" * Serving application at http://172.20.10.5:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
