import React from 'react';
import PerformanceDashboard from '../components/PerformanceDashboard';
import SignalCard from '../components/SignalCard';
import { useSignals } from '../hooks/useSignals';
import '../styles/global.css';

const Home = () => {
  const { signals } = useSignals();

  return (
    <div className="home-page">
      <h1>Argento Dashboard</h1>
      <PerformanceDashboard />
      <h2>Latest Signals</h2>
      <div className="signal-list">
        {signals.slice(0, 3).map((signal) => (
          <SignalCard key={signal.id} signal={signal} />
        ))}
      </div>
    </div>
  );
};

export default Home;