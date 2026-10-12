import requests


def get_card_from_scryfall(card_name):
    # Gets a card using its name
    url = "https://api.scryfall.com/cards/named"

    headers = {
        "User-Agent": "MTGCollectionApp/1.0",
        "Accept": "application/json"
    }

    params = {
        "exact": card_name
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print("Scryfall request failed:", response.status_code)
        return None

    card_data = response.json()

    colour_order = ["W", "U", "B", "R", "G"]
    sorted_colour_identity = sorted(
        card_data["color_identity"],
        key=lambda colour: colour_order.index(colour)
    )

    colour_identity = "".join(sorted_colour_identity)

    type_parts = card_data["type_line"].split(" — ")

    types = type_parts[0].split()

    if len(type_parts) > 1:
        subtypes = type_parts[1].split()
    else:
        subtypes = []

    return {
        "name": card_data["name"],
        "collector_number": card_data["collector_number"],
        "cmc": card_data["cmc"],
        "colors": card_data["colors"],
        "color_identity": colour_identity,
        "rarity": card_data["rarity"],
        "card_language": card_data["lang"],
        "types": types,
        "subtypes": subtypes,
        "set_code": card_data["set"],
        "set_name": card_data["set_name"],
        "set_year": card_data["released_at"][:4],
        "market_price": card_data["prices"]["usd"],
        "foil_market_price": card_data["prices"]["usd_foil"]
    }


def search_card_printings(card_name):
    # Gets the list of printings for the user to choose from
    url = "https://api.scryfall.com/cards/search"

    headers = {
        "User-Agent": "MTGCollectionApp/1.0",
        "Accept": "application/json"
    }

    params = {
        "q": f'!"{card_name}"',
        "unique": "prints"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print("Scryfall request failed:", response.status_code)
        return None

    results = response.json()

    printings = []

    for printing in results["data"]:
        if "image_uris" in printing:
            image_url = printing["image_uris"]["normal"]
        else:
            image_url = printing["card_faces"][0]["image_uris"]["normal"]

        printing_data = {"id": printing["id"],
                         "name": printing["name"],
                         "set_name": printing["set_name"],
                         "collector_number": printing["collector_number"],
                         "year": printing["released_at"][:4],
                         "image_url": image_url
        }

        printings.append(printing_data)

    return printings


def get_card_by_scryfall_id(card_id):
    # Gets the exact printing the user selected

    url = f"https://api.scryfall.com/cards/{card_id}"

    headers = {
        "User-Agent": "MTGCollectionApp/1.0",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Scryfall request failed:", response.status_code)
        return None

    card_data = response.json()

    colour_order = ["W", "U", "B", "R", "G"]
    sorted_colour_identity = sorted(
        card_data["color_identity"],
        key=lambda colour: colour_order.index(colour)
    )

    colour_identity = "".join(sorted_colour_identity)

    if "type_line" in card_data:
        type_line = card_data["type_line"]
    else:
        type_line = card_data["card_faces"][0]["type_line"]

    type_parts = type_line.split(" — ")
    types = type_parts[0].split()

    if len(type_parts) > 1:
        subtypes = type_parts[1].split()
    else:
        subtypes = []

    if "colors" in card_data:
        colors = card_data["colors"]
    else:
        colors = set()

        for face in card_data["card_faces"]:
            for color in face["colors"]:
                colors.add(color)

        colors = list(colors)

    if "cmc" in card_data:
        cmc = card_data["cmc"]
    else:
        cmc = card_data["card_faces"][0]["cmc"]

    return {
            "name": card_data["name"],
            "collector_number": card_data["collector_number"],
            "cmc": cmc,
            "colors": colors,
            "color_identity": colour_identity,
            "rarity": card_data["rarity"],
            "card_language": card_data["lang"],
            "types": types,
            "subtypes": subtypes,
            "set_code": card_data["set"],
            "set_name": card_data["set_name"],
            "set_year": card_data["released_at"][:4],
            "market_price": card_data["prices"]["usd"],
            "foil_market_price": card_data["prices"]["usd_foil"]
        }