const express = require('express');
const router = express.Router();
const fs = require('fs').promises;
const path = require('path');

const SETTINGS_FILE = path.join(__dirname, '../settings.json');

router.get('/', async (req, res) => {
  try {
    const settings = await fs.readFile(SETTINGS_FILE, 'utf8');
    res.json(JSON.parse(settings));
  } catch (error) {
    res.status(500).json({ error: 'Failed to read settings' });
  }
});

router.post('/', async (req, res) => {
  try {
    await fs.writeFile(SETTINGS_FILE, JSON.stringify(req.body, null, 2));
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: 'Failed to save settings' });
  }
});

module.exports = router;