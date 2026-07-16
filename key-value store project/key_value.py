# ─────────────────────────────────────────────────────────────
# SDE Store Inventory
#
# This file grows across SDE lessons 11–13 and is polished in L14.
# ─────────────────────────────────────────────────────────────

import json
import random


class Product:
    """Represents one inventory item."""

    def __init__(self, product_type, price, total, color, size, brand):
        # Store the item's basic details and assign it a random ID.
        self.product_type = product_type
        self.price = price
        self.total = total
        self.color = color
        self.size = size
        self.brand = brand
        self.prod_id = random.randint(1000, 5000)

    def describe(self):
        """Return a nicely formatted summary of the product."""
        return (
            f"ID: {self.prod_id} | TYPE: {self.product_type} | PRICE: {self.price} | "
            f"TOTAL: {self.total} | COLOR: {self.color} | SIZE(in): {self.size} | BRAND: {self.brand}"
        )

    def to_dict(self):
        """Convert the product into a JSON-friendly dictionary."""
        return {
            "prod_id": self.prod_id,
            "product_type": self.product_type,
            "price": self.price,
            "total": self.total,
            "color": self.color,
            "size": self.size,
            "brand": self.brand,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Product object from saved JSON data."""
        product = cls(
            data["product_type"],
            data["price"],
            data["total"],
            data["color"],
            data["size"],
            data["brand"],
        )
        product.prod_id = data.get("prod_id", product.prod_id)
        return product


class Store:
    """Manages the inventory and handles save/load behavior."""

    def __init__(self):
        # Start with an empty inventory dictionary.
        self.inventory = {}

    def display_inventory(self):
        """Print every item currently in the inventory."""
        if not self.inventory:
            print("Your inventory is empty.")
            return

        for item_id, item in self.inventory.items():
            print(item.describe())

    def add_product(self, product_type, price, total, color, size, brand):
        """Create a Product object and add it to the inventory."""
        new_product = Product(product_type, price, total, color, size, brand)
        self.inventory[new_product.prod_id] = new_product
        print(f"Added {product_type} with id {new_product.prod_id}")

    def add_product_from_input(self):
        """Ask the user for product details and add the item."""
        product_type = input("Please enter a product type: ").strip()

        try:
            price = float(input("Please enter a price: "))
        except ValueError:
            print("Sorry, that isn't a proper price. Defaulting to 0.0...")
            price = 0.0

        try:
            total = int(input("Please enter a total amount: "))
        except ValueError:
            print("Sorry, that isn't a proper total. Defaulting to 1...")
            total = 1

        color = input("Please give your item a color: ").strip()

        try:
            size = int(input("Please state the size of your product in inches: "))
        except ValueError:
            print("Sorry, that is an improper size input. Defaulting to 12")
            size = 12

        brand = input("Please name your item's brand: ").strip()

        self.add_product(product_type, price, total, color, size, brand)

    def remove_product(self):
        """Remove an item from the inventory by its ID."""
        try:
            target_id = int(input("What is the ID of the item you want to remove: "))
        except ValueError:
            print("That ID isn't available.")
            return

        if target_id in self.inventory:
            del self.inventory[target_id]
            print(f"Removed item at {target_id}")
        else:
            print("ID not found")

    def word_search(self):
        """Search for products by matching part of their type."""
        if not self.inventory:
            print("Your inventory is empty. Please add a product before searching.")
            return

        target = input("What is the product type of the item you're looking for?: ").strip().lower()
        found_any = False

        for item_id, item in self.inventory.items():
            if target in item.product_type.lower():
                print(f"Found! ID: {item_id} | TYPE: {item.product_type}")
                found_any = True

        if not found_any:
            print("No item was found with that product type.")

    def inventory_sum(self):
        """Show every item and calculate the total inventory value."""
        total_value = 0
        print("\nCurrent inventory:")

        for item_id, item in self.inventory.items():
            print(item.describe())
            total_value += item.price * item.total

        print(f"Total inventory value: {total_value}")

    def save_inventory(self):
        """Save the current inventory to a JSON file."""
        file_name = input("Please name your save file: ").strip()
        full_name = f"{file_name}.json"

        try:
            serializable_inventory = {
                str(item_id): item.to_dict() for item_id, item in self.inventory.items()
            }
            with open(full_name, "w", encoding="utf-8") as file:
                json.dump(serializable_inventory, file, indent=4)
            print(f"Saved inventory to {full_name}")
        except Exception as error:
            print(f"Could not save the file: {error}")

    def load_inventory(self):
        """Load inventory data from a previously saved JSON file."""
        file_name = input("Please name your save file: ").strip()
        full_name = f"{file_name}.json"

        try:
            with open(full_name, "r", encoding="utf-8") as file:
                raw_data = json.load(file)

            loaded_inventory = {}
            for item_id, item_data in raw_data.items():
                loaded_inventory[int(item_id)] = Product.from_dict(item_data)

            self.inventory = loaded_inventory
            print("Inventory loaded successfully.")
        except FileNotFoundError:
            print("File not found. Please check the filename and try again.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file content.")


def display_menu():
    """Show the main menu options to the user."""
    print("\n=== Store Inventory Menu ===")
    print("1. View inventory")
    print("2. Add product")
    print("3. Remove product")
    print("4. Search by product type")
    print("5. Show inventory summary")
    print("6. Save inventory")
    print("7. Load inventory")
    print("8. Exit")


def user_selection(store):
    """Handle the user's menu choice and call the right action."""
    display_menu()

    try:
        response = int(input("Please choose an action: "))
    except ValueError:
        print("That is not a valid option.")
        return True

    if response == 1:
        store.display_inventory()
    elif response == 2:
        store.add_product_from_input()
    elif response == 3:
        store.remove_product()
    elif response == 4:
        store.word_search()
    elif response == 5:
        store.inventory_sum()
    elif response == 6:
        store.save_inventory()
    elif response == 7:
        store.load_inventory()
    elif response == 8:
        print("Goodbye!")
        return False
    else:
        print("That is not a valid option.")

    return True


def main():
    """Run the main program loop."""
    store = Store()
    print("Store inventory ready.")

    running = True
    while running:
        running = user_selection(store)


if __name__ == "__main__":
    main()
