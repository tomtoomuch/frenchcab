const axios = require("axios");

const PYTHON_SERVICE_URL = "http://backend:3001";



// -------------------------------------
// PREDICTION PYTHON
// -------------------------------------



async function getPrediction(zone_depart, zone_arrivee, date_depart, heure_depart) {

    return axios.get(
        `${PYTHON_SERVICE_URL}/prediction`,
        {
            params: {zone_depart, zone_arrivee, date_depart, heure_depart}
        }
    );
}

async function getZones() {
    return axios.get(`${PYTHON_SERVICE_URL}/zones`);
}

module.exports = {getPrediction, getZones};