import React from 'react';
import { useTranslation } from '../hooks/useLanguage';
import '../styles/theme.css';

const SignalCard = ({ signal }) => {
  const { t } = useTranslation();
  const { asset, price, confidence, timestamp } = signal;

  return (
    <div className="signal-card">
      <h3>{asset}</h3>
      <p>{t('price')}: ${price}</p>
      <p>{t('confidence')}: {(confidence * 100).toFixed(2)}%</p>
      <p>{t('time')}: {new Date(timestamp).toLocaleString()}</p>
    </div>
  );
};

export default SignalCard;