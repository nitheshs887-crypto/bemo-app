import os
import subprocess
import sys

try:
    import flask
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])

from flask import Flask, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cyberpunk Dark Dashboard</title>
    <!-- Load React, ReactDOM, and Babel for in-browser JSX transformation -->
    <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 flex items-center justify-center h-screen">
    <div id="root"></div>

    <script type="text/babel">
        function App() {
            const [count, setCount] = React.useState(42);
            const [text, setText] = React.useState('');

            return (
                <div className="bg-slate-900/80 backdrop-blur-xl p-8 rounded-2xl shadow-[0_0_50px_rgba(6,182,212,0.15)] w-96 text-center border border-cyan-500/30">
                    <h1 className="text-3xl font-extrabold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-fuchsia-500">Cyber Dashboard</h1>
                    <p className="text-slate-400 mb-6 text-sm">Next-gen React interface via Flask</p>
                    
                    <div className="mb-6 bg-slate-800/50 p-4 rounded-xl border border-cyan-500/20">
                        <p className="text-xs text-cyan-400 font-semibold uppercase tracking-wider mb-1">System Core Status</p>
                        <p className="text-3xl font-mono font-bold text-cyan-200 mb-3">{count}</p>
                        <div className="flex justify-center gap-2">
                            <button 
                                onClick={() => setCount(count - 1)}
                                className="bg-rose-600/80 hover:bg-rose-600 text-white font-bold py-2 px-3 rounded-lg shadow transition transform active:scale-95 border border-rose-500/50"
                            >
                                -
                            </button>
                            <button 
                                onClick={() => setCount(count + 1)}
                                className="bg-cyan-600/80 hover:bg-cyan-600 text-white font-bold py-2 px-6 rounded-lg shadow transition transform active:scale-95 border border-cyan-500/50 font-mono text-sm"
                            >
                                OVERLOAD
                            </button>
                        </div>
                    </div>

                    <div>
                        <input 
                            type="text" 
                            placeholder="Enter command..." 
                            value={text} 
                            onChange={(e) => setText(e.target.value)}
                            className="border border-slate-700 bg-slate-950 p-3 rounded-xl w-full mb-3 focus:outline-none focus:ring-2 focus:ring-fuchsia-500 text-sm text-slate-200 transition"
                        />
                        <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 text-left">
                            <span className="text-xs text-fuchsia-400 block uppercase font-mono font-bold">Terminal Output</span>
                            <p className="text-slate-300 font-mono text-sm truncate">{text || <span className="text-slate-600 italic">Waiting for input...</span>}</p>
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
    print(" * Running on http://127.0.0.1:5000")
    print(" * Deployed URL: https://preview-5000.app.internal.domain")
    app.run(host="0.0.0.0", port=5000, debug=False)
