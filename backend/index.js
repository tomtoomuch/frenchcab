const express = require('express');
const app = express()
const port = 3001
const cors = require('cors'); // 1. Importer le module CORS


// 2. Autoriser uniquement votre frontend Angular
app.use(cors({
  origin: 'http://localhost:4200'
}));

// Permet à Express de lire le JSON envoyé par Angular dans le body des requêtes
app.use(express.json()); 



app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`App connecté sur le port  ${port}`)
})