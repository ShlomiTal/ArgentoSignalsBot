const TelegramBot = require('node-telegram-bot-api');
const dotenv = require('dotenv');
dotenv.config();

const bot = new TelegramBot(process.env.TELEGRAM_TOKEN, { polling: false });

const sendMessage = async (message, chatId = process.env.CHAT_ID) => {
  try {
    await bot.sendMessage(chatId, message);
    return { success: true };
  } catch (error) {
    console.error('Telegram error:', error);
    return { success: false, error };
  }
};

module.exports = { sendMessage };