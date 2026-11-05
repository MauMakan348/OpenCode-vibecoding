def create_item(db, name, total_stock, available_stock):
    """Insert a new item and return its id."""
    cursor = db.execute(
        """
        INSERT INTO item (name, total_stock, available_stock)
        VALUES (?, ?, ?)
        """,
        (name, total_stock, available_stock),
    )
    return cursor.lastrowid


def get_all_items(db):
    """Return every item ordered by id."""
    return db.execute("SELECT * FROM item ORDER BY id").fetchall()


def get_item_by_id(db, item_id):
    """Return one item by id, or None if it does not exist."""
    return db.execute("SELECT * FROM item WHERE id = ?", (item_id,)).fetchone()


def decrement_available_stock(db, item_id, quantity):
    """Subtract quantity only when stock is sufficient.

    Returns True when a row was updated, False when stock was insufficient
    or the item does not exist.
    """
    cursor = db.execute(
        """
        UPDATE item
        SET available_stock = available_stock - ?
        WHERE id = ? AND available_stock >= ?
        """,
        (quantity, item_id, quantity),
    )
    return cursor.rowcount == 1


def increment_available_stock(db, item_id, quantity):
    """Add quantity back to available_stock.

    Returns True when the item was updated. The schema check keeps
    available_stock from exceeding total_stock.
    """
    cursor = db.execute(
        """
        UPDATE item
        SET available_stock = available_stock + ?
        WHERE id = ?
        """,
        (quantity, item_id),
    )
    return cursor.rowcount == 1
