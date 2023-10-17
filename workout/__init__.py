from flask import Flask, request, render_template
from .config.variables import SECRET_KEY
from dotenv import dotenv_values
import os


# ENV = dotenv_values()
# print("ENV:", ENV) 



def create_app():
    app = Flask(__name__)

    # CONFIGS
    app.config["SECRET_KEY"] = SECRET_KEY





    from .views.workout_route import workblog
    app.register_blueprint(workblog)



        # CREATE AN ERROR ROUTE FOR 404 & 500

    # # 404 ERROR
    # @app.errorhandler(404)
    # def error_404(error):
    #     print("404 ERROR:", str(error))
    #     return render_template("error-404.html")
    
    #     # 500 ERROR
    # @app.errorhandler(Exception)
    # def error_500(error):
    #     print("500 ERROR:", str(error))
    #     return render_template("error-500.html")



    return app