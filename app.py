from flask import Flask, g, render_template
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
    #home page - just the ID, Maker, Model and Image URL
    sql = """
            SELECT Planes.PlaneID,Manufacturer.Name,Planes.Model,Planes.ImageURL
            FROM Planes
            JOIN Manufacturer ON Manufacturer.manufacturerID=Planes.manufacturerID;"""
    results = query_db(sql)
    return render_template("home.html", results=results)


@app.route('/plane/<int:id>')
def plane(id):
    #just one plane based on the id
    sql = """
            SELECT * FROM Planes
            JOIN Manufacturer on Manufacturer.ManufacturerID = Planes.ManufacturerID
            WHERE Planes.PlaneID = ?;"""
    result = query_db(sql, (id,), True)
    return render_template("plane.html", plane=result)

@app.route('/manufacturer/<int:id>')
def manufacturer(id)
    #all planes from a specific manufacturer
    sql = """
    SELECT * FROM Planes
    JOIN Manufacturer on Manufacturer.ManufacturerID = Planes.ManufacturerID
            WHERE Planes.ManufacturerID = ?;"""
    result = query_db(sql, (id,), True)
    return render_template("manufacturer.html", plane=result)


if __name__ == '__main__':
    app.run(debug=True)
