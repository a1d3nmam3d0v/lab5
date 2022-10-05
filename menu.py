import sqlite3

db = "juggling_records.sqlite"

with sqlite3.connect(db) as con:
    con.execute(
        "CREATE TABLE IF NOT EXISTS records (name TEXT, country TEXT, catches INT, UNIQUE (name COLLATE NOCASE, country COLLATE NOCASE))"
    )
con.close()

jugglers = [
    ("Janne Mustonen", "Finland", 98),
    ("Ian Stewart", "Canada", 94),
    ("Aaron Gregg", "Canada", 88),
    ("Chadd Taylor", "USA", 78),
]

try:
    with sqlite3.connect(db) as con:
        con.executemany("INSERT INTO records VALUES (?,?,?)", jugglers)
    con.close()
except sqlite3.Error as e:
    print(e, ",\nbut everythings alright keep going")
    # Constraint violation (because duplicate name and country)  each time  the program runs (after the first time )
    # unless you delete the DB file first
    # todo change this


# todo add the database and fill in the functions.


def main():
    menu_text = """
    1. Display all records
    2. Add new record
    3. Edit existing record
    4. Delete record 
    5. Quit
    """

    while True:
        print(menu_text)
        choice = input("Enter your choice: ")
        print()
        if choice == "1":
            display_all_records()
        elif choice == "2":
            add_new_record()
        elif choice == "3":
            edit_existing_record()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            break
        else:
            print("Not a valid selection, please try again")


def display_all_records():
    con = sqlite3.connect(db)
    all_records = con.execute("SELECT rowid, * FROM records")

    for record in all_records:
        print(record)
    con.close()


def edit_existing_record():
    row_id_to_edit = input("Enter row id of record you want to edit:  ")
    updated_catches = int(input("Enter new number of catches: "))

    try:
        with sqlite3.connect(db) as con:
            con.execute(
                "UPDATE records set catches = ? WHERE rowid = ?",
                (updated_catches, row_id_to_edit),
            )
    except sqlite3.Error as e:
        print(e)
        print("Error updating. Table not modified.")
    finally:
        con.close()


def add_new_record():
    new_name = input("Jugglers name?  ")
    new_country = input("Their country? ")
    new_catches = int(input("Number of catches? "))
    add_new_record_sql = "INSERT INTO records  (name, country, catches) VALUES (?,?,?)"
    try:
        with sqlite3.connect(db) as con:
            con.execute(add_new_record_sql, (new_name, new_country, new_catches))
    except sqlite3.IntegrityError:  # integrity errror if user tries to add a record that has the same name AND country as existing record because of unique constraints
        print("That juggler is already in the table.")
        edit_existing = input(
            "Instead, do you want to edit an existing record? y/n "
        ).upper()
        if edit_existing == "Y":
            edit_existing_record()
        else:
            con.close()


def delete_record():
    name_to_delete = input("Enter name of juggler to delete:  ")
    delete_sql = "DELETE  FROM records WHERE name = ?"

    with sqlite3.connect(db) as con:
        con.execute(delete_sql, (name_to_delete,))
    con.close()


if __name__ == "__main__":
    main()
