import customtkinter as ctk

from gui.collection_tab import build_collection_tab
from gui.add_cards_tab import build_add_cards_tab


# Setting dark mode
ctk.set_appearance_mode("dark")

app = ctk.CTk()

# Adding title
app.title("MTG Collection Manager")

# Adding window dimensions
app.geometry("1400x850")

# Creating Tabs
tab_view = ctk.CTkTabview(app)  # creating widget
tab_view.pack(fill="both", expand=True, padx=20, pady=20)   # fills horizontally and vertically, gives it available extra space when the window grows, 20 pixels of space on the left/right, 20 pixels of space above/below.

# Adding tab headings
tab_view.add("Collection")
tab_view.add("Add Cards")
tab_view.add("Trade")
tab_view.add("History")
tab_view.add("Locations")
tab_view.add("Stats")

# Reusable fonts - font type, size and bold/not
heading_font = ctk.CTkFont(
    family="Georgia",
    size=30,
    weight="bold"
)

normal_font = ctk.CTkFont(
    family="Segoe UI",
    size=14
)

summary_value_font = ctk.CTkFont(
    family="Segoe UI",
    size=26,
    weight="bold"
)

card_name_font = ctk.CTkFont(
    family="Georgia",
    size=20,
    weight="bold"
)

# Build Collection tab
build_collection_tab(
    tab_view.tab("Collection"),
    heading_font,
    normal_font,
    summary_value_font,
    card_name_font
)

# Build Add Cards tab
build_add_cards_tab(
    tab_view.tab("Add Cards"),
    heading_font,
    normal_font,
    card_name_font
)

# Running
app.mainloop()