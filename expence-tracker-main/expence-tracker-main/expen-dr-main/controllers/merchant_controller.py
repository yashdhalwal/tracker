from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.merchant import Merchant
from models.transaction import Transaction

import repositories.merchant_repository as merchant_repository
import repositories.transaction_repository as transaction_repository

merchants_blueprint = Blueprint('merchants', __name__)


#Create new merchants
@merchants_blueprint.route('/merchants/new')
def new_merchant():
    return render_template("merchants/new.html")

@merchants_blueprint.route('/merchants', methods=['POST'])
def add_merchant():
    name = request.form['name']
    merchant = Merchant(name)
    merchant_repository.save(merchant)
    return redirect('/merchants')


#Merchant Index
@merchants_blueprint.route('/merchants')
def merchants():
    merchants = merchant_repository.select_all()
    return render_template('merchants/index.html', merchants=merchants)

@merchants_blueprint.route('/merchants/<id>')
def show(id):
    merchant = merchant_repository.select(id)
    transactions = transaction_repository.select_by_merchant(merchant)
    total_spent = Transaction.total_spending(transactions)
    return render_template('merchants/show.html', merchant=merchant, transactions=transactions, total_spent=total_spent)


#Update Merchant
@merchants_blueprint.route('/merchants/<id>/edit')
def edit_merchant(id):
    merchant = merchant_repository.select(id)
    return render_template('merchants/edit.html', merchant=merchant)

@merchants_blueprint.route('/merchants/<id>', methods=['POST'])
def update_merchant(id):
    name = request.form['name']
    merchant = Merchant(name, id)
    merchant_repository.update_merchant(merchant)
    return redirect('/merchants')


#Delete Merchant
@merchants_blueprint.route('/merchants/<id>/delete', methods=['POST'])
def delete_merchant(id):
    merchant_repository.delete(id)
    return redirect('/merchants')
