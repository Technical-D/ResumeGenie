import sqlite3
import secrets

# Database connection
def connect_db(db_name="api_keys.db"):
    connection = sqlite3.connect(db_name)
    return connection

# Creating Api key table
def create_table(connection):
    with connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT UNIQUE NOT NULL,
                contact_email TEXT NOT NULL,
                api_key TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    print("Table created successfully!")

# Generating a secure API key
def generate_api_key():
    return secrets.token_hex(32)

# Adding business_name and their respective api key into db
def add_api_key(connection, business_name, contact_email):
    api_key = generate_api_key()
    try:
        with connection:
            connection.execute('''
                INSERT INTO api_keys (business_name, contact_email, api_key)
                VALUES (?, ?, ?)
            ''', (business_name, contact_email, api_key))
        print(f"API key generated for {business_name}: {api_key}")
    except sqlite3.IntegrityError:
        print("Error: Business name already exists. Please choose a different name.")

# Viewing all the api keys
def view_api_keys(connection):
    with connection:
        keys = connection.execute('SELECT * FROM api_keys').fetchall()
        for key in keys:
            print(key)

# Main function
def main():
    db_name = "api_keys.db"
    connection = connect_db(db_name)
    create_table(connection)
    
    while True:
        print("\nOptions:")
        print("1. Add API Key")
        print("2. View API Keys")
        print("3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            business_name = input("Enter business name: ")
            contact_email = input("Enter contact email: ")
            add_api_key(connection, business_name, contact_email)
        elif choice == "2":
            view_api_keys(connection)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()

if __name__ == '__main__':
    main()
