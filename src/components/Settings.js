import React, { useState, useEffect } from 'react';
import { useTranslation } from '../hooks/useLanguage';
import { updateSettings, sendTestMessage } from '../utils/api';
import '../styles/theme.css';

const Settings = () => {
  const { t, setLang, lang } = useTranslation();
  const [form, setForm] = useState({
    tradingPairs: [],
    confidenceThreshold: 0.8,
    telegramMessage: '',
    schedule: '09:00',
  });

  useEffect(() => {
    // שליפת הגדרות ראשוניות מה-API
    // זמנית - דוגמה
    setForm({
      tradingPairs: ['BTC/USD', 'ETH/USD'],
      confidenceThreshold: 0.8,
      telegramMessage: 'New Signal: {asset} at {price}',
      schedule: '09:00',
    });
  }, []);

  const handleSave = async () => {
    await updateSettings(form);
    alert(t('save_success'));
  };

  const handleTestMessage = async () => {
    await sendTestMessage(form.telegramMessage);
    alert('Test message sent!');
  };

  return (
    <div className="settings">
      <h2>{t('settings')}</h2>
      <label>{t('language')}</label>
      <select value={lang} onChange={(e) => setLang(e.target.value)}>
        <option value="en">English</option>
        <option value="he">עברית</option>
      </select>
      <label>{t('trading_pairs')}</label>
      <input
        type="text"
        value={form.tradingPairs.join(',')}
        onChange={(e) => setForm({ ...form, tradingPairs: e.target.value.split(',') })}
      />
      <label>{t('confidence_threshold')}</label>
      <input
        type="number"
        value={form.confidenceThreshold}
        onChange={(e) => setForm({ ...form, confidenceThreshold: +e.target.value })}
        step="0.1"
        min="0"
        max="1"
      />
      <label>{t('telegram_message')}</label>
      <textarea
        value={form.telegramMessage}
        onChange={(e) => setForm({ ...form, telegramMessage: e.target.value })}
      />
      <label>{t('schedule')}</label>
      <input
        type="time"
        value={form.schedule}
        onChange={(e) => setForm({ ...form, schedule: e.target.value })}
      />
      <button onClick={handleSave}>{t('save')}</button>
      <button onClick={handleTestMessage}>{t('test_message')}</button>
    </div>
  );
};

export default Settings;