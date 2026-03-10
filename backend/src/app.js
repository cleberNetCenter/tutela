const express = require('express');
const cors = require('cors');
const routes = require('./routes');

const app = express();

app.use(cors());
app.use(express.json());

app.use('/api', routes);

app.get('/health', (_, res) => {
  res.status(200).json({ status: 'ok' });
});

module.exports = app;
