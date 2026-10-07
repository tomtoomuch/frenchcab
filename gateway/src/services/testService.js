const axios = require("axios");
const bdd = require("../../connexion.js");

const PYTHON_SERVICE_URL = "https://api1.valentinduflot.fr";


async function getTests() {

    console.log("URL Backend :", process.env.BACKEND_URL);

    try {

        const response = await axios.get(`${process.env.BACKEND_URL}/test`);
 
        return response.data;

    } catch (error) {

        console.log(error.message);

        throw new Error("Impossible de contacter l'API");    
    }
}


// -------------------------------------
// COURSE PAR ID
// -------------------------------------

function getTrouverCourseParId(uid_trajet) {

    return new Promise((resolve, reject) => {

        bdd.get(
            `SELECT * FROM trajets
             WHERE uid_trajet = ?`,
            [uid_trajet],
            (err, result) => {

                if (err) {
                    return reject(err);
                }

                resolve(result);
            }
        );
    });
}


// -------------------------------------
// LISTE DES COURSES
// -------------------------------------

function getCourses(limit, offset) {

    return new Promise((resolve, reject) => {

        bdd.all(
            `SELECT * FROM trajets
             LIMIT ? OFFSET ?`,
            [limit, offset],
            (err, result) => {

                if (err) {
                    return reject(err);
                }

                resolve(result);
            }
        );
    });
}


// -------------------------------------
// PREDICTION PYTHON
// -------------------------------------

async function getPrediction(zone_depart, zone_arrivee, date_depart, heure_depart) {

    return axios.get(
        `${PYTHON_SERVICE_URL}/api/prediction`,
        {
            params: {zone_depart, zone_arrivee, date_depart, heure_depart}
        }
    );
}


module.exports = {getTests, getTrouverCourseParId, getCourses, getPrediction};