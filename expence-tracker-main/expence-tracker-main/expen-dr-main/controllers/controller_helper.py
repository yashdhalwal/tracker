import repositories.transaction_repository as transaction_repository

def select_db_query(filter):
    if filter.merchant_id:
        if filter.tag_id:
            filtered_transactions = transaction_repository.select_by_date_merchant_tag(filter.start_date, filter.end_date, filter.merchant_id, filter.tag_id)
        else:
            filtered_transactions = transaction_repository.select_by_date_merchant(filter.start_date, filter.end_date, filter.merchant_id)
    else:
        if filter.tag_id:
            filtered_transactions = transaction_repository.select_by_date_tag(filter.start_date, filter.end_date, filter.tag_id)
        else:
            filtered_transactions = transaction_repository.select_by_date(filter.start_date, filter.end_date)

    return filtered_transactions

def no_value_checker(form_input):
    if form_input == "":
        return None;
    return form_input


