from api.scryfall_api import get_card_by_scryfall_id
from card_database import get_or_create_set
from card_database import get_card
from card_database import add_card
from services.transaction_service import add_cards_with_transaction


def get_or_create_card_from_scryfall(scryfall_id):
    card_data = get_card_by_scryfall_id(scryfall_id)

    if card_data is None:
        return None

    set_id = get_or_create_set(
        card_data["set_name"],
        card_data["set_code"],
        card_data["set_year"]
    )

    if set_id is False:
        return None

    existing_card = get_card(
        card_data["name"],
        card_data["collector_number"],
        set_id,
        card_data["card_language"]
    )

    if existing_card is not None:
        card_id = existing_card["Card_ID"]
    else:
        card_id = add_card(card_data, set_id)

        if card_id is False:
            return None

    return card_id


def add_scryfall_card_to_collection(
        scryfall_id,
        location_id,
        quantity,
        foil,
        card_condition,
        event_date,
        transaction_type,
        person_place,
        notes,
        price_per_card,
        currency
):
    if quantity < 1:
        return None

    allowed_conditions = [
        "Near Mint",
        "Lightly Played",
        "Moderately Played",
        "Heavily Played",
        "Damaged"
    ]

    if card_condition not in allowed_conditions:
        return None

    allowed_transaction_types = [
        "Purchase",
        "Trade",
        "Gift",
        "Initial Inventory",
        "Other"
    ]

    if transaction_type not in allowed_transaction_types:
        return None

    if (price_per_card is not None and currency is None) or (price_per_card is None and currency is not None):
        return None

    card_id = get_or_create_card_from_scryfall(scryfall_id)

    if card_id is None:
        return None

    result = add_cards_with_transaction(
        event_date,
        transaction_type,
        person_place,
        notes,
        card_id,
        location_id,
        quantity,
        foil,
        card_condition,
        price_per_card,
        currency
    )

    return result