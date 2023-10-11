import sqlite3


def create_clear_log():
    with sqlite3.connect('../data/mail_samples.db') as db:
        db.cursor().execute("""CREATE TABLE Samples (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                tag TEXT,
                                name TEXT,
                                sample TEXT
                                )""")
        val = [(f'tag{x%2}', f'name{x}', f'some_text\nsome_text {"with ?%var?%" if x%2==0 else "without var"} and\nsome_text') for x in range(20)]
        db.executemany('INSERT INTO Samples (tag, name, sample) VALUES (?, ?, ?)', val)


if __name__ == '__main__':
    create_clear_log()