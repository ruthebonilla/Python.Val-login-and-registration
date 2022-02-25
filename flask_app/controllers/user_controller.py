from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, session, request, flash
bcrypt = Bcrypt(app)

from flask_app.models.user import User





# MAIN PAGE////////////////////////////
@app.route("/")
def log_reg():
    return render_template("index.html")




#PROCESSING REGISTRATION////////////////
@app.route("/register", methods=["POST"])
def register():
    #VALIDATE THE FORM
    if not User.validate_user(request.form):
        return redirect("/")
    #CHECK TO SEE IF EMAIL IS IN DATABASE
    data = {
        "email" : request.form['email']
    }
    if User.get_by_email(data):
        flash("email you entered already exits")
        return redirect ("/")

    # WE NEED TO HASH PASSWORD BEFORE SAVING
    pass_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data={
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pass_hash
    }
    print(pass_hash)

    user_id = User.save(data)
    session['user_id'] = user_id

    return redirect("/logged_in")




# PROCESSING LOGIN////////////////////////
@app.route("/login", methods=["POST"])
def login():
    data ={
        "email" : request.form["email"]
    }
    # GRAB THE USER BASED ON EMAIL
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("User doesn't exit")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("wrong password")
        return redirect("/")

    session["user_id"] = user_in_db.id

#PAGE USER LANDS ON AFTER LOGGING IN
    return redirect("/logged_in")



@app.route("/logged_in")
def logged_in():
    if "user_id" not in session:
        flash("please register/login")
        return redirect ("/")
    

    data = {
    "user_id" : session["user_id"]  
    }
    user = User.get_user_by_id(data)
    return render_template("logged_in.html", user = user)

# LOGOUT USER
@app.route("/logout")
def logout():
    session.clear()
    flash("you have successfully logged out")
    return redirect("/")