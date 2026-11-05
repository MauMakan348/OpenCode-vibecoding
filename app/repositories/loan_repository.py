def create_loan(db, student_id, item_id, quantity):
    """Insert a new loan with status BORROWED and return its id."""
    cursor = db.execute(
        """
        INSERT INTO loan (student_id, item_id, quantity, status)
        VALUES (?, ?, ?, 'BORROWED')
        """,
        (student_id, item_id, quantity),
    )
    return cursor.lastrowid


def get_loan_by_id(db, loan_id):
    """Return one loan by id, or None if it does not exist."""
    return db.execute("SELECT * FROM loan WHERE id = ?", (loan_id,)).fetchone()


def update_loan_status(db, loan_id, status):
    """Set a loan status. Returns True when a row was updated."""
    cursor = db.execute(
        "UPDATE loan SET status = ? WHERE id = ?",
        (status, loan_id),
    )
    return cursor.rowcount == 1


def mark_returned(db, loan_id):
    """Set a BORROWED loan to RETURNED. Returns True when a row was updated.

    The status condition prevents a second return from restoring stock twice.
    """
    cursor = db.execute(
        """
        UPDATE loan
        SET status = 'RETURNED'
        WHERE id = ? AND status = 'BORROWED'
        """,
        (loan_id,),
    )
    return cursor.rowcount == 1


def get_loans_by_student_id(db, student_id):
    """Return one student's loans, newest first."""
    return db.execute(
        """
        SELECT * FROM loan
        WHERE student_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (student_id,),
    ).fetchall()
