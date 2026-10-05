const express = require('express');
const app = express();
const port = 3001;
const cors = require('cors');
const courseRoute = require('./mvc/Route/courseRoute.js');


app.use(cors({ origin: ['http://localhost:4200', 'https://g1.valentinduflot.fr']}));


app.use(express.json());

app.get('/hello', (req, res) => {
  res.send('Hello World!');
});

app.use('/api', courseRoute);

app.listen(port, () => {
  console.log(`App connecté sur le port ${port}`);
});