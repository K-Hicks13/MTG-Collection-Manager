from transaction_service import trade_cards_with_transaction

result = trade_cards_with_transaction(
    event_date="2026-09-29",
    person_place="Rollback Test",
    notes="This trade should fail and rollback",
    outgoing_cards=[
        {
            "collection_id": 2,
            "quantity": 1,
            "price_per_card": None,
            "currency": None
        }
    ],
    incoming_cards=[
        {
            "card_id": 99999,
            "location_id": 1,
            "quantity": 1,
            "foil": False,
            "card_condition": "Near Mint",
            "price_per_card": None,
            "currency": None
        }
    ]
)

print(result)