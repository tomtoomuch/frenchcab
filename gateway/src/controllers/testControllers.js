const gatewayService = require("../services/testService.js");


// -------------------------------------
// TEST
// -------------------------------------

async function getTest(req, res) {

    try {

        const data = await gatewayService.getTests();

        return res.status(200).json({
            success: true,
            data: data
        });

    } catch (error) {

        console.error("Erreur test :", error.message);

        return res.status(500).json({
            success: false,
            message: "Impossible de récupérer le test"
        });
    }
}


// -------------------------------------
// COURSE PAR ID
// -------------------------------------

async function getTrouverCourseParId(req, res) {

    try {

        const { uid_trajet } = req.query;

        console.log("Paramètre reçu :", req.query);

        if (!uid_trajet) {

            return res.status(400).json({
                success: false,
                message: "Le paramètre uid_trajet est obligatoire"
            });
        }

        const course = await gatewayService.getTrouverCourseParId(uid_trajet);

        if (!course) {

            return res.status(404).json({
                success: false,
                message: "Course non trouvée"
            });
        }

        return res.status(200).json({
            success: true,
            course: course
        });

    } catch (error) {

        console.error("Erreur récupération course :", error.message);

        return res.status(500).json({
            success: false,
            message:"Impossible de contacter la base de données"
        });
    }
}


// -------------------------------------
// LISTE DES COURSES
// -------------------------------------

async function getCourses(req, res) {

    try {

        const limit =
            Number(req.query.limit) || 100;

        const offset =
            Number(req.query.offset) || 0;

        const courses =
            await gatewayService.getCourses(limit, offset);

        return res.status(200).json({
            success: true,
            courses: courses,
            limit: limit,
            offset: offset
        });

    } catch (error) {

        console.error("Erreur récupération courses :", error.message);

        return res.status(500).json({
            success: false,
            message:"Impossible de contacter la base de données"
        });
    }
}


// -------------------------------------
// PREDICTION
// -------------------------------------

async function getPrediction(req, res) {

    try {

        const {zone_depart, zone_arrivee, date_depart, heure_depart} = req.query;

        console.log("Paramètres reçus :",req.query);

        if (!zone_depart || !zone_arrivee || !date_depart || !heure_depart) {

            return res.status(400).json({
                success: false,
                message:
                    "Les paramètres zone_depart, "
                    + "zone_arrivee, date_depart "
                    + "et heure_depart sont obligatoires"
            });
        }

        const reponse =
            await gatewayService.getPrediction(zone_depart, zone_arrivee, date_depart, heure_depart);

        return res.status(200).json({
            success: true,
            reponse: reponse.data
        });

    } catch (error) {

        console.error("Code reçu :", error.response?.status);
        console.error("Réponse reçue :", error.response?.data);
        console.error("Message :", error.message);

        return res.status(error.response?.status || 500).json({
            success: false,
            message:error.response?.data?.detail || error.message
        });
    }
}


module.exports = {getTest, getTrouverCourseParId, getCourses, getPrediction};