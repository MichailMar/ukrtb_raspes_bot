
class ItemError(Exception):
    def __init__(self, item) -> None:
        self.item = item

    def __str__(self) -> str:
        return "Item {} not found. Check item or cheked connect".format(self.item)

class NotTimeTable(Exception):
    def __init__(self, item, data) -> None:
        self.item = item
        self.data = data
    
    def __str__(self) -> str:
        return "Item {} not time table in {}".format(self.item, self.data)