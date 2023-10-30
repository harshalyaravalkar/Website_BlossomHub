from flask import Flask, render_template, request, redirect

import pymysql as p

def getconnect():
    return p.connect (host="harshalyaravalkar.mysql.pythonanywhere-services.com", user="harshalyaravalka", password="haryarpyany", database="harshalyaravalka$blossomhub")


def getdata():
    db = getconnect()
    cr = db.cursor()

    sql ="select username, password from users"
    cr.execute(sql)
    data = cr.fetchall()

    db.commit()
    db.close()
    return data


def insertdata(t):
    db = getconnect()
    cr = db.cursor()

    sql = "insert into users (username,email,password) values (%s, %s, %s)"
    cr.execute(sql, t)
    

    db.commit()
    db.close()

def alldata():
    db = getconnect()
    cr = db.cursor()

    sql = "select id,username,email,password from users"
    cr.execute(sql)
    userlist = cr.fetchall()

    db.commit()
    db.close()
    return userlist

def getdatabyid(ids):
    db = getconnect()
    cr = db.cursor()

    sql = "select id,username,email,password from users where id=%s"
    cr.execute(sql,ids)
    data = cr.fetchone()

    db.commit()
    db.close()
    return data

def updatedata(t):
    db = getconnect()
    cr = db.cursor()

    sql = "update users set username=%s, email=%s, password=%s where id=%s"
    cr.execute(sql, t)
    

    db.commit()
    db.close()

def deletedata(ids):
    db = getconnect()
    cr = db.cursor()

    sql = "delete from users where id=%s"
    cr.execute(sql, ids)
    

    db.commit()
    db.close()

def getadmin():
    db = getconnect()
    cr = db.cursor()

    sql = "select username, password, admin from users"
    cr.execute(sql)
    adminfo = cr.fetchall()

    db.commit()
    db.close()
    return adminfo




#======================== Flask =================================
app = Flask(__name__)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/home")
def home():
    return render_template("homepage.html")

@app.route("/registeration")
def register():
    return render_template("signup.html")

@app.route("/adminlogin")
def adminlogin():
    return render_template("adminlogin.html")

@app.route("/summer")
def summer():
    return render_template("summer.html")

@app.route("/spring")
def spring():
    return render_template("spring.html")

@app.route("/winter")
def winter():
    return render_template("winter.html")


@app.route("/userlist")
def getuser():

    ulist = alldata()

    return render_template("userlist.html", u_list = ulist )

@app.route("/validadmin", methods=["POST"])
def admin():
    usernem = request.form["uname"]
    paw = request.form["pin"]
    adm = request.form["adm_in"]

    adminfo = (usernem, paw, adm)
    datab = getadmin()

    if(adminfo in datab):
        ulist = alldata()
        return render_template("userlist.html", u_list = ulist)


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

@app.route("/insertrec", methods = ["POST"])
def signup():
    usernm = request.form["uname"]
    email = request.form["email"]
    pasw = request.form["pin"]

    t = (usernm,email,pasw)
    insertdata(t)
    return render_template("homepage.html")


@app.route("/updateuser/<int:ids>")
def update_user(ids):
    d = getdatabyid(ids)
    return render_template("update.html", data = d)

@app.route("/updaterec", methods=["POST"])
def update_rec():
    ids = request.form["id"]
    usernm = request.form["uname"]
    email = request.form["email"]
    pasw = request.form["pin"]

    t = (usernm, email, pasw, ids)
    updatedata(t)

    return redirect("/userlist")

@app.route("/deleteuser/<int:ids>")
def delete_user(ids):
    deletedata(ids)
    return redirect("/userlist")

if (__name__=="__main__"):
    app.run(debug=True)
    
