import "dotenv/config";
import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { spawn } from "child_process";
import { runPipeline } from "./lib/pipeline.js";
import fs from "fs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const app =
