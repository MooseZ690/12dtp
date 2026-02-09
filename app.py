from flask import Flask, g
import sqlite3
DATABASE = 'database.db'

#initialize app
app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route("/")
def home():
    #home page - just the ID, Mkaer, Model and Image URL
    sql = """
            SELECT Planes.PlaneID,Manufacturer.Name,Planes.Model,Planes.ImageURL
            FROM Planes
            JOIN Manufacturer ON Manufacturer.manufacturerID=Planes.manufacturerID;"""
    results = query_db(sql)
    return str(results)


@app.route('/plane/<int:id>')
def plane(id):
    #just one plane based on the id
    sql = """
            SELECT * FROM Planes
            JOIN Manufacturer on Manufacturer.ManufacturerID = Planes.ManufacturerID
            WHERE Planes.PlaneID = ?;"""
    result = query_db(sql, (id,), True)
    return str(result)


if __name__ == '__main__':
    app.run(debug=True)
