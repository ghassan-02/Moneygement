from flask import Blueprint, render_template, flash, request, redirect
from flask_login import login_required, current_user
from .models import Account, Payment
from . import db
import datetime


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

        if n=="" or t=="" or c=="" or b=="":
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

@views.route('/DeleteAccount/<int:id>')
@login_required
def DeleteAccount(id):
    account_to_delete=Account.query.get_or_404(id)
    db.session.delete(account_to_delete)
    db.session.commit()
    return redirect('/YourAccounts')



@views.route('/UpcomingPayments', methods=['GET','POST'])
@login_required
def UpcomingPayments():
    if request.method == 'POST':
        a=request.form.get('payment_input_amount')
        t=request.form.get('payment_input_type')
        c=request.form.get('payment_input_currency')
        dd=request.form.get('payment_input_duedate')
        d=request.form.get('payment_input_description')
        dd=dd.split("-")
        dd=datetime.date(int(dd[0]),int(dd[1]),int(dd[2]))

        if a=="" or t=="" or c=="" or dd=="":
            flash("All fields should be filled", category='error')
            return redirect('/UpcomingPayments')
        else:
            new_payment=Payment(amount=a,type=t,currency=c,duedate=dd,description=d,user_id=current_user.id)
            db.session.add(new_payment)
            db.session.commit()
            return redirect('/UpcomingPayments')
    else:
        amounts=Payment.query.order_by(Payment.amount).all()
        return render_template("upcoming_payments.html", user = current_user, amounts=amounts, date=datetime.date.today())

@views.route('/DeletePayment/<int:id>')
@login_required
def DeletePayment(id):
    payment_to_delete=Payment.query.get_or_404(id)
    db.session.delete(payment_to_delete)
    db.session.commit()
    return redirect('/UpcomingPayments')
    