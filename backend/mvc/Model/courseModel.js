const bdd = require('../../connexion.js');

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

module.exports = {
    trouverCourseParId,
    trouverCourse
};