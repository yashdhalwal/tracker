import pdb
from faker import Faker
import random

from console_functions.resources.resources import retailers, tags

from models.merchant import Merchant
from models.tag import Tag
from models.transaction import Transaction

import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository
import repositories.transaction_repository as transaction_repository


def create_merchant(retailers):
    for retailer in retailers:
        merchant = Merchant(retailer)
        merchant_repository.save(merchant)

def create_tag(tags):
    for tag in tags:
        expense_tag = Tag(tag)
        tag_repository.save(expense_tag)

def create_transaction(min_payment= 1, max_payment = 1000, start_date = '-2y', end_date = 'now'):
    merchants = merchant_repository.select_all()
    tags = tag_repository.select_all()
    fake = Faker()
    random_date = fake.date_between(start_date, end_date)
    random_payment = random.randrange(min_payment, max_payment)
    random_merchant = random.choice(merchants)
    random_tag = random.choice(tags)

    transaction = Transaction(random_date, random_payment, random_merchant, random_tag)
    transaction_repository.save(transaction)


# create_merchant(retailers)

# create_tag(tags)

# for i in range(10):
#     create_transaction()


#Show all transactions
tran_results = transaction_repository.select_all()

for result in tran_results:
    print(result.__dict__)


#Show all tags
tag_results = tag_repository.select_all()

for result in tag_results:
    print(result.__dict__)



#Show all merchants
merch_results = merchant_repository.select_all()

for result in merch_results:
    print(result.__dict__)

pdb.set_trace()