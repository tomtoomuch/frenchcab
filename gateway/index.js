const express = require("express");
require("dotenv").config();
const cors = require('cors');

const app = express();

app.use(cors());

app.use(express.json());

const testRoutes = require("./src/routes/testRoutes");

app.use("/test", testRoutes)

app.listen(3000, () => {
  console.log(`Application à l'écoute sur le port 3000!`);
});