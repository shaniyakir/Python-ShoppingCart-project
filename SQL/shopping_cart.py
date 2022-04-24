from item import Item
from errors import ItemNotExistError, ItemAlreadyExistsError


# i decided to build the shopping_cart.cart object as a dictionary with the name of the item as the key
class ShoppingCart:
    def __init__(self):
        self.cart = {}

    # add an item to the cart
    def add_item(self, item: Item) -> object:
        if item.name in self.cart:
            raise ItemAlreadyExistsError
        else:
            self.cart[item.name] = item

    # remove item from cart
    def remove_item(self, item_name: str):
        if item_name in self.cart:
            del self.cart[item_name]
        else:
            raise ItemNotExistError

    # returns the sum of all items price
    def get_subtotal(self) -> int:
        sm = 0
        for item in self.cart.values():
            sm += item.price
        return sm
