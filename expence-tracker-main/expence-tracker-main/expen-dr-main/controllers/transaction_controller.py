from urllib.request import Request
from flask import Flask, render_template, request, redirect
from flask import Blueprint
import datetime

from models.transaction import Transaction
from models.objects import filter 
from controllers.controller_helper import *


import repositories.transaction_repository as transaction_repository
import repositories.tag_repository as tag_repository
import repositories.merchant_repository as merchant_repository

transaction_blueprint = Blueprint("transaction", __name__)

#Create transaction
@transaction_blueprint.route('/transactions/new')
def new_transaction():
    tags = tag_repository.select_all()
    merchants = merchant_repository.select_all()
    return render_template('transactions/new.html', tags=tags, merchants=merchants)

@transaction_blueprint.route('/transactions', methods=['POST'])
def add_transaction():    
    date = request.form['date']
    amount = request.form['amount']
    merchant_id = request.form['merchant']
    tag_id = request.form['tag']

    merchant = merchant_repository.select(merchant_id)
    tag = tag_repository.select(tag_id)

    transaction = Transaction(date, amount, merchant, tag)
    transaction_repository.save(transaction)
    return redirect('/transactions')

#transaction main
@transaction_blueprint.route('/transactions')
def transactions():
    all_tags = tag_repository.select_all()
    all_merchants = merchant_repository.select_all()


    filtered_transactions = select_db_query(filter)
    filtered_transactions.sort(key=lambda transaction: transaction.date, reverse=True)
    total_spent = Transaction.total_spending(filtered_transactions) 

    for transaction in filtered_transactions:
        transaction = transaction.amount_formatted()
    return render_template('transactions/index.html', filtered_transactions=filtered_transactions, total_spent=total_spent, filter=filter, all_tags=all_tags, all_merchants=all_merchants)

#Update transaction filter
@transaction_blueprint.route('/transactions/change_date', methods=['POST'])
def change_date_transactions():
    filter.start_date = request.form['start_date']
    filter.end_date = request.form['end_date']

    filter.merchant_id = no_value_checker(request.form['merchant'])
    filter.tag_id = no_value_checker(request.form['tag'])
    
    return redirect('/transactions')



@transaction_blueprint.route('/transactions/<id>')
def show(id):
    transaction = transaction_repository.select(id)
    daily_transactions = transaction_repository.select_by_date(transaction.date, transaction.date)
    total_spent = Transaction.total_spending(daily_transactions)
    
    return render_template('transactions/show.html', transaction=transaction, daily_transactions=daily_transactions, total_spent=total_spent)

#Update
@transaction_blueprint.route('/transactions/<id>/edit')
def edit_transaction(id):
    transaction = transaction_repository.select(id)
    tags = tag_repository.select_all()
    merchants = merchant_repository.select_all()
    return render_template('transactions/edit.html', transaction=transaction, merchants=merchants, tags=tags)


@transaction_blueprint.route('/transactions/<id>', methods=['POST'])
def update_transaction(id):
    date = request.form['date']
    amount = request.form['amount']
    merchant_id = request.form['merchant']
    tag_id = request.form['tag']

    merchant = merchant_repository.select(merchant_id)
    tag = tag_repository.select(tag_id)

    transaction = Transaction(date, amount, merchant, tag, id)
    transaction_repository.update_transaction(transaction)
    return redirect('/transactions')


#Delete
@transaction_blueprint.route('/transactions/<id>/delete', methods=['POST'])
def delete_transaction(id):
    transaction_repository.delete(id)
    return redirect('/transactions')
