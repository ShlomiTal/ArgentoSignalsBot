const API_BASE_URL = 'http://localhost:8080/api';

export const getSignals = async () => {
  const response = await fetch(`${API_BASE_URL}/signals`);
  return response.json();
};

export const updateSettings = async (settings) => {
  const response = await fetch(`${API_BASE_URL}/settings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(settings),
  });
  return response.json();
};

export const sendTestMessage = async (message) => {
  const response = await fetch(`${API_BASE_URL}/signals/test`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message }),
  });
  return response.json();
};