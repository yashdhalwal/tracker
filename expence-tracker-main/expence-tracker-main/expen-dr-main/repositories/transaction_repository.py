from db.run_sql import run_sql

from models.transaction import Transaction

import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository


def save(transaction):
    sql = "INSERT INTO transactions (date, merchant_id, tag_id, amount) VALUES (%s, %s, %s, %s) RETURNING id"
    values = [transaction.date, transaction.merchant.id, transaction.tag.id, transaction.amount]
    results  = run_sql(sql, values)
    transaction.id = results[0]['id']
    return transaction

def select_all():

    transactions = []

    sql = "SELECT * FROM transactions"
    results = run_sql(sql)
    
    if results is not None:
        for row in results:
            merchant = merchant_repository.select(row['merchant_id'])
            tag = tag_repository.select(row['tag_id'])
            transaction = Transaction(row['date'], row['amount'], merchant, tag, row['id'])
            transactions.append(transaction)
        return transactions

def select(id):
    sql = "SELECT * FROM transactions WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        merchant = merchant_repository.select(result['merchant_id'])
        tag = tag_repository.select(result['tag_id'])
        transaction = Transaction(result['date'], result['amount'], merchant, tag, result['id'])
        return transaction

def select_filter(start_date, end_date, merchant_id = None, tag_id= None):

    transactions = []

    sql = """

    SELECT * 
    FROM transactions 
    WHERE 
         date BETWEEN %s AND %s
    INTERSECT 
    SELECT *
    FROM transactions
    WHERE 
        (merchant_id IS NULL OR merchant_id = %s)
    INTERSECT 
    SELECT * 
    FROM transactions
    WHERE
        (tag_id IS NULL OR tag_id = %s);
    """
    values = [start_date, end_date, merchant_id, tag_id]
    results = run_sql(sql, values)
    
    if results is not None:
        for row in results:
            merchant = merchant_repository.select(row['merchant_id'])
            tag = tag_repository.select(row['tag_id'])
            transaction = Transaction(row['date'], row['amount'], merchant, tag, row['id'])
            transactions.append(transaction)
    return transactions

def select_by_date(start_date, end_date):
    transactions = []

    sql = "SELECT * FROM transactions WHERE date BETWEEN %s AND %s"
    values = [start_date, end_date]
    results = run_sql(sql, values)

    if results is not None:
        for row in results:
            merchant = merchant_repository.select(row['merchant_id'])
            tag = tag_repository.select(row['tag_id'])
            transaction = Transaction(row['date'], row['amount'], merchant, tag, row['id'])
            transactions.append(transaction)
    return transactions

def select_by_merchant(merchant):
    transactions = []
    sql = "SELECT * FROM transactions WHERE merchant_id = %s"
    values = [merchant.id]
    results = run_sql(sql, values)
    if results is not None:
        for row in results:
            tag = tag_repository.select(row['tag_id'])
            transaction = Transaction(row['date'], row['amount'], merchant, tag, row['id'])
            transactions.append(transaction)
    return transactions

def select_by_tag(tag):
    transactions = []
    sql = "SELECT * FROM transactions WHERE tag_id = %s"
    values = [tag.id]
    results = run_sql(sql, values)

    if results is not None:
        for row in results:
            merchant = merchant_repository.select(row['merchant_id'])
            transaction = Transaction(row['date'], row['amount'], merchant, tag, row['id'])
            transactions.append(transaction)
    return transactions

def select_by_date_tag(start_date, end_date, tag_id):
    transactions = []
    sql = "SELECT * FROM transactions WHERE (date BETWEEN %s AND %s) AND (tag_id = %s)"
    values = [start_date, end_date, tag_id]
    results = run_sql(sql, values)
    if results is not None:
        for row in results:
            merchant = merchant_repository.select(row['merchant_id'])
            tag = tag_repository.select(row['tag_id'])
            transaction = Transaction(row['date'], row['amount'], merchant, tag, row['id'])
            transactions.append(transaction)
    return transactions

def select_by_date_merchant(start_date, end_date, merchant_id):
    transactions = []
    sql = "SELECT * FROM transactions WHERE (date BETWEEN %s AND %s) AND (merchant_id = %s)"
    values = [start_date, end_date, merchant_id]
    results = run_sql(sql, values)

    if results is not None:
        for row in results:
            merchant = merchant_repository.select(row['merchant_id'])
            tag = tag_repository.select(row['tag_id'])
            transaction = Transaction(row['date'], row['amount'], merchant, tag, row['id'])
            transactions.append(transaction)
    return transactions

def select_by_date_merchant_tag(start_date, end_date, merchant_id, tag_id):
    transactions = []
    sql = "SELECT * FROM transactions WHERE (date BETWEEN %s AND %s) AND (merchant_id = %s) AND (tag_id = %s)"
    values = [start_date, end_date, merchant_id, tag_id]
    results = run_sql(sql, values)

    if results is not None:
        for row in results:
            merchant = merchant_repository.select(row['merchant_id'])
            tag = tag_repository.select(row['tag_id'])
            transaction = Transaction(row['date'], row['amount'], merchant, tag, row['id'])
            transactions.append(transaction)
    return transactions

def update_transaction(transaction):
    sql = "UPDATE transactions SET(date, merchant_id, tag_id, amount) = (%s, %s, %s, %s) WHERE id = %s"
    values = [transaction.date, transaction.merchant.id,  transaction.tag.id, transaction.amount, transaction.id]
    run_sql(sql, values)

def delete_all():
    sql = "DELETE FROM transactions"
    run_sql(sql)

def delete(id):
    sql = "DELETE FROM transactions WHERE id = %s"
    values = [id]
    run_sql(sql, values)

