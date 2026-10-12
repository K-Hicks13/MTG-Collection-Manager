CREATE DATABASE IF NOT EXISTS MTG_Collection_Updated;
USE MTG_Collection_Updated;

CREATE TABLE IF NOT EXISTS MTG_Set
(
    Set_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Set_Name VARCHAR(255) NOT NULL,
    Set_Code VARCHAR(10) NOT NULL,
    CONSTRAINT uq_sets_code UNIQUE (Set_Code),
    Set_Year YEAR NOT NULL
);

CREATE TABLE IF NOT EXISTS Location
(
    Location_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Location_Name VARCHAR(100) NOT NULL,
    CONSTRAINT uq_location_name UNIQUE (Location_Name),
    Location_Description VARCHAR(255),
    Location_Type ENUM('Binder', 'Box', 'Deck', 'Sleeves', 'Cube', 'Storage') NOT NULL
);

CREATE TABLE IF NOT EXISTS Colour
(
    Colour_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Colour_Name VARCHAR(25) NOT NULL,
    CONSTRAINT uq_colour_name UNIQUE (Colour_Name),
    Colour_Code CHAR(1) NOT NULL,
    CONSTRAINT uq_colour_code UNIQUE (Colour_Code),
    Sort_Order TINYINT NOT NULL,
    CONSTRAINT uq_colour_sort_order UNIQUE (Sort_Order)
);

INSERT IGNORE INTO Colour (Colour_Name, Colour_Code, Sort_Order)
VALUES ('White', 'W', 1),
       ('Blue', 'U', 2),
       ('Black', 'B', 3),
       ('Red', 'R', 4),
       ('Green', 'G', 5);

CREATE TABLE IF NOT EXISTS Type
(
    Type_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Type_Name VARCHAR(50) NOT NULL,
    CONSTRAINT uq_card_type UNIQUE (Type_Name)
);

CREATE TABLE IF NOT EXISTS Subtype
(
    Subtype_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Subtype_Name VARCHAR(75) NOT NULL,
    CONSTRAINT uq_card_subtype UNIQUE (Subtype_Name)
);

