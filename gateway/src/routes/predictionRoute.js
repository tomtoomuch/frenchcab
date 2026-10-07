const express = require("express");
const router = express.Router();
const predictionControllers = require("../controllers/predictionController");


router.get("/prediction", predictionControllers.getPrediction);


module.exports = router;