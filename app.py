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
    <title>Modern React Dashboard</title>
    <!-- Load React, ReactDOM, and Babel for in-browser JSX transformation -->
    <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center h-screen">
    <div id="root"></div>

    <script type="text/babel">
        function App() {
            const [count, setCount] = React.useState(0);
            const [text, setText] = React.useState('');

            return (
                <div className="bg-white/90 backdrop-blur-md p-8 rounded-2xl shadow-2xl w-96 text-center border border-white/20">
                    <h1 className="text-3xl font-extrabold mb-2 text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">Dashboard UI</h1>
                    <p className="text-gray-500 mb-6 text-sm">Enhanced React app powered by Flask</p>
                    
                    <div className="mb-6 bg-indigo-50 p-4 rounded-xl border border-indigo-100">
                        <p className="text-sm text-indigo-600 font-semibold uppercase tracking-wider mb-1">Counter State</p>
                        <p className="text-3xl font-bold text-indigo-900 mb-3">{count}</p>
                        <div className="flex justify-center gap-2">
                            <button 
                                onClick={() => setCount(count - 1)}
                                className="bg-rose-500 hover:bg-rose-600 text-white font-bold py-2 px-3 rounded-lg shadow transition transform active:scale-95"
                            >
                                -
                            </button>
                            <button 
                                onClick={() => setCount(count + 1)}
                                className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-lg shadow transition transform active:scale-95"
                            >
                                Increment
                            </button>
                        </div>
                    </div>

                    <div>
                        <input 
                            type="text" 
                            placeholder="Type something here..." 
                            value={text} 
                            onChange={(e) => setText(e.target.value)}
                            className="border border-gray-300 bg-gray-50 p-3 rounded-xl w-full mb-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm transition"
                        />
                        <div className="bg-gray-50 p-3 rounded-xl border border-gray-200 text-left">
                            <span className="text-xs text-gray-400 block uppercase font-bold">Live Output</span>
                            <p className="text-gray-800 font-medium truncate">{text || <span className="text-gray-400 italic">Nothing typed yet...</span>}</p>
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
    app.run(host="0.0.0.0", port=5000, debug=False)
