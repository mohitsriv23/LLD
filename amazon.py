import uuid
from typing import List, Dict

# User Management
class User:
    def __init__(self, name: str, email: str, password: str):
        self.user_id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = password  # In real applications, use password hashing
        self.cart = Cart(self.user_id)
        self.orders = []

    def add_to_cart(self, product, quantity):
        self.cart.add_item(product, quantity)

    def checkout(self):
        order = self.cart.checkout()
        if order:
            self.orders.append(order)

# Product Management
class Product:
    def __init__(self, name: str, price: float, stock: int, category: str):
        self.product_id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category
        self.reviews = []

    def update_stock(self, quantity):
        if quantity <= self.stock:
            self.stock -= quantity
            return True
        return False

    def add_review(self, user, rating, comment):
        self.reviews.append({"user": user.name, "rating": rating, "comment": comment})

# Cart Management
class Cart:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.items = {}

    def add_item(self, product: Product, quantity: int):
        if product.stock >= quantity:
            self.items[product] = self.items.get(product, 0) + quantity
        else:
            print("Insufficient stock!")

    def remove_item(self, product):
        if product in self.items:
            del self.items[product]

    def checkout(self):
        if not self.items:
            print("Cart is empty!")
            return None
        total_price = sum(product.price * quantity for product, quantity in self.items.items())
        order = Order(self.user_id, self.items, total_price)
        for product, quantity in self.items.items():
            product.update_stock(quantity)
        self.items.clear()
        return order

# Order Management
class Order:
    def __init__(self, user_id: str, items: Dict[Product, int], total_price: float):
        self.order_id = str(uuid.uuid4())
        self.user_id = user_id
        self.items = items
        self.total_price = total_price
        self.status = "Pending"

    def process_payment(self, payment_method: str):
        # Mock payment processing
        print(f"Processing {payment_method} payment for {self.total_price}")
        self.status = "Paid"

# Inventory Management
class Inventory:
    def __init__(self):
        self.products = {}

    def add_product(self, product: Product):
        self.products[product.product_id] = product

    def list_products(self):
        return [p.__dict__ for p in self.products.values()]

# Testing
if __name__ == "__main__":
    inventory = Inventory()
    user = User("Alice", "alice@example.com", "password")
    
    product1 = Product("Laptop", 1000.0, 10, "Electronics")
    product2 = Product("Phone", 500.0, 20, "Electronics")
    
    inventory.add_product(product1)
    inventory.add_product(product2)
    
    user.add_to_cart(product1, 1)
    user.checkout()
    user.orders[0].process_payment("Credit Card")
    
    print("Order details:", user.orders[0].__dict__)
