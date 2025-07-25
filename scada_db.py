import sqlite3
import datetime

DB_NAME = 'scada.db'


def connect_db():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    return conn


def create_tables():
    """Creates all necessary tables in the database if they don't already exist."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Locations (
            location_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    locations = ['Lobby', 'Office 1', 'Office 2', 'Office 3', 'Corridor 1', 'Corridor 2', 'Parking lot',
                 'Office_unspecified', 'Corridor_unspecified', 'System']
    cursor.executemany('INSERT OR IGNORE INTO Locations (name) VALUES (?)', [(loc,) for loc in locations])

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS People (
            person_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            middle_name TEXT,
            last_name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cards (
            card_id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_number TEXT(10) UNIQUE NOT NULL CHECK(length(card_number) = 10 AND card_number GLOB '[0-9]*'),
            person_id INTEGER,
            FOREIGN KEY (person_id) REFERENCES People (person_id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accesses (
            access_id INTEGER PRIMARY KEY AUTOINCREMENT,
            card_id INTEGER NOT NULL,
            location_id INTEGER NOT NULL,
            FOREIGN KEY (card_id) REFERENCES Cards (card_id) ON DELETE CASCADE,
            FOREIGN KEY (location_id) REFERENCES Locations (location_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    event_types = [
        'successful_rfid_access', 'unsuccessful_rfid_access', 'multiple_objects_passed_parking_lot_gate',
        'parking_lot_was_forced_open', 'parking_lot_was_forced_closed', 'fire_detected', 'emergency_happened',
        'alarm_was_activated', 'alarm_was_deactivated', 'alarm_was_triggered', 'security_was_called',
        'fire_dept_was_called', 'config_altered', 'auto_security_impossible', 'parking_gate_open_warning',
        'parking_spot_miscount', 'light_config_error', 'parking_gate_forced_error', 'parking_spot_config_error',
        'temp_config_error', 'work_day_config_error', 'cold_month_config_error'
    ]
    cursor.executemany('INSERT OR IGNORE INTO Events (name) VALUES (?)', [(evt,) for evt in event_types])

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Log (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            timestamp DATETIME NOT NULL,
            location_id INTEGER NOT NULL,
            card_id INTEGER,
            is_resolved BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY (event_id) REFERENCES Events (event_id),
            FOREIGN KEY (location_id) REFERENCES Locations (location_id),
            FOREIGN KEY (card_id) REFERENCES Cards (card_id) ON DELETE SET NULL
        )
    ''')

    conn.commit()
    conn.close()


def log_event(event_name: str, location_name: str, card_number: str = None, is_resolved: bool = False):
    """Logs a generic event, checking for existing unresolved events to avoid duplicates."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT event_id FROM Events WHERE name = ?', (event_name,))
    event_id_res = cursor.fetchone()
    cursor.execute('SELECT location_id FROM Locations WHERE name = ?', (location_name,))
    location_id_res = cursor.fetchone()
    int_card_id = None
    if card_number:
        cursor.execute('SELECT card_id FROM Cards WHERE card_number = ?', (card_number,))
        card_pk_res = cursor.fetchone()
        if card_pk_res:
            int_card_id = card_pk_res[0]
    if event_id_res and location_id_res:
        event_id = event_id_res[0]
        location_id = location_id_res[0]
        cursor.execute('''
            SELECT log_id FROM Log
            WHERE event_id = ? AND location_id = ? AND is_resolved = 0
        ''', (event_id, location_id))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO Log (event_id, timestamp, location_id, card_id, is_resolved)
                VALUES (?, ?, ?, ?, ?)
            ''', (event_id, datetime.datetime.now(), location_id, int_card_id, is_resolved))
    conn.commit()
    conn.close()


def resolve_event(event_name: str, location_name: str):
    """Marks the latest unresolved event of a specific type and location as resolved."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT event_id FROM Events WHERE name = ?', (event_name,))
    event_id_res = cursor.fetchone()
    cursor.execute('SELECT location_id FROM Locations WHERE name = ?', (location_name,))
    location_id_res = cursor.fetchone()
    if event_id_res and location_id_res:
        event_id = event_id_res[0]
        location_id = location_id_res[0]
        cursor.execute('''
            UPDATE Log
            SET is_resolved = 1
            WHERE log_id = (
                SELECT log_id FROM Log
                WHERE event_id = ? AND location_id = ? AND is_resolved = 0
                ORDER BY timestamp DESC LIMIT 1
            )
        ''', (event_id, location_id))
    conn.commit()
    conn.close()


def execute_query(query: str, params=()):
    """Executes a given SQL query and returns column headers and results."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description] if cursor.description else []
        results = cursor.fetchall()
        conn.commit()
        return columns, results, None
    except sqlite3.Error as e:
        conn.rollback()
        return [], [], str(e)
    finally:
        conn.close()


def get_logs():
    """Retrieves the last 25 log entries with detailed information."""
    query = """
    SELECT
        l.log_id AS id,
        e.name AS event,
        loc.name AS location,
        l.timestamp,
        COALESCE(c.card_number, 'N/A') AS card,
        COALESCE(p.first_name || ' ' || p.last_name, 'N/A') AS owner,
        l.is_resolved AS resolved
    FROM Log l
    JOIN Events e ON l.event_id = e.event_id
    JOIN Locations loc ON l.location_id = loc.location_id
    LEFT JOIN Cards c ON l.card_id = c.card_id
    LEFT JOIN People p ON c.person_id = p.person_id
    ORDER BY l.timestamp DESC
    LIMIT 25;
    """
    return execute_query(query)


def get_people():
    """Retrieves all people and their associated card numbers."""
    query = """
    SELECT p.person_id, p.first_name, p.middle_name, p.last_name, GROUP_CONCAT(c.card_number) as card_numbers
    FROM People p
    LEFT JOIN Cards c ON p.person_id = c.person_id
    GROUP BY p.person_id
    ORDER BY p.last_name, p.first_name;
    """
    return execute_query(query)


def get_cards():
    """Retrieves all cards and their owners' names."""
    query = """
    SELECT c.card_id, c.card_number, c.person_id, p.first_name || ' ' || p.last_name as owner_name
    FROM Cards c
    LEFT JOIN People p ON c.person_id = p.person_id
    ORDER BY c.card_number;
    """
    return execute_query(query)


def get_accesses():
    """Retrieves all access rights, showing card number, owner, and location."""
    query = """
    SELECT
        a.access_id,
        rc.card_number,
        COALESCE(p.first_name || ' ' || p.last_name, 'Unassigned') as owner_name,
        l.name as location_name
    FROM Accesses a
    JOIN Locations l ON a.location_id = l.location_id
    LEFT JOIN Cards rc ON a.card_id = rc.card_id
    LEFT JOIN People p ON rc.person_id = p.person_id
    ORDER BY a.access_id;
    """
    return execute_query(query)


def add_person(first_name, middle_name, last_name):
    """Adds a person to the People table."""
    query = "INSERT INTO People (first_name, middle_name, last_name) VALUES (?, ?, ?)"
    return execute_query(query, (first_name, middle_name, last_name))


def add_card(card_number, person_id):
    """Adds a new RFID card and assigns it to a person."""
    query = "INSERT INTO Cards (card_number, person_id) VALUES (?, ?)"
    return execute_query(query, (card_number, person_id))


def add_access(card_id, location_id):
    """Adds an access right for a card's primary key ID to a location ID."""
    query = "INSERT INTO Accesses (card_id, location_id) VALUES (?, ?)"
    return execute_query(query, (card_id, location_id))


def remove_person(person_id):
    """Removes a person and all their associated cards and accesses (cascading)."""
    return execute_query("DELETE FROM People WHERE person_id = ?", (person_id,))


def remove_card(card_id):
    """Removes a card and its associated accesses (cascading) by its primary key."""
    return execute_query("DELETE FROM Cards WHERE card_id = ?", (card_id,))


def remove_access(access_id):
    """Removes a specific access right by its ID."""
    return execute_query("DELETE FROM Accesses WHERE access_id = ?", (access_id,))


def get_or_create_card(card_number: str) -> int:
    """
    Returns the card_id for a 10-digit card_number.
    If it doesn't exist, it inserts the card with person_id=NULL.
    """
    conn = connect_db()
    cur = conn.cursor()
    card_id = None
    try:
        cur.execute("SELECT card_id FROM Cards WHERE card_number = ?", (card_number,))
        row = cur.fetchone()
        if row:
            card_id = row[0]
        else:
            cur.execute("INSERT INTO Cards (card_number) VALUES (?)", (card_number,))
            card_id = cur.lastrowid
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error in get_or_create_card: {e}")
        conn.rollback()
    finally:
        conn.close()
    return card_id


def has_access(card_id: int, location_name: str) -> bool:
    """
    Returns True if the card with the given card_id has an Access entry
    for the specified location name.
    """
    conn = connect_db()
    cur = conn.cursor()
    ok = False
    try:
        cur.execute("""
            SELECT 1 FROM Accesses A
            JOIN Locations L ON A.location_id = L.location_id
            WHERE A.card_id = ? AND L.name = ?
        """, (card_id, location_name))
        ok = cur.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Database error in has_access: {e}")
    finally:
        conn.close()
    return ok


def record_rfid_event(location_name: str, card_id: int, success: bool):
    """
    Logs 'successful_rfid_access' or 'unsuccessful_rfid_access' for a
    specific card at a location with the current timestamp.
    These events are considered momentary and are immediately marked as resolved.
    """
    event_name = 'successful_rfid_access' if success else 'unsuccessful_rfid_access'
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT event_id FROM Events WHERE name = ?", (event_name,))
        event_id_res = cur.fetchone()
        cur.execute("SELECT location_id FROM Locations WHERE name = ?", (location_name,))
        location_id_res = cur.fetchone()

        if event_id_res and location_id_res:
            event_id = event_id_res[0]
            location_id = location_id_res[0]
            cur.execute(
                "INSERT INTO Log (event_id, timestamp, location_id, card_id, is_resolved) VALUES (?, ?, ?, ?, ?)",
                (event_id, datetime.datetime.now(), location_id, card_id, True)
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error in record_rfid_event: {e}")
        conn.rollback()
    finally:
        conn.close()


create_tables()