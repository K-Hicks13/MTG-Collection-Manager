import customtkinter as ctk
from tkinter import ttk


def build_collection_tab(collection_tab, heading_font, normal_font, summary_value_font, card_name_font):
    # Building Collection tab
    collection_tab.grid_columnconfigure(0, weight=1)  # allows column 0 to expand across the available width
    collection_tab.grid_rowconfigure(3, weight=1)

    # Collection heading
    collection_heading = ctk.CTkLabel(
        collection_tab,
        text="COLLECTION",
        font=heading_font
    )
    collection_heading.grid(
        row=0,
        column=0,
        padx=20,
        pady=(20, 10),
        sticky="w")  # placing the heading. First row, first column. sticky w = west, so aligned to the left

    summary_frame = ctk.CTkFrame(collection_tab)  # container to put other widgets inside

    summary_frame.grid(
        row=1,
        column=0,
        padx=20,
        pady=10,
        sticky="ew"
    )

    summary_frame.grid_columnconfigure(0, weight=1)
    summary_frame.grid_columnconfigure(1, weight=1)
    summary_frame.grid_columnconfigure(2, weight=1)

    # Total Cards card
    total_cards_frame = ctk.CTkFrame(summary_frame)
    total_cards_frame.grid_columnconfigure(0, weight=1)

    total_cards_frame.grid(  # placing it
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="ew"
    )

    # Adding text
    total_cards_label = ctk.CTkLabel(
        total_cards_frame,
        text="TOTAL CARDS OWNED",
        font=normal_font
    )

    total_cards_label.grid(
        row=0,
        column=0,
        padx=20,
        pady=(15, 5),
    )

    total_cards_value = ctk.CTkLabel(
        total_cards_frame,
        text="0",
        font=summary_value_font
    )

    total_cards_value.grid(
        row=1,
        column=0,
        padx=20,
        pady=(0, 15),
    )

    # Entries card
    entries_frame = ctk.CTkFrame(summary_frame)
    entries_frame.grid_columnconfigure(0, weight=1)

    entries_frame.grid(
        row=0,
        column=1,
        padx=10,
        pady=10,
        sticky="ew"
    )

    entries_label = ctk.CTkLabel(
        entries_frame,
        text="COLLECTION ENTRIES",
        font=normal_font
    )

    entries_label.grid(
        row=0,
        column=0,
        padx=20,
        pady=(15, 5),
    )

    entries_value = ctk.CTkLabel(
        entries_frame,
        text="0",
        font=summary_value_font
    )

    entries_value.grid(
        row=1,
        column=0,
        padx=20,
        pady=(0, 15),
    )

    # Value card
    value_frame = ctk.CTkFrame(summary_frame)
    value_frame.grid_columnconfigure(0, weight=1)

    value_frame.grid(
        row=0,
        column=2,
        padx=10,
        pady=10,
        sticky="ew"
    )

    value_label = ctk.CTkLabel(
        value_frame,
        text="ESTIMATED VALUE",
        font=normal_font
    )

    value_label.grid(
        row=0,
        column=0,
        padx=20,
        pady=(15, 5),
    )

    value_card_value = ctk.CTkLabel(
        value_frame,
        text="$0.00",
        font=summary_value_font
    )

    value_card_value.grid(
        row=1,
        column=0,
        padx=20,
        pady=(0, 15),
    )

    # Search and filters
    filter_frame = ctk.CTkFrame(collection_tab)
    filter_frame.grid_columnconfigure(0, weight=1)

    filter_frame.grid(
        row=2,
        column=0,
        padx=20,
        pady=10,
        sticky="ew"
    )

    # Collection search box
    collection_search = ctk.CTkEntry(  # CTkEntry for a text input box
        filter_frame,
        placeholder_text="Search your collection...",
        font=normal_font
    )

    collection_search.grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="ew"
    )

    # Location filter
    location_filter = ctk.CTkOptionMenu(
        filter_frame,
        values=["All Locations", "Binder", "Deck", "Box"],
        font=normal_font
    )

    location_filter.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    # Set filter
    set_filter = ctk.CTkOptionMenu(
        filter_frame,
        values=["All Sets", "Foundations", "Modern Horizons 3"],
        font=normal_font
    )

    set_filter.grid(
        row=0,
        column=2,
        padx=10,
        pady=10
    )

    # Colour filter
    colour_filter = ctk.CTkOptionMenu(
        filter_frame,
        values=["All Colours", "White", "Blue", "Black", "Red", "Green", "Colourless"],
        font=normal_font
    )

    colour_filter.grid(
        row=0,
        column=3,
        padx=10,
        pady=10
    )

    # More filters button
    more_filters_button = ctk.CTkButton(
        filter_frame,
        text="More Filters",
        font=normal_font
    )

    more_filters_button.grid(
        row=0,
        column=4,
        padx=10,
        pady=10
    )

    # Clear filters button
    clear_filters_button = ctk.CTkButton(
        filter_frame,
        text="Clear Filters",
        font=normal_font
    )

    clear_filters_button.grid(
        row=0,
        column=5,
        padx=10,
        pady=10
    )

    # Main collection area
    collection_content_frame = ctk.CTkFrame(collection_tab)

    # Allows the contents of this frame to expand
    collection_content_frame.grid_rowconfigure(0, weight=1)
    collection_content_frame.grid_columnconfigure(0, weight=3)
    collection_content_frame.grid_columnconfigure(1, weight=1)

    collection_content_frame.grid(
        row=3,
        column=0,
        padx=20,
        pady=(10, 20),
        sticky="nsew"
    )

    # Collection table area
    collection_table_frame = ctk.CTkFrame(collection_content_frame)

    collection_table_frame.grid_columnconfigure(0, weight=1)
    collection_table_frame.grid_rowconfigure(1, weight=1)

    collection_table_frame.grid(
        row=0,
        column=0,
        padx=(10, 5),
        pady=10,
        sticky="nsew"
    )

    # Collection table heading
    collection_table_heading = ctk.CTkLabel(
        collection_table_frame,
        text="YOUR CARDS",
        font=normal_font
    )

    collection_table_heading.grid(
        row=0,
        column=0,
        padx=15,
        pady=(10, 5),
        sticky="w"
    )

    # Collection table columns
    collection_columns = (
        "card_name",
        "set",
        "card_number",
        "colour",
        "type",
        "quantity",
        "foil",
        "condition",
        "location",
        "market_price"
    )

    # Styling the collection table
    tree_style = ttk.Style()
    tree_style.theme_use("clam")

    tree_style.configure(
        "Treeview",
        background="#2b2b2b",
        foreground="white",
        fieldbackground="#2b2b2b",
        borderwidth=0,
        font=("Segoe UI", 11),
        rowheight=30
    )

    tree_style.configure(
        "Treeview.Heading",
        background="#3a3a3a",
        foreground="white",
        font=("Segoe UI", 11, "bold")
    )

    # Collection table
    collection_tree = ttk.Treeview(
        collection_table_frame,
        columns=collection_columns,
        show="headings"
    )

    # Collection table headings
    collection_tree.heading("card_name", text="Card Name")
    collection_tree.heading("set", text="Set")
    collection_tree.heading("card_number", text="Card #")
    collection_tree.heading("colour", text="Colour")
    collection_tree.heading("type", text="Type")
    collection_tree.heading("quantity", text="Qty")
    collection_tree.heading("foil", text="Foil")
    collection_tree.heading("condition", text="Condition")
    collection_tree.heading("location", text="Location")
    collection_tree.heading("market_price", text="Market Price")

    # Collection table column sizes and alignment
    collection_tree.column("card_name", width=160, anchor="w")
    collection_tree.column("set", width=100, anchor="w")
    collection_tree.column("card_number", width=70, anchor="center")
    collection_tree.column("colour", width=70, anchor="center")
    collection_tree.column("type", width=110, anchor="w")
    collection_tree.column("quantity", width=50, anchor="center")
    collection_tree.column("foil", width=50, anchor="center")
    collection_tree.column("condition", width=100, anchor="center")
    collection_tree.column("location", width=100, anchor="w")
    collection_tree.column("market_price", width=90, anchor="e")

    # Place collection table
    collection_tree.grid(
        row=1,
        column=0,
        padx=(15, 0),
        pady=(5, 0),
        sticky="nsew"
    )

    # Vertical scrollbar for collection table
    collection_vertical_scrollbar = ttk.Scrollbar(
        collection_table_frame,
        orient="vertical",
        command=collection_tree.yview
    )

    collection_vertical_scrollbar.grid(
        row=1,
        column=1,
        pady=(5, 0),
        sticky="ns"
    )

    # Horizontal scrollbar for collection table
    collection_horizontal_scrollbar = ttk.Scrollbar(
        collection_table_frame,
        orient="horizontal",
        command=collection_tree.xview
    )

    collection_horizontal_scrollbar.grid(
        row=2,
        column=0,
        padx=(15, 0),
        pady=(0, 15),
        sticky="ew"
    )

    # Connecting Treeview back to the scrollbar
    collection_tree.configure(
        yscrollcommand=collection_vertical_scrollbar.set,
        xscrollcommand=collection_horizontal_scrollbar.set
    )

    # Selected card details area
    card_details_frame = ctk.CTkScrollableFrame(collection_content_frame)

    card_details_frame.grid_columnconfigure(0, weight=1)

    card_details_frame.grid(
        row=0,
        column=1,
        padx=(5, 10),
        pady=10,
        sticky="nsew"
    )

    # Selected card heading
    card_details_heading = ctk.CTkLabel(
        card_details_frame,
        text="SELECTED CARD",
        font=normal_font
    )

    card_details_heading.grid(
        row=0,
        column=0,
        padx=15,
        pady=(10, 5),
        sticky="w"
    )

    # Card image placeholder
    card_image_placeholder = ctk.CTkLabel(
        card_details_frame,
        text="Card Image",
        width=160,
        height=224,
        fg_color="#242424",
        corner_radius=10,
        font=normal_font
    )

    card_image_placeholder.grid(
        row=1,
        column=0,
        padx=20,
        pady=10
    )

    # Selected card information
    card_info_frame = ctk.CTkFrame(
        card_details_frame,
        fg_color="transparent"
    )

    card_info_frame.grid_columnconfigure(0, weight=1)

    card_info_frame.grid(
        row=2,
        column=0,
        padx=20,
        pady=10,
        sticky="ew"
    )

    card_info_frame.grid_columnconfigure(0, weight=1)

    card_name_label = ctk.CTkLabel(
        card_info_frame,
        text="No card selected",
        font=card_name_font
    )

    card_name_label.grid(
        row=0,
        column=0,
        sticky="w"
    )

    # Selected card set and number
    card_set_label = ctk.CTkLabel(
        card_info_frame,
        text="Set • Card #",
        font=normal_font
    )

    card_set_label.grid(
        row=1,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Selected card type
    card_type_label = ctk.CTkLabel(
        card_info_frame,
        text="Type • Subtype",
        font=normal_font
    )

    card_type_label.grid(
        row=2,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Selected card colour information
    card_colour_label = ctk.CTkLabel(
        card_info_frame,
        text="Colour: —   •   Identity: —",
        font=normal_font
    )

    card_colour_label.grid(
        row=3,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Selected card mana value
    card_mana_value_label = ctk.CTkLabel(
        card_info_frame,
        text="Mana Value: —",
        font=normal_font
    )

    card_mana_value_label.grid(
        row=4,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Selected card rarity
    card_rarity_label = ctk.CTkLabel(
        card_info_frame,
        text="Rarity: —",
        font=normal_font
    )

    card_rarity_label.grid(
        row=5,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Ownership section heading
    ownership_heading = ctk.CTkLabel(
        card_info_frame,
        text="YOUR COPY",
        font=normal_font
    )

    ownership_heading.grid(
        row=6,
        column=0,
        pady=(15, 5),
        sticky="w"
    )

    # Selected card quantity and foil
    card_ownership_label = ctk.CTkLabel(
        card_info_frame,
        text="Quantity: —   •   Foil: —",
        font=normal_font
    )

    card_ownership_label.grid(
        row=7,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Selected card condition
    card_condition_label = ctk.CTkLabel(
        card_info_frame,
        text="Condition: —",
        font=normal_font
    )

    card_condition_label.grid(
        row=8,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Selected card location
    card_location_label = ctk.CTkLabel(
        card_info_frame,
        text="Location: —",
        font=normal_font
    )

    card_location_label.grid(
        row=9,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Selected card market value
    card_market_value_label = ctk.CTkLabel(
        card_info_frame,
        text="Market Price: $—",
        font=normal_font
    )

    card_market_value_label.grid(
        row=10,
        column=0,
        pady=(15, 0),
        sticky="w"
    )

    # Total value of owned copies
    card_total_value_label = ctk.CTkLabel(
        card_info_frame,
        text="Total Value: $—",
        font=normal_font
    )

    card_total_value_label.grid(
        row=11,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Action Buttons
    # Selected card actions
    card_actions_frame = ctk.CTkFrame(
        card_details_frame,
        fg_color="transparent"
    )

    card_actions_frame.grid(
        row=3,
        column=0,
        padx=20,
        pady=(5, 20),
        sticky="ew"
    )

    card_actions_frame.grid_columnconfigure((0, 1), weight=1)

    # Increase quantity button
    increase_quantity_button = ctk.CTkButton(
        card_actions_frame,
        text="+1"
    )

    increase_quantity_button.grid(
        row=0,
        column=0,
        padx=(0, 5),
        pady=5,
        sticky="ew"
    )

    # Decrease quantity button
    decrease_quantity_button = ctk.CTkButton(
        card_actions_frame,
        text="-1"
    )

    decrease_quantity_button.grid(
        row=0,
        column=1,
        padx=(5, 0),
        pady=5,
        sticky="ew"
    )

    # Edit selected collection entry
    edit_card_button = ctk.CTkButton(
        card_actions_frame,
        text="Edit"
    )

    edit_card_button.grid(
        row=1,
        column=0,
        padx=(0, 5),
        pady=5,
        sticky="ew"
    )

    # Move selected collection entry
    move_card_button = ctk.CTkButton(
        card_actions_frame,
        text="Move"
    )

    move_card_button.grid(
        row=1,
        column=1,
        padx=(5, 0),
        pady=5,
        sticky="ew"
    )

    # Remove all copies of selected collection entry
    remove_all_button = ctk.CTkButton(
        card_actions_frame,
        text="Remove All"
    )

    remove_all_button.grid(
        row=2,
        column=0,
        columnspan=2,
        padx=0,
        pady=(5, 0),
        sticky="ew"
    )