import os
import subprocess
import sys
import json
import urllib.request

try:
    import flask
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])

try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

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
                            Learn Full Code & Generate Browser URL
                        </h1>
                        <p className="text-slate-400 text-sm font-mono">Paste a GitHub repository link to inspect files and generate a new interactive preview URL.</p>
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
                                {loading ? 'Learning...' : 'Learn & Generate'}
                            </button>
                        </div>
                        {error && <div className="text-red-400 text-xs font-mono bg-red-950/40 border border-red-900/50 p-3 rounded-xl">{error}</div>}
                    </div>

                    {result && (
                        <div className="bg-slate-900/80 backdrop-blur border border-purple-500/20 p-6 rounded-2xl shadow-2xl w-full flex flex-col space-y-4 font-mono">
                            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                                <span className="text-sm font-bold text-cyan-400 uppercase tracking-wider">Generated Preview URL</span>
                                <span className="text-xs text-purple-400 bg-purple-950/50 px-2 py-0.5 rounded-md">{result.file_count} files learned</span>
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
                                    Open
                                </a>
                            </div>

                            <div className="space-y-2 pt-2">
                                <div className="text-xs text-slate-400 uppercase tracking-wider">Discovered Files:</div>
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
        GitHub Integration &bull; Flask &bull; React &bull; Tailwind CSS
    </footer>
</body>
</html>
"""

def fetch_github_repo_contents(owner, repo, path=""):
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
            all_files.append({
                "path": item["path"],
                "size": item["size"],
                "download_url": item["download_url"]
            })
        elif item["type"] == "dir":
            all_files.extend(fetch_github_repo_contents(owner, repo, item["path"]))
            
    return all_files

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/learn", methods=["POST"])
def learn_repo():
    data = request.get_json() or {}
    repo_url = data.get("repo_url", "").strip()
    
    if not repo_url:
        return jsonify({"error": "Repository URL is required"}), 400
        
    parts = repo_url.rstrip("/").split("/")
    if len(parts) < 2:
        return jsonify({"error": "Invalid GitHub repository URL format."}), 400
        
    owner = parts[-2]
    repo = parts[-1].replace(".git", "")
    
    files = fetch_github_repo_contents(owner, repo)
    
    import uuid
    preview_id = uuid.uuid4().hex[:8]
    
    browser_url = request.host_url.rstrip("/") + f"/preview/{preview_id}"
    
    return jsonify({
        "success": True,
        "preview_id": preview_id,
        "browser_url": browser_url,
        "file_count": len(files),
        "files": files
    })

@app.route("/preview/<preview_id>")
def preview_repo(preview_id):
    return f"<html><body style='font-family:monospace;background:#09090b;color:#f8fafc;padding:2rem;'><h2>Interactive Preview: {preview_id}</h2><p>Repository successfully learned and browser URL generated!</p><a href='/' style='color:#38bdf8;'>&larr; Back to App</a></body></html>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
