from flask import Flask, render_template, request, redirect
from flask import Blueprint

from models.tag import Tag
from models.transaction import Transaction

import repositories.tag_repository as tag_repository
import repositories.transaction_repository as transaction_repository

tags_blueprint = Blueprint("tags", __name__)


#Create
@tags_blueprint.route('/tags/new')
def new_tag():
    return render_template("tags/new.html")

@tags_blueprint.route('/tags', methods=['POST'])
def add_tag():
    name = request.form['name'].capitalize()
    tag = Tag(name)
    tag_repository.save(tag)
    return redirect('/tags')


#Tag Index
@tags_blueprint.route('/tags')
def tags():
    tags = tag_repository.select_all()
    return render_template('tags/index.html', tags=tags)

@tags_blueprint.route('/tags/<id>')
def show(id):
    tag = tag_repository.select(id)
    transactions = transaction_repository.select_by_tag(tag)
    total_spent = Transaction.total_spending(transactions)
    return render_template('tags/show.html', tag=tag, transactions=transactions, total_spent=total_spent)


#Update Tag
@tags_blueprint.route('/tags/<id>/edit')
def edit_tag(id): 
    tag = tag_repository.select(id)
    return render_template('tags/edit.html', tag=tag)

@tags_blueprint.route('/tags/<id>', methods=['POST'])
def update_tag(id):
    name = request.form['name']
    tag = Tag(name, id)
    tag_repository.update_tag(tag)
    return redirect('/tags')


#Delete Tag
@tags_blueprint.route('/tags/<id>/delete', methods=['POST'])
def delete_tag(id):
    tag_repository.delete(id)
    return redirect('/tags')
