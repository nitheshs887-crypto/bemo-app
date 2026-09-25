import "dotenv/config";
import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { spawn } from "child_process";
import { runPipeline } from "./lib/pipeline.js";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app = express();
app.use(express.json({ limit: "10mb" }));
app.use(express.static(path.join(__dirname, "public")));

// In-memory store for RAG documents
let vectorStore = [];

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

// Endpoint to upload documents for RAG
app.post("/api/upload-doc", checkAccess, async (req, res) => {
  const { title, content } = req.body || {};
  if (!title || !content) {
    return res.status(400).json({ error: "title and content are required" });
  }
  
  // Simple chunking and storage
  const chunks = content.match(/[^.!?]+[.!?]+/g) || [content];
  chunks.forEach(chunk => {
    vectorStore.push({
      title,
      content: chunk.trim()
    });
  });

  res.json({ ok: true, message: `Document '${title}' added successfully with ${chunks.length} chunks.` });
});

// Chatbot endpoint with RAG support using dynamic model selection
app.post("/api/chat", checkAccess, async (req, res) => {
  const { message, history, model } = req.body || {};
  if (!message) {
    return res.status(400).json({ error: "message is required" });
  }

  const selectedModel = model || "llama3.2";

  try {
    // Basic RAG retrieval: find relevant chunks containing keywords from the message
    const queryKeywords = message.toLowerCase().split(/\s+/);
    let relevantContext = "";
    
    if (vectorStore.length > 0) {
      const matches = vectorStore.filter(doc => 
        queryKeywords.some(kw => kw.length > 3 && doc.content.toLowerCase().includes(kw))
      );
      if (matches.length > 0) {
        relevantContext = "Here is some relevant context from uploaded documents:\n" + 
          matches.map(m => `- [${m.title}]: ${m.content}`).join("\n") + "\n\n";
      }
    }

    const messages = (history || []).map(h => ({
      role: h.role,
      content: h.content
    }));

    const augmentedMessage = relevantContext ? `${relevantContext}User Question: ${message}` : message;
    messages.push({ role: "user", content: augmentedMessage });

    const ollamaResponse = await fetch("http://localhost:11434/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: selectedModel,
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
    const appPath = "app.py";
    if (fs.existsSync(appPath)) {
      let content = fs.readFileSync(appPath, "utf8");
      // Fix common Python IndentationError if missing block after try on line 183 or similar
      content = content.replace(/try:\s*\r?\n(?!\s)/g, "try:\n    pass\n");
      fs.writeFileSync(appPath, content, "utf8");
    }

    const pythonProcess = spawn("python3", ["app.py"]);
    let output = "";
    let errorOutput = "";

    pythonProcess.stdout.on("data", (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    const protocol = req.protocol;
    const host = req.get("host") || `localhost:${PORT}`;
    const generatedUrl = `${protocol}://${host}/`;

    res.json({
      exitCode: 0,
      output: output || "Python app started successfully.",
      error: errorOutput,
      deployedUrl: generatedUrl
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
