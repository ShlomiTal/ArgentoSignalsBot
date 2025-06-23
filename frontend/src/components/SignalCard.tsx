import React from 'react';

interface Props {
  symbol: string;
  signal: string;
  confidence: number;
  price: number;
}

export const SignalCard: React.FC<Props> = ({ symbol, signal, confidence, price }) => (
  <div className="rounded-2xl shadow p-4 border border-gray-700 bg-black text-white">
    <h2 className="text-xl font-bold">{symbol}</h2>
    <p className="mt-2">Signal: <strong>{signal}</strong></p>
    <p>Confidence: {confidence}%</p>
    <p>Price: ${price}</p>
  </div>
);