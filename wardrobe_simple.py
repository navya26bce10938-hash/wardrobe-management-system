wardrobe = {}
item_id_counter = 0

def add_item(name, category, color=None):
    global item_id_counter
    item_id_counter += 1
    item = {
        'id': item_id_counter,
        'name': name,
        'category': category,
        'color': color}
    wardrobe[item_id_counter] = item
    print(f"Added item: {name} (ID: {item_id_counter})")

def remove_item(item_id):
    if item_id in wardrobe:
        removed_item = wardrobe.pop(item_id)
        print(f"Removed item: {removed_item['name']} (ID: {item_id})")
    else:
        print(f"Item with ID {item_id} not found.")

def view_wardrobe():
    if not wardrobe:
        print("Your wardrobe is empty.")
        return
    print("Your Wardrobe")
    for item_id, item_details in wardrobe.items():
        color_info = f", Color: {item_details['color']}" 
        if item_details['color']:
            print(f"ID: {item_details['id']}, Name: {item_details['name']}, Category: {item_details['category']}{color_info}")
        else:
            print("Not available ")

add_item("Blue T-shirt", "shirt", "blue")
add_item("Denim Jeans", "pants")
add_item("Summer Dress", "dress", "floral")
add_item("Leather Jacket", "outerwear", "black")

view_wardrobe()

remove_item(2)

view_wardrobe()

remove_item(99)
