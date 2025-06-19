const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const fs = require('fs');

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

app.post('/api/prompt', (req, res) => {
  const { prompt } = req.body;
  console.log("User prompt:", prompt);
  // Replace this with actual ChatGPT API logic if needed
  res.json({ response: `You said: ${prompt}` });
});

app.post('/api/generate', (req, res) => {
  const { prompt } = req.body;
  if (!prompt) {
    return res.status(400).json({ error: 'Prompt is required' });
  }

  // Call the new ADK agent pipeline
  const py = spawn('python3', [
    './run_pipeline.py',
    prompt
  ], { cwd: __dirname + '/..' });

  let output = '';
  let statusUpdates = [];
  let logContent = '';

  py.stdout.on('data', (data) => {
    const lines = data.toString().split('\n');
    lines.forEach(line => {
      if (line.startsWith('STATUS:')) {
        statusUpdates.push(line.replace('STATUS:', '').trim());
      } else {
        output += line + '\n';
      }
    });
  });

  py.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  py.on('close', (code) => {
    console.log(`Child process exited with code ${code}`);
    
    // Read the log file
    const logPath = __dirname + '/../run_pipeline.log';
    
    try {
      if (fs.existsSync(logPath)) {
        logContent = fs.readFileSync(logPath, 'utf8');
      }
    } catch (err) {
      console.error('Error reading log file:', err);
    }

    res.json({
      success: code === 0,
      output: output,
      statusUpdates: statusUpdates,
      logContent: logContent,
      exitCode: code
    });
  });
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
