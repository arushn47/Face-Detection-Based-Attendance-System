from flask import Flask, render_template, redirect, url_for
from routes.auth import auth_bp
from routes.teacher import teacher_bp
from routes.principal import principal_bp

app = Flask(__name__)

# 🔐 Secret Key for Sessions
app.secret_key = "09a97d14ef55f3ece1eaec00b42f22f2"

# 🔹 Register Blueprints (Auth, Teacher, Principal)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(teacher_bp, url_prefix="/teacher")
app.register_blueprint(principal_bp, url_prefix="/principal")

# 🌐 Home Route (Redirect to Login)
@app.route("/")
def home():
    return redirect(url_for("auth.login"))

# 🌐 Error Handler (404 Page Not Found)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("auth/error.html", error="Page Not Found"), 404

if __name__ == "__main__":
    app.run(debug=True)