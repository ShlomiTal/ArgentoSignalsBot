import React, { useEffect, useState } from 'react';
import { SignalCard } from './components/SignalCard';
import { Settings } from './pages/Settings';

function App() {
  const [signalData, setSignalData] = useState<any>(null);
  const [page, setPage] = useState<'signals' | 'settings'>('signals');

  useEffect(() => {
    fetch('/api/signal?symbol=BTC/USD')
      .then(res => res.json())
      .then(data => setSignalData(data));
  }, []);

  return (
    <div className="p-4">
      <div className="flex justify-between mb-4">
        <button onClick={() => setPage('signals')} className="bg-slate-700 px-4 py-2 rounded">Signals</button>
        <button onClick={() => setPage('settings')} className="bg-slate-700 px-4 py-2 rounded">Settings</button>
      </div>
      {page === 'signals' && signalData ? (
        <SignalCard
          symbol={signalData.symbol}
          signal={signalData.signal}
          confidence={signalData.confidence}
          price={signalData.price}
        />
      ) : (
        <Settings />
      )}
    </div>
  );
}

export default App;