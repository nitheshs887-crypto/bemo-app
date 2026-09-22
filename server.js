import "dotenv/config";
import express from "express";
import path from "path";
import { fileURLToPath } from "url";
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
  if (!process.env.ANTHROPIC_API_KEY) {
    return res.status(500).json({ error: "ANTHROPIC_API_KEY is not set on the server" });
  }
  try {
    const result = await runPipeline({ repoUrl, token, branch, command, deployHookUrl });
    res.json(result);
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

const PORT = process.env.PORT || 3000;
const HOST = process.env.HOST || "0.0.0.0";
app.listen(PORT, HOST, () => {
  console.log(`Build agent listening on http://${HOST}:${PORT}`);
  console.log(`Access from Android emulator: http://10.0.2.2:${PORT}`);
});
