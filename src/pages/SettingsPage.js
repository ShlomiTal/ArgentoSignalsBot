import React from 'react';
import Settings from '../components/Settings';
import '../styles/global.css';

const SettingsPage = () => {
  return (
    <div className="settings-page">
      <h1>Settings</h1>
      <Settings />
    </div>
  );
};

export default SettingsPage;