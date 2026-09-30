const express = require("express");
const router = express.Router();
const courseModel = require('../Model/courseModel.js')




router.get('/courseID', (req,res) => {

    const id  = Number(req.query.id);
    //console.log("id reçu : ", id)
    courseModel.trouverCourse(id, (err, course) => {
         console.log("Erreur SQL :", err);
    console.log("course :", course);

    if (err) {
        return res.status(500).json({ 
            success: false,
            error: err.message
        });
    }
        if (course) {
             return res.status(200).json({
                course,             
                }
             );
        
        }else {
             return res.status(404).json({"message":"course non trouvé"})
        }

            
    });
});

router.get('/courses', (req,res) => {

    courseModel.trouverCourse((err, course) => {
         console.log("Erreur SQL :", err);
    console.log("course :", course);

        if (err) {
            return res.status(500).json({
                success: false,
                error: err.message
            });
        }

        return res.status(200).json({
            "courses" : course
        });

    });

});


module.exports = router;