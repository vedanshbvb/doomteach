import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await axios.post('http://localhost:5000/api/prompt', { prompt });
    setResponse(res.data.response);
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
      {response && <p className="response">{response}</p>}
    </div>
  );
}

export default App;
