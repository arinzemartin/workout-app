from functools import wraps
from flask import session, redirect, abort
from workout.config.database import get_connection 

def guest_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("WORKBLOG_LOGIN"): return redirect("/login")
        return func(*args, **kwargs)
    return wrapper


def autheticated_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("WORKBLOG_LOGIN"): return redirect("/register")
        return func(*args, **kwargs)
    return wrapper


def prevent_multiple(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        db = get_connection()
        if not db: return abort(500, "Failed to connect to DB")

        conn, cursor = db
        query = "SELECT * FROM workblog"
        cursor.execute(query)

        count = cursor.rowcount
        if count: return redirect("/register")

        return func(*args, **kwargs)
    return wrapper
