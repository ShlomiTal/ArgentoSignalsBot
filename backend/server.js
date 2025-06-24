const express = require('express');
const dotenv = require('dotenv');
const signalRoutes = require('./routes/signals');
const settingsRoutes = require('./routes/settings');
const authRoutes = require('./routes/auth');

dotenv.config();
const app = express();
app.use(express.json());

app.use('/api/signals', signalRoutes);
app.use('/api/settings', settingsRoutes);
app.use('/api/auth', authRoutes);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));