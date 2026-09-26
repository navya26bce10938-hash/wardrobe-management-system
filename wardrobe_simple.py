"""
Simple Wardrobe Manager (beginner version)
-------------------------------------------
This program helps you keep track of your clothes.

It uses:
- a list of dictionaries to store the clothes (no classes needed)
- simple functions for each feature
- a while loop with a menu so you can keep using the program

Features:
1. Add a clothing item
2. View all items
3. Search / filter items
4. Log that you wore an item (usage tracking)
5. Get an outfit suggestion
6. Delete an item
"""

import json
import random
import os
from datetime import date

# This is where we save your clothes so they are still there next time.
DATA_FILE = "wardrobe_data.json"

# The choices a user can pick from. Keeping these in one place makes
# it easy to change later.
CATEGORIES = ["Top", "Bottom", "Dress", "Outerwear", "Shoes", "Accessory"]
SEASONS = ["Spring", "Summer", "Fall", "Winter", "All-season"]
OCCASIONS = ["Casual", "Work", "Formal", "Athletic"]


# ---------------------------------------------------------
# Loading and saving
# ---------------------------------------------------------

def load_wardrobe():
    """Load the list of clothes from the save file, or start empty."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []  # no file yet, start with an empty closet


def save_wardrobe(wardrobe):
    """Save the current list of clothes to the file."""
    with open(DATA_FILE, "w") as f:
        json.dump(wardrobe, f, indent=2)


# ---------------------------------------------------------
# Small helper for asking the user to pick from a list
# ---------------------------------------------------------

def choose_from_list(question, options):
    print(question)
    for i, option in enumerate(options, start=1):
        print(f"  {i}. {option}")
    choice = input("Enter a number: ")
    # Turn the text into a number safely
    if choice.isdigit() and 1 <= int(choice) <= len(options):
        return options[int(choice) - 1]
    else:
        print("Invalid choice, picking the first option by default.")
        return options[0]


# ---------------------------------------------------------
# Feature 1: Add an item
# ---------------------------------------------------------

def add_item(wardrobe):
    print("\n--- Add a new clothing item ---")
    name = input("Name (e.g. Blue jeans): ")
    category = choose_from_list("Category:", CATEGORIES)
    season = choose_from_list("Season:", SEASONS)
    occasion = choose_from_list("Occasion:", OCCASIONS)

    # Each item is just a dictionary of information
    item = {
        "name": name,
        "category": category,
        "season": season,
        "occasion": occasion,
        "times_worn": 0,       # usage tracking starts at 0
        "last_worn": None,
    }

    wardrobe.append(item)
    save_wardrobe(wardrobe)
    print(f"Added '{name}' to your wardrobe!\n")


# ---------------------------------------------------------
# Feature 2: View all items
# ---------------------------------------------------------

def view_items(wardrobe):
    print("\n--- Your Wardrobe ---")
    if len(wardrobe) == 0:
        print("Your wardrobe is empty. Add something first!")
        return

    for i, item in enumerate(wardrobe, start=1):
        last_worn = item["last_worn"] if item["last_worn"] else "never"
        print(f"{i}. {item['name']} | {item['category']} | {item['season']} | "
              f"{item['occasion']} | worn {item['times_worn']}x | last worn: {last_worn}")
    print()


# ---------------------------------------------------------
# Feature 3: Search / filter items
# ---------------------------------------------------------

def search_items(wardrobe):
    print("\n--- Search Your Wardrobe ---")
    print("Leave a box blank to skip that filter.")
    category = input(f"Category {CATEGORIES}: ")
    season = input(f"Season {SEASONS}: ")
    keyword = input("Search by name (any word): ")

    results = []
    for item in wardrobe:
        # Skip this item if it does not match a filter the user typed in
        if category and item["category"].lower() != category.lower():
            continue
        if season and item["season"].lower() != season.lower():
            continue
        if keyword and keyword.lower() not in item["name"].lower():
            continue
        results.append(item)

    print(f"\nFound {len(results)} matching item(s):")
    for item in results:
        print(f"- {item['name']} ({item['category']}, {item['season']}, {item['occasion']})")
    print()


# ---------------------------------------------------------
# Feature 4: Log that an item was worn (usage tracking)
# ---------------------------------------------------------

def log_wear(wardrobe):
    view_items(wardrobe)
    if len(wardrobe) == 0:
        return

    choice = input("Which item number did you wear today? ")
    if choice.isdigit() and 1 <= int(choice) <= len(wardrobe):
        item = wardrobe[int(choice) - 1]
        item["times_worn"] += 1
        item["last_worn"] = str(date.today())
        save_wardrobe(wardrobe)
        print(f"Logged a wear for '{item['name']}'. Worn {item['times_worn']}x total.\n")
    else:
        print("That wasn't a valid item number.\n")


# ---------------------------------------------------------
# Feature 5: Outfit suggestion
# ---------------------------------------------------------

def suggest_outfit(wardrobe):
    print("\n--- Outfit Suggestion ---")
    season = choose_from_list("What season is it?", SEASONS)

    # Separate the wardrobe into tops, bottoms and shoes for this season
    tops = [i for i in wardrobe if i["category"] == "Top"
            and (i["season"] == season or i["season"] == "All-season")]
    bottoms = [i for i in wardrobe if i["category"] == "Bottom"
               and (i["season"] == season or i["season"] == "All-season")]
    shoes = [i for i in wardrobe if i["category"] == "Shoes"
             and (i["season"] == season or i["season"] == "All-season")]

    if not tops or not bottoms:
        print("You need at least one top and one bottom for that season to get a suggestion.\n")
        return

    # To encourage variety, prefer items that have been worn the least.
    tops.sort(key=lambda i: i["times_worn"])
    bottoms.sort(key=lambda i: i["times_worn"])

    # Take the 3 least-worn options (or fewer if there aren't 3) and
    # pick randomly among them, so it's not the exact same suggestion every time.
    top_choice = random.choice(tops[:3])
    bottom_choice = random.choice(bottoms[:3])

    print("Today's suggested outfit:")
    print(f"  Top:    {top_choice['name']}")
    print(f"  Bottom: {bottom_choice['name']}")

    if shoes:
        shoes.sort(key=lambda i: i["times_worn"])
        shoe_choice = random.choice(shoes[:3])
        print(f"  Shoes:  {shoe_choice['name']}")
    else:
        shoe_choice = None

    # Offer to log all three as worn today
    log_it = input("\nLog this outfit as worn today? (y/n): ")
    if log_it.lower() == "y":
        for item in [top_choice, bottom_choice, shoe_choice]:
            if item:
                item["times_worn"] += 1
                item["last_worn"] = str(date.today())
        save_wardrobe(wardrobe)
        print("Outfit logged!\n")


# ---------------------------------------------------------
# Feature 6: Delete an item
# ---------------------------------------------------------

def delete_item(wardrobe):
    view_items(wardrobe)
    if len(wardrobe) == 0:
        return

    choice = input("Which item number do you want to delete? ")
    if choice.isdigit() and 1 <= int(choice) <= len(wardrobe):
        removed = wardrobe.pop(int(choice) - 1)
        save_wardrobe(wardrobe)
        print(f"Deleted '{removed['name']}'.\n")
    else:
        print("That wasn't a valid item number.\n")


# ---------------------------------------------------------
# Main program: shows a menu and repeats until the user quits
# ---------------------------------------------------------

def main():
    wardrobe = load_wardrobe()
    print("Welcome to your Wardrobe Manager!")

    while True:
        print("What would you like to do?")
        print("1. Add an item")
        print("2. View all items")
        print("3. Search / filter items")
        print("4. Log that you wore an item")
        print("5. Get an outfit suggestion")
        print("6. Delete an item")
        print("7. Quit")

        choice = input("Enter a number (1-7): ")

        if choice == "1":
            add_item(wardrobe)
        elif choice == "2":
            view_items(wardrobe)
        elif choice == "3":
            search_items(wardrobe)
        elif choice == "4":
            log_wear(wardrobe)
        elif choice == "5":
            suggest_outfit(wardrobe)
        elif choice == "6":
            delete_item(wardrobe)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Please enter a number between 1 and 7.\n")


# This makes sure main() only runs when you run this file directly
if __name__ == "__main__":
    main()
