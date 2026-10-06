const bdd = require('../../connexion.js');
const { execFile } = require('child_process');
const path = require('path');

function trouverCourseParId(id, callback) {
    bdd.get(
        `SELECT * FROM trajets WHERE id_trajet = ?`,
        [id],
        (err, result) => {
            if (err) {
                return callback(err, null);
            }
            return callback(null, result);
        }
    );
}

function trouverCourse(limit, offset, callback) {
    bdd.all(
        `SELECT * FROM trajets LIMIT ? OFFSET ?`,
        [limit, offset],
        (err, result) => {
            if (err) {
                return callback(err, null);
            }
            return callback(null, result);
        }
    );
}

function predictionTrajet(locDep, locArr, jour, temps, callback){
    const pythonScript = path.join(__dirname, '..', '..', 'ML', 'taxi_duree_prediction.py');
        execFile('python3', [script, 'dm'], (err, result, stderr) => {
    if (err) {
      console.error(stderr);
      return callback({ error: 'Erreur Python' });
    }
        res.json(JSON.parse(result));
    });
}

module.exports = {
    trouverCourseParId,
    trouverCourse
};