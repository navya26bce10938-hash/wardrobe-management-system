CATEGORIES = ("tops", "bottoms", "shoes", "accessories") 
wardrobe = {}                                            
next_id = 1
print("**************************WELCOME TO YOUR WARDROBE OF THE WEEK🛍️*************************************" )
while True:
    print("1. Add item " 
          " 2. View wardrobe  " 
          "3. Filter by category " 
          " 4. Remove item  " 
          "5. Exit")
    
    choice = input("Choose: ")
 
    if choice == "1":
        name = input("Item name: ")
        category = input("Category (tops/bottoms/shoes/accessories): ").lower()
 
        if category not in CATEGORIES:
            print("Invalid category:Item not added.")
        else:
            item = {
                "name": name,
                "category": category,
                "colour": input("Colour: "),
                "brand": input("Brand: "),
                "season": input("Season (summer/winter/monsoon/all): "),
                "formality": input("Formality (casual/formal): "),
                "weather": input("Weather (hot/cold/rainy/any): "),
                "photo": input("Photo file name (e.g. shirt.jpg, or leave blank): "),
            }
            if item["photo"] == "":
                item["photo"] = "Not available"
 
            wardrobe[next_id] = item
            print("Added", name, "with ID", next_id)
            next_id += 1
 
    elif choice == "2":
        if len(wardrobe) == 0:
            print("Your wardrobe is empty.")
        else:
            for item_id, item in wardrobe.items():
                print(item_id, "|", item["name"], "|", item["category"], "|",
                      item["colour"], "|", item["brand"], "|", item["season"], "|",
                      item["formality"], "|", item["weather"], "|", item["photo"])
 
    elif choice == "3":
        wanted = input("Category to show: ").lower()
        found = []                                  
        for item_id, item in wardrobe.items():
            if item["category"] == wanted:
                found.append(item["name"])
 
        if len(found) > 0:
            print("Items in", wanted, ":", ", ".join(found))
        else:
            print("No items found in that category.")
 
    elif choice == "4":
        remove_id = input("Enter ID to remove: ")
        if remove_id.isdigit() and int(remove_id) in wardrobe:
            removed = wardrobe.pop(int(remove_id))
            print("Removed", removed["name"])
        else:
            print("Item not found.")
 
    elif choice == "5":
        print("****************************GOODBYE YOU DIVA😘**********************************")
    
        break
 
    else:
        print("Invalid choice. Try again.")
