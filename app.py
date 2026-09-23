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
    <title>React.js User Interface</title>
    <!-- Load React, ReactDOM, and Babel for in-browser JSX transformation -->
    <script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <!-- Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
    <div id="root"></div>

    <script type="text/babel">
        function App() {
            const [count, setCount] = React.useState(0);
            const [text, setText] = React.useState('');

            return (
                <div className="bg-white p-8 rounded-lg shadow-md w-96 text-center">
                    <h1 className="text-2xl font-bold mb-4 text-gray-800">React.js User Interface</h1>
                    <p className="text-gray-600 mb-6">Interactive component running inside Flask</p>
                    
                    <div className="mb-6">
                        <p className="text-xl font-semibold mb-2">Count: {count}</p>
                        <button 
                            onClick={() => setCount(count + 1)}
                            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded transition"
                        >
                            Increment
                        </button>
                    </div>

                    <div>
                        <input 
                            type="text" 
                            placeholder="Type something..." 
                            value={text} 
                            onChange={(e) => setText(e.target.value)}
                            className="border border-gray-300 p-2 rounded w-full mb-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <p className="text-gray-700">You typed: <span className="font-medium">{text}</span></p>
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
