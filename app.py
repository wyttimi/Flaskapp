from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_mysqldb import MySQL
import yaml

app= Flask(__name__)
app.secret_key = "d03811b6f39d7a1ef40400f3a96648b4"

#database configuration
db=yaml.load(open('db.yaml'), Loader=yaml.FullLoader)
app.config["MYSQL_HOST"] = db["mysql_host"]
app.config["MYSQL_USER"] = db["mysql_user"]
app.config["MYSQL_PASSWORD"] = db["mysql_password"]
app.config["MYSQL_DB"] = db["mysql_db"]

mysql = MySQL(app)

#login for all
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        userdata=request.form
        username=userdata["username"]
        password=userdata["password"]
        cur=mysql.connection.cursor()
        value=cur.execute("SELECT username, password FROM user WHERE username=%s",(username,))

        if value>0:
            data=cur.fetchone()
            passw=data[1]
            if password==passw:
                session["logged_in"]=True
                session["username"]=username
                flash("Login Successful","success")
                #return redirect("/Mainpage")
        else:
            flash("User not found.")
        cur.close()
    return render_template("login.html")

#register
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        userdata=request.form
        username=userdata["username"]
        password=userdata["password"]
        name=userdata["name"]
        email=userdata["email"]
        phone=userdata["phone"]
        dob=userdata["dob"]
        address=userdata["address"]
        occupation=userdata["occupation"]
        cur=mysql.connection.cursor()

        cur.execute("SELECT * FROM user WHERE username = %s", (username,))
        existing_user=cur.fetchone()
        if existing_user:
            flash(f"Username '{username}' already exists. Please choose a different username.", "danger")
            cur.close()
            return redirect("/register")
        else:
            cur.execute("INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(username,password,name,email,phone,dob,address,occupation))
            mysql.connection.commit()
            flash("Register Successful.")
            cur.close()
            return redirect("/")
    return render_template("register.html")

#staff login
@app.route("/staff/login", methods=["GET","POST"])
def staff_login():
    if request.method == "POST":
        userdata=request.form
        username=userdata["username"]
        password=userdata["password"]
        cur=mysql.connection.cursor()
        value=cur.execute("SELECT username, password FROM user WHERE username=%s",(username,))

        if value>0:
            data=cur.fetchone()
            passw=data["password"]
            if password==passw:
                session["logged_in"]=True
                session["username"]=username
                flash("Login Successful","success")
                #return redirect("Staffpage")
        else:
            flash("User not found.")
        cur.close()
    return render_template("staff_login.html")

#C-home page
@app.route("/homepage", methods=["GET","POST"])
def homepage():
    return render_template("homepage.html")

#C-setting/profile
@app.route("/user/setting/profile", methods=["GET","POST"])
def setting_profile():
    return render_template("setting_profile.html")

#C-setting/profile/edit profile
@app.route("/user/setting/profile/edit", methods=["GET","POST"])
def setting_profile_edit():
    return render_template("setting_profile_edit.html")

#C-setting/payment method
@app.route("/user/setting/payment_method", methods=["GET","POST"])
def setting_payment_method():
    return render_template("setting_payment_method.html")

#C-setting/payment detail/edit payment detail
@app.route("/user/setting/payment_method/edit", methods=["GET","POST"])
def setting_payment_method_edit():
    return render_template("setting_payment_method_edit.html")

#C-setting/payment detail/add payment detail
@app.route("/user/setting/payment_method/add", methods=["GET","POST"])
def setting_payment_method_add():
    return render_template("setting_payment_method_add.html")

#C-setting/history(default purchase)
@app.route("/user/setting/history/purchase", methods=["GET","POST"])
def setting_history_purchase():
    return render_template("setting_history_purchase.html")

#C-setting/history/search history
@app.route("/user/setting/history/search", methods=["GET","POST"])
def setting_history_search():
    return render_template("setting_history_search.html")

#C-survey page
@app.route("/recommend/survey", methods=["GET","POST"])
def recommend_survey():
    return render_template("recommend_survey.html")

#C-survey/fill in survey
@app.route("/recommend/survey/form", methods=["GET","POST"])
def recommend_survey_form():
    return render_template("recommend_survey_form.html")

#C-auto recommend page
@app.route("/recommend/auto", methods=["GET","POST"])
def recommend_auto():
    return render_template("recommend_auto.html")

#C-laptop(all)
@app.route("/laptop", methods=["GET","POST"])
def laptop():
    return render_template("laptop.html")

#C-laptop/search+filter result
@app.route("/laptop/search", methods=["GET","POST"])
def laptop_search():
    return render_template("laptop_search.html")

#C-laptop/detail
@app.route("/laptop/detail", methods=["GET","POST"])
def laptop_detail():
    return render_template("laptop_detail.html")

#C-cart(all)
@app.route("/cart", methods=["GET","POST"])
def cart():
    return render_template("cart.html")

#C-cart/checkout(choose payment method,address)
@app.route("/cart/checkout", methods=["GET","POST"])
def cart_checkout():
    return render_template("cart_checkout.html")

#C-cart/payment
@app.route("/cart/payment", methods=["GET","POST"])
def cart_payment():
    return render_template("cart_payment.html")

#C-cart/payment success
@app.route("/cart/payment/success", methods=["GET","POST"])
def cart_payment_success():
    return render_template("cart_payment_success.html")

#C-cart/payment failed
@app.route("/cart/payment/failed", methods=["GET","POST"])
def cart_payment_failed():
    return render_template("cart_payment_failed.html")

#A-home page
@app.route("/admin/homepage", methods=["GET","POST"])
def admin_homepage():
    return render_template("admin_homepage.html")

#A-laptop
@app.route("/admin/laptop", methods=["GET","POST"])
def admin_laptop():
    return render_template("admin_laptop.html")

#A-laptop/edit laptop
@app.route("/admin/laptop/edit", methods=["GET","POST"])
def admin_laptop_edit():
    return render_template("admin_laptop_edit.html")

#A-laptop/detail
@app.route("/admin/laptop/detail", methods=["GET","POST"])
def admin_laptop_detail():
    return render_template("admin_laptop_detail.html")

#A-feedback(view+reply)
@app.route("/admin/feedback/user", methods=["GET","POST"])
def admin_feedback_user():
    return render_template("admin_feedback_user.html")

#A-feedback/send feedback
@app.route("/admin/feedback/send", methods=["GET","POST"])
def admin_feedback_send():
    return render_template("admin_feedback_send.html")

#A-orders
@app.route("/admin/orders", methods=["GET","POST"])
def admin_orders():
    return render_template("admin_orders.html")

#M-home page
@app.route("/manager/homepage", methods=["GET","POST"])
def manager_homepage():
    return render_template("manager_homepage.html")

#M-laptop
@app.route("/manager/laptop", methods=["GET","POST"])
def manager_laptop():
    return render_template("manager_laptop.html")

#M-laptop/detail
@app.route("/manager/laptop/detail", methods=["GET","POST"])
def manager_laptop_detail():
    return render_template("manager_laptop_detail.html")

#M-view account
@app.route("/manager/account", methods=["GET","POST"])
def manager_account():
    return render_template("manager_account.html")

#M-view account/add new account
@app.route("/manager/account/new", methods=["GET","POST"])
def manager_account_new():
    return render_template("manager_account_new.html")

#M-reports/daily
@app.route("/manager/reports/daily", methods=["GET","POST"])
def manager_reports_daily():
    return render_template("manager_reports_daily.html")

#M-reports/weekly
@app.route("/manager/reports/weekly", methods=["GET","POST"])
def manager_reports_weekly():
    return render_template("manager_reports_weekly.html")

#M-reports/monthly
@app.route("/manager/reports/monthly", methods=["GET","POST"])
def manager_reports_monthly():
    return render_template("manager_reports_monthly.html")

#M-reports/yearly
@app.route("/manager/reports/yearly", methods=["GET","POST"])
def manager_reports_yearly():
    return render_template("manager_reports_yearly.html")

#M-feedbacks
@app.route("/manager/feedback", methods=["GET","POST"])
def manager_feedback():
    return render_template("manager_feedback.html")

if __name__=='__main__':
    app.run(debug=True)