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
    Item("Apple", 10),
    Item("Banana", 11),
    Item("FakeGameCode", 100),
    Item("MessageToSomeone", 20)
]