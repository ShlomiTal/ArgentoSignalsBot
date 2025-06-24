import React, { useEffect, useState } from 'react';
import { Line } from 'recharts';
import { LineChart, XAxis, YAxis, Tooltip } from 'recharts';
import { useTranslation } from '../hooks/useLanguage';
import '../styles/theme.css';

const PerformanceDashboard = () => {
  const { t } = useTranslation();
  const [data, setData] = useState([]);

  useEffect(() => {
    // דוגמה - שליפת נתונים מה-API
    setData([
      { date: '2025-06-01', performance: 0.85 },
      { date: '2025-06-02', performance: 0.88 },
      { date: '2025-06-03', performance: 0.90 },
    ]);
  }, []);

  return (
    <div className="performance-dashboard">
      <h2>{t('performance')}</h2>
      <LineChart width={600} height={300} data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="performance" stroke="#FFD700" />
      </LineChart>
    </div>
  );
};

export default PerformanceDashboard;