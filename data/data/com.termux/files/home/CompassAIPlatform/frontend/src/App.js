import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [protectedData, setProtectedData] = useState('');
  const [token, setToken] = useState(localStorage.getItem('jwtToken') || '');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [wsMessage, setWsMessage] = useState('');
  const [wsResponse, setWsResponse] = useState('');
  const [ws, setWs] = useState(null);

  useEffect(() => {
    // Test basic backend connection
    fetch('/api')
      .then(res => res.text())
      .then(data => setMessage(data))
      .catch(err => console.error('Error fetching from backend:', err));

    // WebSocket setup
    const websocket = new WebSocket('ws://localhost:3000'); // Adjust if backend is on different port/host
    websocket.onopen = () => {
      console.log('WebSocket Connected');
      setWs(websocket);
    };
    websocket.onmessage = (event) => {
      setWsResponse(event.data);
    };
    websocket.onclose = () => {
      console.log('WebSocket Disconnected');
    };
    websocket.onerror = (error) => {
      console.error('WebSocket Error:', error);
    };

    return () => {
      if (websocket.readyState === WebSocket.OPEN) {
        websocket.close();
      }
    };
  }, []);

  const handleLogin = async () => {
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.json();
      if (response.ok) {
        setToken(data.token);
        localStorage.setItem('jwtToken', data.token);
        alert('Login successful!');
      } else {
        alert(data || 'Login failed.');
      }
    } catch (error) {
      console.error('Login error:', error);
      alert('Login failed due to network error.');
    }
  };

  const handleRegister = async () => {
    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });
      const data = await response.text();
      if (response.ok) {
        alert(data);
      } else {
        alert(data || 'Registration failed.');
      }
    } catch (error) {
      console.error('Registration error:', error);
      alert('Registration failed due to network error.');
    }
  };

  const fetchProtectedData = async () => {
    if (!token) {
      alert('Please log in first.');
      return;
    }
    try {
      const response = await fetch('/api/protected', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      const data = await response.json();
      if (response.ok) {
        setProtectedData(data.message);
      } else {
        setProtectedData(data.message || 'Failed to fetch protected data.');
      }
    } catch (error) {
      console.error('Protected data fetch error:', error);
      setProtectedData('Failed to fetch protected data due to network error.');
    }
  };

  const sendWsMessage = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(wsMessage);
    } else {
      alert('WebSocket is not connected.');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Compass AI Platform</h1>
        <p>{message}</p>

        <h2>Authentication</h2>
        <div>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
          <button onClick={handleRegister}>Register</button>
        </div>

        <h2>Protected Data</h2>
        <button onClick={fetchProtectedData}>Fetch Protected Data</button>
        <p>{protectedData}</p>

        <h2>WebSocket Communication</h2>
        <div>
          <input
            type="text"
            placeholder="Send message via WS"
            value={wsMessage}
            onChange={(e) => setWsMessage(e.target.value)}
          />
          <button onClick={sendWsMessage}>Send WS Message</button>
          <p>WS Response: {wsResponse}</p>
        </div>

        {/* Placeholder for gRPC interaction - typically client-side gRPC is more complex */}
        <h2>gRPC (Client-side not directly implemented in browser)</h2>
        <p>gRPC client-side interaction usually requires a proxy or specific libraries not directly available in standard browser environments. This is handled on the backend.</p>
      </header>
    </div>
  );
}

export default App;