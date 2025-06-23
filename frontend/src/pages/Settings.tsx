import React, { useState } from 'react';
import { t } from '../i18n';

export const Settings: React.FC = () => {
  const [message, setMessage] = useState('');
  const [schedule, setSchedule] = useState('09:00');
  const [trustLevel, setTrustLevel] = useState(70);
  const [pair, setPair] = useState('');
  const [pairs, setPairs] = useState<string[]>([]);

  const handleAddPair = () => {
    if (pair) setPairs([...pairs, pair]);
    setPair('');
  };

  return (
    <div className="p-4 text-white">
      <h1 className="text-2xl font-bold mb-4">Settings</h1>
      <div className="space-y-4">
        <div>
          <label className="block">{t('message')}:</label>
          <textarea value={message} onChange={e => setMessage(e.target.value)} className="w-full p-2 rounded bg-gray-800 border border-gray-600" />
        </div>
        <div>
          <label className="block">{t('schedule')}:</label>
          <input type="time" value={schedule} onChange={e => setSchedule(e.target.value)} className="w-full p-2 rounded bg-gray-800 border border-gray-600" />
        </div>
        <div>
          <label className="block">{t('trustLevel')}:</label>
          <input type="number" value={trustLevel} min={0} max={100} onChange={e => setTrustLevel(Number(e.target.value))} className="w-full p-2 rounded bg-gray-800 border border-gray-600" />
        </div>
        <div>
          <label className="block">{t('addPair')}:</label>
          <div className="flex gap-2">
            <input type="text" value={pair} onChange={e => setPair(e.target.value)} className="flex-1 p-2 rounded bg-gray-800 border border-gray-600" />
            <button onClick={handleAddPair} className="bg-purple-700 px-4 py-2 rounded">Add</button>
          </div>
          <ul className="mt-2 list-disc ml-5">
            {pairs.map((p, i) => <li key={i}>{p}</li>)}
          </ul>
        </div>
      </div>
    </div>
  );
};