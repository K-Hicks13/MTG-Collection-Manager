# MTG Collection Manager

A desktop application for managing a Magic: The Gathering card collection.

The application is being developed using **Python**, **CustomTkinter**, **MySQL**, and the **Scryfall API**.

The project is currently under development.

## Project Structure

### Main Application

| File | Description |
|---|---|
| `app.py` | Main application entry point. Creates the CustomTkinter interface, including the Collection, Add Cards, Trade, History, Locations, and Stats tabs. |
| `database.py` | Establishes connections to the MySQL database using credentials stored in environment variables. |
| `Database.sql` | Defines the MySQL database schema, including tables, relationships, constraints, and reference data. |

### Card Management

| File | Description |
|---|---|
| `card_repository.py` | Performs database operations for card records, including retrieving cards and checking whether a particular printing already exists. |
| `card_database.py` | Coordinates saving Scryfall card data to the database, including sets, cards, and their colour/type relationships. |
| `card_service.py` | Connects Scryfall card retrieval with database operations and the process of adding cards to the collection. |
| `scryfall_api.py` | Communicates with the Scryfall API to search for cards, retrieve specific printings, and convert API responses into data the application can use. |

### Collection Management

| File | Description |
|---|---|
| `collection_repository.py` | Handles collection database operations, including retrieving owned cards, changing quantities, updating entries, moving cards between locations, and soft deletion. |
| `location_repository.py` | Manages collection storage locations, including retrieving, creating, and updating locations. |

### Reference Data

| File | Description |
|---|---|
| `set_repository.py` | Handles retrieving and creating MTG set records. |
| `colour_repository.py` | Manages card colours and the relationships between cards and colours. |
| `type_repository.py` | Manages card types and their relationships with cards. |
| `subtype_repository.py` | Manages card subtypes and their relationships with cards. |

### Collection History and Transactions

| File | Description |
|---|---|
| `event_repository.py` | Creates and retrieves collection events, representing actions such as adding, removing, editing, moving, or trading cards. |
| `transaction_repository.py` | Stores and retrieves transactions and individual transaction items associated with collection events. |
| `transaction_service.py` | Coordinates collection changes with their history records, including additions, removals, quantity changes, moves, edits, and trades. Uses database transactions so related operations succeed or fail together. |

### Testing

| File | Description |
|---|---|
| `database_test.py` | Contains development tests for database connections and database-related functionality. |

### Configuration

| File / Folder | Description |
|---|---|
| `.env` | Stores local database connection credentials. This file must not be committed to GitHub. |
| `.gitignore` | Specifies files and folders Git should ignore, including `.env` and `.venv/`. |
| `.venv/` | Python virtual environment containing project-specific installed packages. |

## Application Architecture

The project separates responsibilities into different layers:

- **GUI (`app.py`)** — Displays information and receives user input.
- **Services (`*_service.py`)** — Coordinates application workflows and business rules.
- **Repositories (`*_repository.py`)** — Executes database queries and manages database records.
- **Database (`database.py`, `Database.sql`)** — Provides the MySQL connection and data structure.
- **External API (`scryfall_api.py`)** — Retrieves card information from Scryfall.

This separation makes the application easier to understand, test, maintain, and extend.

## Current Development Status

- MySQL database schema created.
- Database connection established.
- Card and collection repository functionality implemented.
- Scryfall API integration implemented.
- Collection history and transaction workflows implemented.
- Trade workflow implemented and tested.
- CustomTkinter GUI layout in progress.

The application is not yet fully connected to the graphical interface.