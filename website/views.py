from flask import Blueprint, render_template
from flask_login import login_required, current_user


views=Blueprint('views',__name__)

@views.route('/')
def welcome():
    return render_template("welcome.html")

@views.route('/home')
@login_required
def home():
    return render_template("accounts.html", user = current_user)

@views.route('/YourAccounts')
@login_required
def YourAccounts():
    return render_template("accounts.html", user = current_user)

@views.route('/UpcomingPayments')
@login_required
def UpcomingPayments():
    return render_template("upcoming_payments.html", user = current_user)