import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [status, setStatus] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('Generating script...');
    setResponse('');
    try {
      const res = await axios.post('http://localhost:5000/api/generate', { prompt });
      setResponse(res.data.script);
      setStatus('');
    } catch (err) {
      setStatus('Error generating script.');
    }
  };

  return (
    <div className="app">
      <h1 className="title">doomteach</h1>
      <form onSubmit={handleSubmit} className="prompt-form">
        <input
          type="text"
          placeholder="Enter your prompt..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
      {status && <p className="response">{status}</p>}
      {response && (
        <div className="response">
          <strong>Script:</strong>
          <pre style={{whiteSpace: 'pre-wrap'}}>{response}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
