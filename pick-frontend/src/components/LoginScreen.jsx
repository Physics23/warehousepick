import { useState } from 'react';

export default function LoginScreen({ onLogin, error }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <div className="login-screen">
      <h1>Warehouse Kiosk Login</h1>
      <form onSubmit={(e) => { e.preventDefault(); onLogin(username, password); }}>
        <input type="text" placeholder="Operator Username" value={username} onChange={(e) => setUsername(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Sign In</button>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}