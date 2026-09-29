const bdd = require("../data/connexion.js");

function trouverCourseParId(id, callback) {
    bdd.query(
        `SELECT * FROM trajets WHERE id_trajet = ?`,
        [id],
        (err, result) => {
            if (err) {
                return callback(err, null);
            }
            return callback(null, result[0]);
        }
    );
}

function trouverCourse(callback) {
    bdd.query(
        `SELECT * FROM trajets`,
        (err, result) => {
            if (err) {
                return callback(err, null);
            }
            return callback(null, result);
        }
    );
}


module.exports = {
    trouverCourseParId,
    trouverCourse

}