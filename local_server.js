import express from 'express';
import dotenv from 'dotenv';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import interpretHandler from './api/interpret.js';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static(__dirname));

// Mock Vercel Request/Response for the handler
app.post('/api/interpret', async (req, res) => {
    // Vercel handlers expect (req, res), express provides them similarly but we need to ensure compatibility
    // interpreting handler uses res.status().json() which express supports.
    try {
        await interpretHandler(req, res);
    } catch (error) {
        console.error("Handler error:", error);
        res.status(500).json({ error: "Internal Server Error" });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
