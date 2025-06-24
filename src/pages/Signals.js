import React, { useEffect } from 'react';
import SignalCard from '../components/SignalCard';
import { useSignals } from '../hooks/useSignals';
import '../styles/global.css';

const Signals = () => {
  const { signals, fetchSignals } = useSignals();

  useEffect(() => {
    fetchSignals();
    const interval = setInterval(fetchSignals, 30 * 60 * 1000); // כל 30 דקות
    return () => clearInterval(interval);
  }, [fetchSignals]);

  return (
    <div className="signals-page">
      <h1>Signals Dashboard</h1>
      <div className="signal-list">
        {signals.map((signal) => (
          <SignalCard key={signal.id} signal={signal} />
        ))}
      </div>
    </div>
  );
};

export default Signals;