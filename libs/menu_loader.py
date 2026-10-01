import json
def load_menu():
    with open("menu.json", "r") as f:
        json_data =  json.load(f)
        menu_text =  ""
        for name,price in json_data.items():
            menu_text = menu_text + f" - {name}:  AED{price}\n"
        return menu_text