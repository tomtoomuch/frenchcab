const express = require("express");
const router = express.Router();
const courseModel = require('../Model/courseModel.js')




router.get('/courseID', (req,res) => {

    const id  = Number(req.query.id);
    //console.log("id reçu : ", id)
    courseModel.trouverCourseParId(id, (err, course) => {
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

router.get('/courses', (req, res) => {
    const limit = Number(req.query.limit) || 100;
    const offset = Number(req.query.offset) || 0;
    courseModel.trouverCourse(limit, offset, (err, course) => {
        console.log("Erreur SQL :", err);
        console.log("Nombre de courses :", course?.length);
        if (err) {
            return res.status(500).json({
                success: false,
                error: err.message
            });
        }
        return res.status(200).json({
            courses: course,
            limit,
            offset
        });
    });
});

router.post('/prediction', (req, res) => {
    const locDep = req.query.locDep;
    const locArr = req.query.locArr;
    const jour = req.query.jour;
    const temps = req.query.temps;
    courseModel.predictionTrajet(locDep, locArr, jour, temps, (err, trajet) => {
         console.log("Erreur SQL :", err);
    console.log("trajet :", trajet);

    if (err) {
        return res.status(500).json({ 
            success: false,
            error: err.message
        });
    }
        if (trajet) {
             return res.status(200).json({
                trajet,             
                }
             );
        
        }else {
             return res.status(404).json({"message":"course non trouvé"})
        }

            
    });

});


module.exports = router;