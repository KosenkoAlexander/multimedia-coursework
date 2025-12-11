class CustomPaginated:
    def __init__(self, header, rows, per_page = 0): #per_page = 0 means no max count
        self.header = header
        self.rows = rows
        self.per_page = per_page
        self.page = 0
        self.pages = len(rows)//per_page+(len(rows)%per_page!=0) if per_page else 1

    def get_current_items(self):
        start = self.page*self.per_page
        return self.rows[start:start+self.per_page]

    def next_page_num(self):
        result = self.page+1
        return result if result<self.pages else None

    def prev_page_num(self):
        return self.page-1 if self.page else None

    def set_per_page(self, per_page):
        self.per_page = per_page
        self.pages = len(self.rows)//per_page+(len(self.rows)%per_page!=0) if per_page else 1
        if self.page>=self.pages:
            self.page = self.pages-1

    def set_page(self, page):
        if page>=0 and page<self.pages:
            self.page = page
        else:
            self.page = 0
