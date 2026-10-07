const express = require("express");
const router = express.Router();
const testControllers = require("../controllers/testControllers");


router.get("/", testControllers.getTest);
router.get("/courses", testControllers.getCourses);
router.get("/courseID", testControllers.getTrouverCourseParId);
router.get("/prediction", testControllers.getPrediction);


module.exports = router;