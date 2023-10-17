from flask import Blueprint, request, flash, redirect, url_for, render_template, session, get_flashed_messages
# from workout.config.variables import SECRET_KEY
from ..config.database import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

from ..config.database import get_connection
from workout.templates.utils.decorators import autheticated_admin, guest_admin, prevent_multiple







workblog = Blueprint("workblog", __name__)
# workblog.SECRET_KEY = SECRET_KEY 
workblog1 = []
workblog2 = []
db = get_connection()


# REGISTER ROUTE VIEW
@workblog.get("/register")
# @guest_admin
# @prevent_multiple
def register_page():
    return render_template("register.html")

# REGISTER ROUTE VIEW
@workblog.get("/login")
# @guest_admin
def login_page():
    return render_template("login.html")




@workblog.post("/create")
def handle_register_page():

    form = request.form

    email = form.get('email')
    name = form.get('name')
    password = form.get('password')
    hashed_password = generate_password_hash(password)

    if not db:
        flash("danger connecting to db", "danger")
        return redirect("/register")

    conn, cursor = db


    query = "INSERT INTO workout(name, email, password) VALUES(%s, %s, %s)"
    cursor.execute(query, [name, email, hashed_password])
    conn.commit()

    if not cursor.rowcount:
        flash("Failed to register admin", "danger")
        return redirect("/register")

    flash("Registration Successful", "Success")
    return redirect("/login")



# LOGIN ROUTE (VIEW)
@workblog.post("/login")
def handle_login_page():
    form = request.form

    # FORM FIELDS
    email = form.get("email")
    password = form.get("password")


    if not db:
        flash("danger connecting to db", "danger")
        return redirect("/login")
    
    conn, cursor = db


    # GET THE ADMIN
    query = "select * FROM workout WHERE email = %s"
    cursor.execute(query, [email])

    user = cursor.fetchone()

    if not user:
        flash("User does not exist", "danger")
        return redirect("/login")
    
    # VERIFY THE PASSWORD
    if not check_password_hash(user.get("password"), password):
        flash("Incorrect credentials", "danger")
        return redirect("/login")
    

    # CREATE MADMIN LOGIN SESSION
    session["WORKBLOG_LOGIN"] = user.get("id")

    flash("Login successful", "success")
    return redirect("/home")

# HANDLE ADMIN LOGOUT
@workblog.get("/logout")
def logout_admin():
    session.pop("WORKBLOG_LOGIN", None)
    return redirect("/login")


@workblog.get("/home")
# @autheticated_admin
def workblog_page():

    return render_template("index.html")
    # return redirect("/home")



@workblog.get("/data")
def workblog_data():
    html = render_template("all_workouts.html", workblog1=enumerate(workblog1))
    return html

@workblog.get("/edit")
def edit_workblog():
    return render_template("edit.html", workblog1=enumerate(workblog1))

@workblog.get("/workout")
def workout_page():
    return render_template("newworkout.html")

@workblog.get("/allworkout")
def allworkout_page():
    return render_template("all_workouts.html", workblog1=enumerate(workblog1))

@workblog.post("/add")
def workout_add():
    form = request.form
    workblog1.append(form)
    print("USERS:", workblog1)

    # for workblog in workouts

    return redirect("/data")

@workblog.get("/delete/<int:id>")
def workblog_delete(id):
    print("PRINT: ", len(workblog1))
    workblog1.pop(id)
    
    # Redirect to todo page
    return redirect(url_for('workblog.workblog_data'))

@workblog.post("/update/<int:id>")
def handle_save_workblog(id):
    # GET THE NEW VALUE FROM THE INPUT
    myForm = request.form
    print(myForm)
    
    workblog1[id] = myForm



    return redirect("/data")



