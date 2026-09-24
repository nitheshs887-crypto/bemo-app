import os
import subprocess
import sys
import json
import uuid
import tempfile
import threading
import socket
import urllib.request

try:
    import flask
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

from flask import Flask, render_template_string, request, jsonify, redirect
import requests

app = Flask(__name__)

# Global dictionary to store running preview instances: preview_id -> {url, port, process, thread, files}
active_previews = {}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Code Learner & Browser URL Generator</title>
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
            const [repoUrl, setRepoUrl] = React.useState('');
            const [loading, setLoading] = React.useState(false);
            const [result, setResult] = React.useState(null);
            const [error, setError] = React.useState('');

            const handleLearn = async () => {
                if (!repoUrl.trim()) {
                    setError('Please enter a GitHub repository URL.');
                    return;
                }
                setError('');
                setLoading(true);
                setResult(null);

                try {
                    const response = await fetch('/api/learn', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ repo_url: repoUrl })
                    });
                    const data = await response.json();
                    if (!response.ok) {
                        throw new Error(data.error || 'Failed to process repository.');
                    }
                    setResult(data);
                } catch (err) {
                    setError(err.message);
                } finally {
                    setLoading(false);
                }
            };

            return (
                <div className="flex flex-col items-center justify-center max-w-2xl mx-auto w-full space-y-6">
                    <div className="text-center space-y-2">
                        <span className="bg-purple-500/10 border border-purple-500/30 text-purple-400 text-xs font-mono px-3 py-1 rounded-full uppercase tracking-widest">GitHub Integration</span>
                        <h1 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 font-mono">
                            Learn Full Code & Run to Give URL
                        </h1>
                        <p className="text-slate-400 text-sm font-mono">Paste a GitHub repository link to read full files, run the application, and generate a live browser URL.</p>
                    </div>
                    
                    <div className="bg-slate-900/80 backdrop-blur border border-purple-500/20 p-6 rounded-2xl shadow-2xl w-full flex flex-col space-y-4">
                        <div className="flex space-x-2">
                            <input 
                                type="text" 
                                placeholder="https://github.com/username/repository" 
                                value={repoUrl} 
                                onChange={(e) => setRepoUrl(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleLearn()}
                                className="flex-1 bg-slate-950 border border-slate-700 p-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 text-slate-200 font-mono text-sm"
                            />
                            <button 
                                onClick={handleLearn}
                                disabled={loading}
                                className="bg-gradient-to-r from-cyan-600 to-purple-600 hover:from-cyan-500 hover:to-purple-500 text-white font-mono font-bold px-6 rounded-xl shadow-lg shadow-purple-900/30 transition disabled:opacity-50"
                            >
                                {loading ? 'Running...' : 'Run & Get URL'}
                            </button>
                        </div>
                        {error && <div className="text-red-400 text-xs font-mono bg-red-950/40 border border-red-900/50 p-3 rounded-xl">{error}</div>}
                    </div>

                    {result && (
                        <div className="bg-slate-900/80 backdrop-blur border border-purple-500/20 p-6 rounded-2xl shadow-2xl w-full flex flex-col space-y-4 font-mono">
                            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                                <span className="text-sm font-bold text-cyan-400 uppercase tracking-wider">Live Execution URL</span>
                                <span className="text-xs text-purple-400 bg-purple-950/50 px-2 py-0.5 rounded-md">{result.file_count} files read & run</span>
                            </div>
                            <div className="flex items-center space-x-2">
                                <input 
                                    type="text" 
                                    readOnly 
                                    value={result.browser_url} 
                                    className="flex-1 bg-slate-950 border border-slate-700 p-2.5 rounded-xl text-cyan-300 text-xs font-mono select-all"
                                />
                                <a 
                                    href={result.browser_url} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="bg-purple-600 hover:bg-purple-500 text-white font-bold px-4 py-2.5 rounded-xl text-xs transition inline-flex items-center"
                                >
                                    Open App
                                </a>
                            </div>

                            <div className="space-y-2 pt-2">
                                <div className="text-xs text-slate-400 uppercase tracking-wider">Read Files & Execution Log:</div>
                                <div className="max-h-48 overflow-y-auto space-y-1.5 pr-1">
                                    {result.files.map((file, index) => (
                                        <div key={index} className="bg-slate-950/60 border border-slate-800/80 px-3 py-2 rounded-lg text-xs text-slate-300 flex items-center justify-between">
                                            <span className="truncate">{file.path}</span>
                                            <span className="text-purple-400 text-[10px] ml-2">{file.size} bytes</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            );
        }

        ReactDOM.createRoot(document.getElementById('root')).render(<App />);
    </script>
    <footer className="text-center py-4 text-xs font-mono text-slate-500">
        GitHub Full Code Reader &bull; Flask &bull; React &bull; Tailwind CSS
    </footer>
</body>
</html>
"""

def fetch_github_repo_contents_with_content(owner, repo, path=""):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    response = requests.get(api_url, headers=headers)
    if response.status_code != 200:
        return []
    
    items = response.json()
    all_files = []
    
    if isinstance(items, dict):
        items = [items]
        
    for item in items:
        if item["type"] == "file":
            file_data = {
                "path": item["path"],
                "size": item["size"],
                "download_url": item["download_url"],
                "content": ""
            }
            if item["download_url"]:
                try:
                    res = requests.get(item["download_url"])
                    if res.status_code == 200:
                        file_data["content"] = res.text
                except Exception:
                    pass
            all_files.append(file_data)
        elif item["type"] == "dir":
            all_files.extend(fetch_github_repo_contents_with_content(owner, repo, item["path"]))
            
    return all_files

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/learn', methods=['POST'])
def api_learn():
    data = request.json or {}
    repo_url = data.get('repo_url', '').strip()
    
    if not repo_url:
        return jsonify({"error": "Repository URL is required."}), 400
        
    # Parse github url
    clean_url = repo_url.rstrip('/')
    if clean_url.endswith('.git'):
        clean_url = clean_url[:-4]
        
    parts = clean_url.split('/')
    if len(parts) < 2:
        return jsonify({"error": "Invalid GitHub repository URL format."}), 400
        
    owner = parts[-2]
    repo = parts[-1]
    
    files = fetch_github_repo_contents_with_content(owner, repo)
    if not files:
        return jsonify({"error": "Could not fetch files from GitHub repository or repository is empty."}), 404
        
    # Create temp directory and write files
    temp_dir = tempfile.mkdtemp(prefix="gh_preview_")
    for file_info in files:
        file_path = os.path.join(temp_dir, file_info["path"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8", errors="ignore") as f:
            f.write(file_info["content"])
            
    # Look for an entrypoint script (app.py, main.py, server.py, index.js, etc.)
    entry_script = None
    candidates = ["app.py", "main.py", "server.py", "run.py", "index.py"]
    for c in candidates:
        if os.path.exists(os.path.join(temp_dir, c)):
            entry_script = c
            break
            
    if not entry_script:
        # search recursively or pick first python file
        for root, dirs, filenames in os.walk(temp_dir):
            for fn in filenames:
                if fn.endswith('.py'):
                    entry_script = os.path.relpath(os.path.join(root, fn), temp_dir)
                    break
            if entry_script:
                break
                
    preview_id = str(uuid.uuid4())[:8]
    port = find_free_port()
    
    process = None
    if entry_script:
        script_full_
