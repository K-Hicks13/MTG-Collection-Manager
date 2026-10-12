import customtkinter as ctk
from tkinter import ttk


def build_add_cards_tab(add_cards_tab, heading_font, normal_font, card_name_font):
    # Add Cards tab layout
    add_cards_tab.grid_columnconfigure(0, weight=1)
    add_cards_tab.grid_rowconfigure(2, weight=1)

    # Page heading
    add_cards_heading = ctk.CTkLabel(
        add_cards_tab,
        text="Add Cards",
        font=heading_font
    )

    add_cards_heading.grid(
        row=0,
        column=0,
        padx=20,
        pady=(20, 10),
        sticky="w"
    )

    # Add Cards mode selector
    add_mode_selector = ctk.CTkSegmentedButton(
        add_cards_tab,
        values=["Single Add", "Quick / Bulk Add"],
        font=normal_font
    )

    add_mode_selector.grid(
        row=1,
        column=0,
        padx=20,
        pady=(5, 15),
        sticky="w"
    )

    # Set the default mode
    add_mode_selector.set("Single Add")

    # Single Add content frame
    single_add_frame = ctk.CTkFrame(
        add_cards_tab
    )

    single_add_frame.grid(
        row=2,
        column=0,
        padx=20,
        pady=(0, 20),
        sticky="nsew"
    )

    single_add_frame.grid_columnconfigure(0, weight=1)
    single_add_frame.grid_rowconfigure(1, weight=1)

    # Single add search box
    single_add_search = ctk.CTkEntry(
        single_add_frame,
        placeholder_text="Search for a card...",
        font=normal_font
    )

    single_add_search.grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="ew"
    )

    # Search button
    search_button = ctk.CTkButton(
        single_add_frame,
        text="Search",
        font=normal_font
    )

    search_button.grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )

    # Search area
    add_content_frame = ctk.CTkFrame(single_add_frame)

    # Allows the contents of this frame to expand
    add_content_frame.grid_rowconfigure(0, weight=1)
    add_content_frame.grid_columnconfigure(0, weight=3)
    add_content_frame.grid_columnconfigure(1, weight=1)

    add_content_frame.grid(
        row=1,
        column=0,
        columnspan=2,
        padx=20,
        pady=(10, 20),
        sticky="nsew"
    )

    # Search content frame
    search_results_frame = ctk.CTkFrame(
        add_content_frame
    )

    search_results_frame.grid(
        row=0,
        column=0,
        padx=20,
        pady=(0, 20),
        sticky="nsew"
    )

    search_results_frame.grid_columnconfigure(0, weight=1)
    search_results_frame.grid_rowconfigure(0, weight=1)

    # Search Results table
    search_columns = ("card_name", "set", "card_number", "year")

    search_tree = ttk.Treeview(
        search_results_frame,
        columns=search_columns,
        show="headings"
    )

    # Search Results table headings
    search_tree.heading("card_name", text="Card Name")
    search_tree.heading("set", text="Set")
    search_tree.heading("card_number", text="Card #")
    search_tree.heading("year", text="Year")

    # Search Results table column sizes and alignment
    search_tree.column("card_name", width=160, anchor="w")
    search_tree.column("set", width=100, anchor="w")
    search_tree.column("card_number", width=70, anchor="center")
    search_tree.column("year", width=70, anchor="center")

    # Place search results table
    search_tree.grid(
        row=0,
        column=0,
        padx=(15, 0),
        pady=(5, 0),
        sticky="nsew"
    )

    # Vertical scrollbar for search results table
    search_vertical_scrollbar = ttk.Scrollbar(
        search_results_frame,
        orient="vertical",
        command=search_tree.yview
    )

    search_vertical_scrollbar.grid(
        row=0,
        column=1,
        pady=(5, 0),
        sticky="ns"
    )

    # Horizontal scrollbar for search results table
    search_horizontal_scrollbar = ttk.Scrollbar(
        search_results_frame,
        orient="horizontal",
        command=search_tree.xview
    )

    search_horizontal_scrollbar.grid(
        row=1,
        column=0,
        padx=(15, 0),
        pady=(0, 15),
        sticky="ew"
    )

    # Connecting Treeview back to the scrollbar
    search_tree.configure(
        yscrollcommand=search_vertical_scrollbar.set,
        xscrollcommand=search_horizontal_scrollbar.set
    )

    # Selected card details area
    selected_printing_frame = ctk.CTkScrollableFrame(add_content_frame)

    selected_printing_frame.grid_columnconfigure(0, weight=1)

    selected_printing_frame.grid(
        row=0,
        column=1,
        padx=(5, 10),
        pady=10,
        sticky="nsew"
    )

    # Selected card heading
    selected_printing_heading = ctk.CTkLabel(
        selected_printing_frame,
        text="SELECTED PRINTING",
        font=normal_font
    )

    selected_printing_heading.grid(
        row=0,
        column=0,
        padx=15,
        pady=(10, 5),
        sticky="w"
    )

    # Card image placeholder
    selected_printing_image_placeholder = ctk.CTkLabel(
        selected_printing_frame,
        text="Card Image",
        width=160,
        height=224,
        fg_color="#242424",
        corner_radius=10,
        font=normal_font
    )

    selected_printing_image_placeholder.grid(
        row=1,
        column=0,
        padx=20,
        pady=10
    )

    # Selected printing information
    selected_printing_info_frame = ctk.CTkFrame(
        selected_printing_frame,
        fg_color="transparent"
    )

    selected_printing_info_frame.grid_columnconfigure(0, weight=1)

    selected_printing_info_frame.grid(
        row=2,
        column=0,
        padx=20,
        pady=10,
        sticky="ew"
    )

    selected_printing_name_label = ctk.CTkLabel(
        selected_printing_info_frame,
        text="No card selected",
        font=card_name_font
    )

    selected_printing_name_label.grid(
        row=0,
        column=0,
        sticky="w"
    )

    # Selected printing set and number
    selected_printing_set_label = ctk.CTkLabel(
        selected_printing_info_frame,
        text="Set • Card #",
        font=normal_font
    )

    selected_printing_set_label.grid(
        row=1,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Selected printing rarity and type
    selected_printing_type_label = ctk.CTkLabel(
        selected_printing_info_frame,
        text="Rarity • Type",
        font=normal_font
    )

    selected_printing_type_label.grid(
        row=2,
        column=0,
        pady=(5, 0),
        sticky="w"
    )

    # Selected printing market value
    selected_printing_price_label = ctk.CTkLabel(
        selected_printing_info_frame,
        text="Market Price: $—",
        font=normal_font
    )

    selected_printing_price_label.grid(
        row=3,
        column=0,
        pady=(15, 0),
        sticky="w"
    )

    # Ownership section heading
    add_ownership_heading = ctk.CTkLabel(
        selected_printing_frame,
        text="ADD TO COLLECTION",
        font=normal_font
    )

    add_ownership_heading.grid(
        row=3,
        column=0,
        pady=(20, 5),
        padx=20,
        sticky="w"
    )

    # Selected printing quantity and foil
    add_quantity_entry = ctk.CTkEntry(
        selected_printing_frame,
        placeholder_text="Quantity",
        width=120,
        font=normal_font
    )

    add_quantity_entry.grid(
        row=4,
        column=0,
        pady=(5, 10),
        padx=20,
        sticky="w"
    )

    # Foil checkbox
    add_foil_checkbox = ctk.CTkCheckBox(
        selected_printing_frame,
        text="Foil",
        font=normal_font
    )

    add_foil_checkbox.grid(
        row=5,
        column=0,
        pady=(5, 10),
        padx=20,
        sticky="w"
    )

    # Selected printing condition
    add_condition_menu = ctk.CTkOptionMenu(
        selected_printing_frame,
        values=["NM", "LP", "MP", "HP", "DMG"],
        font=normal_font,
        width=150
    )

    add_condition_menu.grid(
        row=6,
        column=0,
        pady=(5, 10),
        padx=20,
        sticky="w"
    )

    # Selected printing location
    add_location_menu = ctk.CTkOptionMenu(
        selected_printing_frame,
        values=["Select Location"],
        font=normal_font,
        width=200
    )

    add_location_menu.grid(
        row=7,
        column=0,
        pady=(5, 10),
        padx=20,
        sticky="w"
    )

    # Add to Collection Button
    add_to_collection_button = ctk.CTkButton(
        selected_printing_frame,
        text="Add To Collection",
        font=normal_font,
        width=200
    )

    add_to_collection_button.grid(
        row=8,
        column=0,
        pady=(20, 10),
        padx=20,
        sticky="w"
    )

    # Bulk add content frame
    bulk_add_frame = ctk.CTkFrame(
        add_cards_tab
    )

    bulk_add_frame.grid(
        row=2,
        column=0,
        padx=20,
        pady=(0, 20),
        sticky="nsew"
    )

    bulk_add_frame.grid_columnconfigure(0, weight=1)
    bulk_add_frame.grid_rowconfigure(1, weight=1)

    # Bulk add heading
    bulk_add_heading = ctk.CTkLabel(
        bulk_add_frame,
        text="QUICK / BULK ADD",
        font=normal_font
    )

    bulk_add_heading.grid(
        row=0,
        column=0,
        padx=20,
        pady=(15, 10),
        sticky="w"
    )

    # Bulk entry area
    bulk_entry_frame = ctk.CTkFrame(
        bulk_add_frame,
    )

    bulk_entry_frame.grid(
        row=1,
        column=0,
        pady=(5, 20),
        padx=20,
        sticky="nsew"
    )

    bulk_entry_frame.grid_columnconfigure(0, weight=1)
    bulk_entry_frame.grid_rowconfigure(1, weight=1)

    # Instructions label
    bulk_instructions_label = ctk.CTkLabel(
        bulk_entry_frame,
        text="Enter one card per line to add multiple cards at once.",
        font=normal_font
    )

    bulk_instructions_label.grid(
        row=0,
        column=0,
        pady=(15, 10),
        padx=15,
        sticky="w"
    )

    # Bulk card text input
    bulk_cards_textbox = ctk.CTkTextbox(
        bulk_entry_frame,
        font=normal_font
    )

    bulk_cards_textbox.grid(
        row=1,
        column=0,
        pady=(5, 15),
        padx=15,
        sticky="nsew"
    )

    # Processing button
    bulk_process_button = ctk.CTkButton(
        bulk_entry_frame,
        text="Review Cards",
        font=normal_font,
        width=180
    )

    bulk_process_button.grid(
        row=2,
        column=0,
        pady=(5, 15),
        padx=15,
        sticky="e"
    )

    # Switching between add modes
    def switch_add_mode(selected_mode):
        if selected_mode == "Single Add":
            bulk_add_frame.grid_remove()
            single_add_frame.grid()
        elif selected_mode == "Quick / Bulk Add":
            single_add_frame.grid_remove()
            bulk_add_frame.grid()

    switch_add_mode("Single Add")

    add_mode_selector.configure(command=switch_add_mode)