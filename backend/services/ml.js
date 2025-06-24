// דוגמה פשוטה - יושם עם ML אמיתי בהמשך
const generateSignal = async () => {
  // לוגיקה זמנית
  return [
    {
      id: 1,
      asset: 'BTC/USD',
      price: 60000,
      confidence: 0.85,
      timestamp: new Date(),
    },
  ];
};

module.exports = { generateSignal };