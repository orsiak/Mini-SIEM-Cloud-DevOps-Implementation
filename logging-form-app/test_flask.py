from flask import Flask,render_template, request, redirect,session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#Db config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.secret_key="upss" #need to be stored it in env variable

#Db modeling 
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(15), unique=True, nullable=False)
    password_hash=db.Column(db.String(150),nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)



#Routes


@app.route("/")
def main_page():
    if "username" in session:
        user_html = session.get("username")
        return render_template("index.html",user_html=user_html)
    else:
        return redirect(url_for("login"))

#register
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        user_check=User.query.filter_by(username=username).first()
        if user_check is None:
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        else:
            return render_template("register.html",error="There is user with that username")
    else:
        return render_template("register.html")
    


#login
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(password)
        user=User.query.filter_by(username=username).first()
        print(user)
        print(user.check_password(password))
        if user and user.check_password(password):
            session["username"]=username
            return redirect(url_for("main_page"))
        return render_template("login.html")
    else:
        return render_template("login.html")



#logout 
@app.route("/logout",methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1",port=8080,debug=True)