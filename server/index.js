const express = require('express');
const cors = require('cors');

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

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
