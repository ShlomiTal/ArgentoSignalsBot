const express = require('express');
const router = express.Router();
const { generateSignal, sendTelegramMessage } = require('../services/ml');
const { sendMessage } = require('../services/telegram');

router.get('/', async (req, res) => {
  const signals = await generateSignal();
  res.json(signals);
});

router.post('/test', async (req, res) => {
  const { message } = req.body;
  await sendMessage(message);
  res.json({ status: 'Message sent' });
});

module.exports = router;