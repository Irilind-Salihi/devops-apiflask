import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
mysql.init_app(app)


@app.route("/")
def index():
    return "Hello, world!"


@app.route("/create", methods=["POST"])
def add_user():
    json = request.json
    name = json["name"]
    email = json["email"]
    pwd = json["pwd"]
    if name and email and pwd and request.method == "POST":
        sql = "INSERT INTO users(user_name, user_email, user_password) " \
              "VALUES(%s, %s, %s)"
        data = (name, email, pwd)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("User created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide name, email , password")


@app.route("/users", methods=["GET"])
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/user/<int:user_id>", methods=["GET"])
def user(user_id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id=%s", user_id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/update", methods=["POST"])
def update_user():
    json = request.json
    name = json["name"]
    email = json["email"]
    pwd = json["pwd"]
    user_id = json["user_id"]
    if name and email and pwd and user_id and request.method == "POST":
        # save edits
        sql = "UPDATE users SET user_name=%s, user_email=%s, " \
              "user_password=%s WHERE user_id=%s"
        data = (name, email, pwd, user_id)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify("updated!")
            resp.status_code = 200
            cursor.close()
            conn.close()
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("give me id, name, email , password")


@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    """Function to delete a user from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id=%s", user_id)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify("Deleted!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
