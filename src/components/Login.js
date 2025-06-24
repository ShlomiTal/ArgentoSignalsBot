import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';

const Login = () => {
  const [password, setPassword] = useState('');
  const { login, error } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    login(password);
  };

  return (
    <div className="login-page">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Enter password"
        />
        <button type="submit">Login</button>
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    );
  };
};


export default Login;
