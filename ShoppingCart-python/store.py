import yaml

from item import Item
from shopping_cart import ShoppingCart
from errors import ItemNotExistError, ItemAlreadyExistsError, TooManyMatchesError


class Store:
    def __init__(self, path):
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        return self._items

    def search_by_name(self, item_name: str) -> list:
        # we need to check if the item to add is not already in the cart
        # a includes all items with the name to be search
        a = [product for product in self.get_items() if item_name in product.name and product.name
             not in self._shopping_cart.cart]
        # we want to return a list which is sorted first by tags later by name
        return sorted(a, key=lambda x: (self.sort_by_tag(x), x.name))

    # help function that returns the number of all the common tags for item in the shopping cart
    def sort_by_tag(self, item):
        count = 0
        a = [hashtag for item in self._shopping_cart.cart.values() for hashtag in item.hashtags]
        for tag in item.hashtags:
            count -= a.count(tag)
        return count

    def search_by_hashtag(self, hashtag: str) -> list:
        # crate a list name lst that contains all items that share the same hashtag name.
        # notice that only items with the exact hashtag name is added not like search by name func
        lst = [item for item in self.get_items() if item not in self._shopping_cart.cart.values() and
               hashtag in item.hashtags]
        # return the list ordered first by tags later by items name using the help func
        return sorted(lst, key=lambda x: (self.sort_by_tag(x), x.name))

    def add_item(self, item_name: str):
        # first we look for the item with search by name func and save the result list to a list name item_list
        item_list = self.search_by_name(item_name)
        # raise errors if there are any
        if item_name in self._shopping_cart.cart:
            raise ItemAlreadyExistsError()
        elif len(item_list) == 0:
            raise ItemNotExistError()
        elif len(item_list) > 1:
            raise TooManyMatchesError()
        # if no errors we add the item to cart
        else:
            self._shopping_cart.add_item(self.search_by_name(item_name)[0])

    def remove_item(self, item_name: str):
        # we crate a item_list list for keeping the item to remove(if any)
        item_list = [x for x in self._shopping_cart.cart if item_name in x]
        if len(item_list) == 0:
            raise ItemNotExistError()
        elif len(item_list) > 1:
            raise TooManyMatchesError()
        else:
            self._shopping_cart.remove_item(item_list[0])
        # using the get subtotal func that we crate in shopping_cart class
    def checkout(self) -> int:
        return self._shopping_cart.get_subtotal()
