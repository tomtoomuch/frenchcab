const express = require("express");
const router = express.Router();
const courseController = require("../controllers/courseController");


router.get("/", testControllers.getTest);
router.get("/courses", testControllers.getCourses);
router.get("/courseID", testControllers.getTrouverCourseParId);


module.exports = router;