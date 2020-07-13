class Item:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost


class Items:
    def __init__(self):
        self.allItems = []

    def buyItem(self, name, balance):
        for i in self.allItems:
            if(i.name.lower() == name.lower() and balance >= i.cost):
                return True, balance - i.cost
        return False, balance

items = Items() #Instantiation

items.allItems = [
    Item("apple", 10),
    Item("banana", 11),
    Item("fakecode", 100),
    Item("messagetosomeone", 20)
]