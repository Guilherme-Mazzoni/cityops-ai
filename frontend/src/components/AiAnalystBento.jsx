import { useState } from 'react';

export default function AiAnalystBento() {
  const [messages, setMessages] = useState([
    { role: 'system', content: 'System Initialized. RAG Vector Database connected. Awaiting query...' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    
    const userQuery = input;
    setMessages(prev => [...prev, { role: 'user', content: userQuery }]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/ask-analyst', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userQuery })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'system', content: data.answer || 'Error: No response generated.' }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'system', content: 'Connection Error: Failed to reach backend API.' }]);
    }
    setLoading(false);
  };

  return (
    <div className="bento-item col-span-8 row-span-2">
      <h2 className="widget-title">Intelligence Terminal (RAG)</h2>
      
      <div className="chat-container">
        <div className="chat-history">
          {messages.map((msg, idx) => (
            <div key={idx} className={`chat-message ${msg.role === 'user' ? 'message-user' : 'message-system'}`}>
              {msg.content}
            </div>
          ))}
          {loading && (
            <div className="chat-message message-system">
              Processing Context Vectors...
            </div>
          )}
        </div>
        
        <form className="chat-input-area" onSubmit={handleSend}>
          <input 
            type="text" 
            className="form-input" 
            placeholder="Input query for RAG analysis..." 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button type="submit" className="btn-primary" disabled={loading || !input.trim()}>
            Send Query
          </button>
        </form>
      </div>
    </div>
  );
}
