import "dotenv/config";
import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { spawn } from "child_process";
import { runPipeline } from "./lib/pipeline.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
app.use(express.json({ limit: "1mb" }));
app.use(express.static(path.join(__dirname, "public")));

function checkAccess(req, res, next) {
  const required = process.env.APP_ACCESS_KEY;
  if (!required) return next(); // no key configured — fine for local-only use
  if (req.header("x-access-key") === required) return next();
  return res.status(401).json({ error: "unauthorized" });
}

app.post("/api/run", checkAccess, async (req, res) => {
  const { repoUrl, token, branch, command, deployHookUrl } = req.body || {};
  if (!repoUrl || !token || !command) {
    return res.status(400).json({ error: "repoUrl, token, and command are required" });
  }
  try {
    const result = await runPipeline({ repoUrl, token, branch, command, deployHookUrl });
    res.json(result);
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

// Chatbot endpoint using local Ollama with llama3.2
app.post("/api/chat", checkAccess, async (req, res) => {
  const { message, history } = req.body || {};
  if (!message) {
    return res.status(400).json({ error: "message is required" });
  }

  try {
    const messages = (history || []).map(h => ({
      role: h.role,
      content: h.content
    }));
    messages.push({ role: "user", content: message });

    const ollamaResponse = await fetch("http://localhost:11434/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "llama3.2",
        messages: messages,
        stream: false
      })
    });

    if (!ollamaResponse.ok) {
      const errText = await ollamaResponse.text();
      return res.status(500).json({ error: `Ollama error: ${errText}` });
    }

    const data = await ollamaResponse.json();
    const reply = data.message?.content || "";
    res.json({ reply });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

// Optional: after a deploy, poll whether the live site is responding.
app.get("/api/check-site", checkAccess, async (req, res) => {
  const { url } = req.query;
  if (!url) return res.status(400).json({ error: "url query param required" });
  try {
    const r = await fetch(url, { method: "GET" });
    res.json({ reachable: true, status: r.status });
  } catch (e) {
    res.json({ reachable: false, error: e.message });
  }
});

app.post("/api/run-app", checkAccess, async (req, res) => {
  try {
    const pythonProcess = spawn("python3", ["app.py"]);
    let output = "";
    let errorOutput = "";

    pythonProcess.stdout.on("data", (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on("close", (code) => {
      res.json({
        exitCode: code,
        output: errorOutput ? errorOutput : output,
        error: errorOutput,
        deployedUrl: "http://localhost:5000"
      });
    });
  } catch (e) {
    res.status(500).json({ ok: false, error: e.message });
  }
});

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || "0.0.0.0";
app.listen(PORT, HOST, () => {
  console.log(`Build agent listening on http://localhost:${PORT}`);
  console.log(`Access from Android emulator: http://10.0.2.2:${PORT}`);
});
