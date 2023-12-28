import sqlite3 



with sqlite3.connect('../data/library.db') as connect:
    cursor = connect.cursor()

    val = (0, 'test_Canvas0')

    cursor.execute("""
    SELECT EXISTS (
        SELECT id, name FROM(
            SELECT id, name FROM Album
            UNION SELECT id, name FROM Canvas
            UNION SELECT id, name FROM Journal
            UNION SELECT id, name FROM Layflat
            UNION SELECT id, name FROM Photobook
            UNION SELECT id, name FROM Photofolder
            UNION SELECT id, name FROM Subproduct
        )
        WHERE id != ? AND name=?
    )""",
    val
    )

    print(*cursor.fetchone())