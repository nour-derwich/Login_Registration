from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt,  

# ======== Display Route ========
@app.route("/")
def regist_log():
    if 'user_id' in session:
        return redirect("/dashboard")

    return render_template("index.html")

# ======== Action Route ========
@app.route("/users/create", methods=["post"])
def register():
    # validation

    if not User.validate_reg(request.form):
        return redirect("/")
    # print(request.form)
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    register_data = {
        **request.form,
        "password": pw_hash,
    }

    user_id = User.create(register_data)
    session['user_id'] = user_id

    return redirect("/dashboard")

# ======== Action Route ========

@app.route("/users/login", methods=["post"])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.get_by_email(data)
    #check email
    if not user_in_db:
        flash("Invalid credentials !", "login")
        return redirect("/")
    # check password
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid credentials !", "login")
        return redirect("/")

    # all good
    session["user_id"] = user_in_db.id
    return redirect("/dashboard")

# ======== Display Route ========

@app.route("/dashboard")
def dash():
    if 'user_id' not in session:
        return redirect("/")
    loggedin_user = User.get_by_id({"id": session["user_id"]})
    print(loggedin_user)
    return render_template("result.html", loggedin_user = loggedin_user)


# ====== Action Route =======
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")