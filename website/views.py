from unicodedata import category
from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import login_required, current_user
from zmq import Message
from .models import Account, Payment, Message, User, Payments_history
from . import db
import datetime
from datetime import timedelta


views=Blueprint('views',__name__)

@views.route('/')
def welcome():
    return render_template("welcome.html")


@views.route('/PrivacyPolicy')
def privacy_policy():
    return render_template("privacy_policy.html")

@views.route('/Support')
def support():
    return render_template("support.html")


# @views.route('/home')
# @login_required
# def home():
#     return render_template("accounts.html", user = current_user)

@views.route('/YourAccounts', methods=['GET','POST'])
@login_required
def YourAccounts():
    accounts=Account.query.filter_by(user_id=current_user.id)
    total_amount=0
    for i in accounts:
        total_amount+=i.balance

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
        return render_template("accounts.html", user = current_user, names=names,total_amount=total_amount)

@views.route('/EditAccount/<int:id>', methods=['GET','POST'])
@login_required
def EditAccount(id):
    account_to_edit=Account.query.get_or_404(id)
    if request.method == 'POST':
        n=request.form.get('edit_name')
        t=request.form.get('edit_type')
        c=request.form.get('edit_currency')
        b=request.form.get('edit_balance')
        d=request.form.get('edit_description')

        if n=="" or t=="" or c=="" or b=="":
            flash("All fields should be filled", category='error')
            return render_template("edit_account.html", user=current_user, a=account_to_edit)

        else:
            account_to_edit.name=n
            account_to_edit.type=t
            account_to_edit.currency=c
            account_to_edit.balance=b
            account_to_edit.description=d
            
            db.session.commit()
            return redirect('/YourAccounts')

    else:
        return render_template("edit_account.html", user=current_user, a=account_to_edit)

@views.route('/AddTransaction/<int:id>', methods=['GET','POST'])
@login_required
def AddTransaction(id):
    account_to_change=Account.query.get_or_404(id)
    if request.method=='POST':
        a=request.form.get('transaction_amount')
        t=request.form.get('transaction_type')

        if a=="" or t=="":
            flash("All fields should be filled", category='error')
            return render_template("add_transaction.html", user=current_user, a=account_to_change)

        else:
            if t=="deposit":
                account_to_change.balance=account_to_change.balance + float(a)
            else:
                if t=="withdrawal":
                    account_to_change.balance=account_to_change.balance - float(a)
            db.session.commit()
            return redirect('/YourAccounts')
    
    return render_template("add_transaction.html", user=current_user, a=account_to_change)


        
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
    accounts=Account.query.filter_by(user_id=current_user.id)
    total_amount=0
    for i in accounts:
        total_amount+=i.balance
    if Account.query.filter_by(user_id=current_user.id).count()!=0:
        if request.method == 'POST':
            a=request.form.get('payment_input_amount')
            b=request.form.get('account_payments')
            t=request.form.get('payment_input_type')
            c=request.form.get('payment_input_currency')
            dd=request.form.get('payment_input_duedate')
            d=request.form.get('payment_input_description')
            dd=dd.split("-")
            
            try:
                
                dd=datetime.date(int(dd[0]),int(dd[1]),int(dd[2]))
            except:
                flash("All fields should be filled", category='error')
                return redirect('/UpcomingPayments')

            if t=="recurring":
                p=request.form.get('payment_input_period')
                if a=="" or t=="" or c=="" or dd=="" or p=="":
                    flash("All fields should be filled", category='error')
                    return redirect('/UpcomingPayments')
            else:
                p=""
                if a=="" or t=="" or c=="" or dd=="":
                    flash("All fields should be filled", category='error')
                    return redirect('/UpcomingPayments')

            new_payment=Payment(amount=a,type=t,period=p,currency=c,duedate=dd,description=d,payment_accountid=b,user_id=current_user.id)
            db.session.add(new_payment)
            db.session.commit()
            return redirect('/UpcomingPayments')
       
        amounts=Payment.query.order_by(Payment.amount).all()
        return render_template("upcoming_payments.html", user = current_user, amounts=amounts,date=datetime.date.today(),total_amount=total_amount)
    else:
        flash('You must create an account first',category='error')
        amounts=Payment.query.order_by(Payment.amount).all()
        return render_template("upcoming_payments.html", user = current_user, amounts=amounts, date=datetime.date.today(),total_amount=total_amount)


@views.route('/SetAsPaid/<int:id>',methods=['GET','POST'])
@login_required
def SetAsPaid(id):
    
    
    payment=Payment.query.get_or_404(id)
    
        
    if request.method=="GET":
        accountid_to_withdaw=Account.query.get_or_404(payment.payment_accountid)
        accountid_to_withdaw.balance-=payment.amount
        payment_h=Payments_history(amount=payment.amount,currency=payment.currency,paiddate=datetime.date.today(),user_id=current_user.id)
        if payment.type=="recurring":
            if payment.period=="weekly":
                payment.duedate=payment.duedate+timedelta(days=7)
            else:
                if payment.period=="monthly":
                    payment.duedate=payment.duedate+timedelta(days=30)
                else:
                    if payment.period=="yearly":
                        payment.duedate=payment.duedate+timedelta(days=365)
        else:
            db.session.delete(payment)
            
        db.session.add(payment_h) 
        db.session.commit()

        return redirect('/UpcomingPayments')
    



@views.route('/DeletePayment/<int:id>')
@login_required
def DeletePayment(id):
    payment_to_delete=Payment.query.get_or_404(id)
    db.session.delete(payment_to_delete)
    db.session.commit()
    return redirect('/UpcomingPayments')

@views.route('/Inbox', methods=['GET','POST'])
@login_required
def Inbox():
    accounts=Account.query.filter_by(user_id=current_user.id)
    total_amount=0
    for i in accounts:
        total_amount+=i.balance
    if request.method=='POST':
        a=request.form.get('message_destinator_email')
        b=request.form.get('message_content')
        try:
            desti_id=User.query.filter_by(email=a).first().id
            message=Message(sender_name=current_user.firstname+' '+current_user.lastname,content=b,user_id=desti_id)
            db.session.add(message)
            db.session.commit()
            
        except:
            flash('Email not found',category='error')
        return redirect('/Inbox')

        
    else:
        content=Message.query.count()
        return render_template("inbox.html", user = current_user, content=content,total_amount=total_amount)
@views.route('/DeleteMessage/<int:id>')
@login_required
def DeleteMessage(id):
    db.session.delete(Message.query.get(id))
    db.session.commit()
    return redirect('/Inbox')

@views.route('/Graph')
@login_required
def Graph():
    accounts=Account.query.filter_by(user_id=current_user.id)
    total_amount=0
    for i in accounts:
        total_amount+=i.balance
    history=Payments_history.query.filter_by(user_id=current_user.id).all()
    data=[]
    for i in history:
        data.append([str(i.paiddate),i.amount])
    xaxis=[]
    yaxis=[]
    for i in data:
        if i[0] not in xaxis:
           
            xaxis.append(i[0])
    for i in xaxis:
        s=0
        for j in data:
            if i==j[0]:
                s+=j[1]
        yaxis.append(s)
        
    
    return render_template('graphs.html',user=current_user,xaxis=xaxis,yaxis=yaxis,history=history,total_amount=total_amount)


