from flask import Blueprint, render_template, flash, request, redirect
from flask_login import login_required, current_user
from .models import Account
from . import db

views=Blueprint('views',__name__)

@views.route('/')
def welcome():
    return render_template("welcome.html")

# @views.route('/home')
# @login_required
# def home():
#     return render_template("accounts.html", user = current_user)

@views.route('/YourAccounts', methods=['GET','POST'])
@login_required
def YourAccounts():
    if request.method == 'POST':
        n=request.form.get('account_input_name')
        t=request.form.get('account_input_type')
        c=request.form.get('account_input_currency')
        b=request.form.get('account_input_balance')
        d=request.form.get('account_input_description')

        if n=="" or t=="" or c=="" or b=="" or d=="":
            flash("All fields should be filled", category='error')
            return redirect('/YourAccounts')
        else:
            new_account=Account(name=n,type=t,currency=c,balance=b,description=d,user_id=current_user.id)
            db.session.add(new_account)
            db.session.commit()
            return redirect('/YourAccounts')
    else:
        names=Account.query.order_by(Account.name).all()
        return render_template("accounts.html", user = current_user, names=names)

@views.route('/delete/<int:id>')
@login_required
def delete(id):
    account_to_delete=Account.query.get_or_404(id)
    db.session.delete(account_to_delete)
    db.session.commit()
    return redirect('/YourAccounts')



@views.route('/UpcomingPayments')
@login_required
def UpcomingPayments():
    return render_template("upcoming_payments.html", user = current_user)