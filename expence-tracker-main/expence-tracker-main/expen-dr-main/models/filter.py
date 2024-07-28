class Filter:
    def __init__(self, start_date, end_date, merchant_id = None, tag_id = None):
        self.start_date = start_date
        self.end_date = end_date
        self.merchant_id = merchant_id
        self.tag_id = tag_id