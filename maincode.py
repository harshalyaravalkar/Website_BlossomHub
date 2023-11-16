# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect

# Import pymysql as p for MySQL connectivity
import pymysql as p

# Function to establish a database connection
def getconnect():
    return p.connect(host="harshalyaravalkar.mysql.pythonanywhere-services.com", user="harshalyaravalka", password="haryarpyany", database="harshalyaravalka$blossomhub")

# Function to fetch all usernames and passwords from the 'users' table
def getdata():
    db = getconnect()
    cr = db.cursor()

    sql = "select username, password from users"
    cr.execute(sql)
    data = cr.fetchall()

    db.commit()
    db.close()
    return data

# Function to insert user data into the 'users' table
def insertdata(t):
    db = getconnect()
    cr = db.cursor()

    sql = "insert into users (username, email, password) values (%s, %s, %s)"
    cr.execute(sql, t)
    
    db.commit()
    db.close()

# Function to fetch all data of all users from the 'users' table
def alldata():
    db = getconnect()
    cr = db.cursor()

    sql = "select id, username, email, password from users"
    cr.execute(sql)
    userlist = cr.fetchall()

    db.commit()
    db.close()
    return userlist

# Function to fetch data of a specific user by their ID from the 'users' table
def getdatabyid(ids):
    db = getconnect()
    cr = db.cursor()

    sql = "select id, username, email, password from users where id=%s"
    cr.execute(sql, ids)
    data = cr.fetchone()

    db.commit()
    db.close()
    return data

# Function to update user data in the 'users' table
def updatedata(t):
    db = getconnect()
    cr = db.cursor()

    sql = "update users set username=%s, email=%s, password=%s where id=%s"
    cr.execute(sql, t)
    
    db.commit()
    db.close()

# Function to delete user data from the 'users' table
def deletedata(ids):
    db = getconnect()
    cr = db.cursor()

    sql = "delete from users where id=%s"
    cr.execute(sql, ids)
    
    db.commit()
    db.close()

# Function to fetch admin credentials from the 'users' table
def getadmin():
    db = getconnect()
    cr = db.cursor()

    sql = "select username, password, admin from users"
    cr.execute(sql)
    adminfo = cr.fetchall()

    db.commit()
    db.close()
    return adminfo

# ======================== Flask =================================
app = Flask(__name__)

# Route to the login page
@app.route("/")
def login():
    return render_template("login.html")

# Route to the home page
@app.route("/home")
def home():
    return render_template("homepage.html")

# Route to the registration page
@app.route("/registeration")
def register():
    return render_template("signup.html")

# Route to the admin login page
@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")

# Route to the summer page
@app.route("/summer")
def summer():
    return render_template("summer.html")

# Route to the spring page
@app.route("/spring")
def spring():
    return render_template("spring.html")

# Route to the winter page
@app.route("/winter")
def winter():
    return render_template("winter.html")

# Route to fetch all user data and display it in the user list
@app.route("/userlist")
def getuser():
    ulist = alldata()
    return render_template("userlist.html", u_list=ulist)

# Route to validate admin login
@app.route("/validadmin", methods=["POST"])
def admin():
    usernem = request.form["uname"]
    paw = request.form["pin"]
    adm = request.form["adm_in"]
    
    adminfo = (usernem, paw, adm)
    datab = getadmin()

    if(adminfo in datab):
        ulist = alldata()
        return render_template("userlist.html", u_list=ulist)

# Route to validate regular user login
@app.route("/validateuser", methods=["POST"])
def valid_user():
    usern = request.form["uname"]
    passw = request.form["pin"]
    
    data = (usern, passw)
    database = getdata()

    if(data in database):
        return render_template("homepage.html")
    else:
        return render_template("signup.html")

# Route to insert user data into the 'users' table
@app.route("/insertrec", methods=["POST"])
def signup():
    usernm = request.form["uname"]
    email = request.form["email"]
    pasw = request.form["pin"]
    
    t = (usernm, email, pasw)
    insertdata(t)
    return render_template("login.html")

# Route to update user data by their ID
@app.route("/updateuser/<int:ids>")
def update_user(ids):
    d = getdatabyid(ids)
    return render_template("update.html", data=d)

# Route to update user data after editing
@app.route("/updaterec", methods=["POST"])
def update_rec():
    ids = request.form["id"]
    usernm = request.form["uname"]
    email = request.form["email"]
    pasw = request.form["pin"]
    
    t = (usernm, email, pasw, ids)
    updatedata(t)
    return redirect("/userlist")

# Route to delete user data by their ID
@app.route("/deleteuser/<int:ids>")
def delete_user(ids):
    deletedata(ids)
    return redirect("/userlist")

# Run the Flask app
if (__name__ == "__main__"):
    app.run(debug=True)