CREATE TABLE IF NOT EXISTS Card
(
    Card_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Card_Name VARCHAR(255) NOT NULL,
    Card_Number VARCHAR(20) NOT NULL,
    Colour_Identity VARCHAR(10) NOT NULL,
    Mana_Value DECIMAL(10,1) NOT NULL,
    CONSTRAINT chk_cards_mana_value CHECK (Mana_Value >= 0),
    Rarity ENUM('common', 'uncommon', 'rare', 'mythic') NOT NULL,
    Set_ID INT NOT NULL,
    CONSTRAINT fk_cards_set FOREIGN KEY (Set_ID) REFERENCES MTG_Set(Set_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    Card_Language VARCHAR(25) NOT NULL,
    Market_Price DECIMAL(10,2),
    CONSTRAINT chk_market_price CHECK ( Market_Price >= 0 ),
    Foil_Market_Price DECIMAL(10,2),
    CONSTRAINT chk_foil_market_price CHECK ( Foil_Market_Price >= 0 ),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
    CONSTRAINT uq_card_printing UNIQUE (Card_Name, Card_Number, Set_ID, Card_Language)
);

CREATE TABLE IF NOT EXISTS Collection
(
    Collection_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Card_ID INT NOT NULL,
    CONSTRAINT fk_collection_card FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    Location_ID INT NOT NULL,
    CONSTRAINT fk_collection_location FOREIGN KEY (Location_ID) REFERENCES Location(Location_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    Quantity INT NOT NULL,
    CONSTRAINT chk_collection_quantity CHECK ( Quantity >= 1 ),
    Foil BOOLEAN NOT NULL DEFAULT FALSE,
    Card_Condition ENUM('Near Mint', 'Lightly Played', 'Moderately Played', 'Heavily Played', 'Damaged') DEFAULT 'Near Mint' NOT NULL,
    Is_Deleted BOOLEAN NOT NULL DEFAULT FALSE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
    CONSTRAINT uq_collection_variant UNIQUE (Card_ID, Location_ID, Foil, Card_Condition)
);

CREATE TABLE IF NOT EXISTS Card_Colour_Map
(
    Card_ID INT NOT NULL,
    CONSTRAINT fk_colour_map_card FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON DELETE CASCADE,
    Colour_ID INT NOT NULL,
    CONSTRAINT fk_colour_map_colour FOREIGN KEY (Colour_ID) REFERENCES Colour(Colour_ID) ON DELETE CASCADE,
    PRIMARY KEY (Card_ID, Colour_ID)
);

CREATE TABLE IF NOT EXISTS Card_Type_Map
(
    Card_ID INT NOT NULL,
    CONSTRAINT fk_type_map_card FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON DELETE CASCADE,
    Type_ID INT NOT NULL,
    CONSTRAINT fk_type_map_type FOREIGN KEY (Type_ID) REFERENCES Type(Type_ID) ON DELETE CASCADE,
    PRIMARY KEY (Card_ID, Type_ID)
);

CREATE TABLE IF NOT EXISTS Card_Subtype_Map
(
    Card_ID INT NOT NULL,
    CONSTRAINT fk_subtype_map_card FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON DELETE CASCADE,
    Subtype_ID INT NOT NULL,
    CONSTRAINT fk_subtype_map_subtype FOREIGN KEY (Subtype_ID) REFERENCES Subtype(Subtype_ID) ON DELETE CASCADE,
    PRIMARY KEY (Card_ID, Subtype_ID)
);

CREATE TABLE IF NOT EXISTS Collection_Event
(
    Event_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Event_Date DATE NOT NULL,
    Event_Type ENUM('Add', 'Edit', 'Remove', 'Move', 'Trade') NOT NULL,
    Person_Place VARCHAR(100),
    Notes VARCHAR(255),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP() NOT NULL
);

CREATE TABLE IF NOT EXISTS Collection_Transaction
(
    Transaction_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Event_ID INT NOT NULL,
    CONSTRAINT fk_collection_transaction_event FOREIGN KEY (Event_ID) REFERENCES Collection_Event(Event_ID) ON DELETE CASCADE,
    Transaction_Type ENUM('Purchase', 'Sale', 'Trade', 'Gift', 'Initial Inventory', 'Internal Move', 'Other') NOT NULL
);

CREATE TABLE IF NOT EXISTS Collection_Transaction_Item
(
    Transaction_Item_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Transaction_ID INT NOT NULL,
    CONSTRAINT fk_transaction_item_transaction FOREIGN KEY (Transaction_ID) REFERENCES Collection_Transaction(Transaction_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    Card_ID INT NOT NULL,
    CONSTRAINT fk_transaction_item_card FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON DELETE RESTRICT ON UPDATE CASCADE,
    Direction ENUM('IN', 'OUT', 'MOVE') NOT NULL,
    Quantity INT NOT NULL,
    CONSTRAINT chk_transaction_item_quantity CHECK ( Quantity >= 1 ),
    From_Location_ID INT,
    CONSTRAINT fk_transaction_item_from_location FOREIGN KEY (From_Location_ID) REFERENCES Location(Location_ID) ON DELETE RESTRICT,
    To_Location_ID INT,
    CONSTRAINT fk_transaction_item_to_location FOREIGN KEY (To_Location_ID) REFERENCES Location(Location_ID) ON DELETE RESTRICT,
    CONSTRAINT chk_transaction_item_locations CHECK (
        (Direction = 'IN' AND From_Location_ID IS NULL AND To_Location_ID IS NOT NULL)
        OR
        (Direction = 'OUT' AND From_Location_ID IS NOT NULL AND To_Location_ID IS NULL)
        OR
        (Direction = 'MOVE' AND From_Location_ID IS NOT NULL AND To_Location_ID IS NOT NULL AND From_Location_ID <> To_Location_ID)),
    Foil BOOLEAN NOT NULL DEFAULT FALSE,
    Card_Condition ENUM('Near Mint', 'Lightly Played', 'Moderately Played', 'Heavily Played', 'Damaged') DEFAULT 'Near Mint' NOT NULL,
    Price_Per_Card DECIMAL(10,2),
    CONSTRAINT chk_transaction_item_price CHECK ( Price_Per_Card >= 0 ),
    Currency ENUM('NOK', 'GBP', 'USD', 'EUR', 'SEK', 'DKK', 'CAD', 'JPY', 'AUD', 'CHF'),
    CONSTRAINT chk_transaction_item_price_currency CHECK (
        (Price_Per_Card IS NULL AND Currency IS NULL)
        OR
        (Price_Per_Card IS NOT NULL AND Currency IS NOT NULL))
);