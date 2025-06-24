const generateBacktestResults = async (asset, startDate, endDate) => {
  // דוגמה - יושם עם לוגיקה אמיתית
  return {
    asset,
    startDate,
    endDate,
    performance: 0.9,
    trades: [
      { date: '2025-06-01', profit: 0.05 },
      { date: '2025-06-02', profit: 0.03 },
    ],
  };
};

module.exports = { generateBacktestResults };