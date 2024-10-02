import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def open_connection(self):
        self.connection = sqlite3.connect(self.db_name)
        print("Соединение с базой данных установлено.")

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто.")

    def execute_query(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        return cursor

    def find_user_by_name(self, name):
        search_query = "SELECT * FROM users WHERE name = ?;"
        cursor = self.execute_query(search_query, (name,))
        return cursor.fetchall() if cursor else None

    def execute_transaction(self, queries_with_params):
        cursor = self.connection.cursor()
        for query, params in queries_with_params:
            cursor.execute(query, params)
        self.connection.commit()


class User:
    def __init__(self, db_manager):
        self.db_manager = db_manager


    def create_user_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        );
        '''
        self.db_manager.execute_query(create_table_query)


    def add_user(self, name, role):
        insert_query = 'INSERT INTO users (name, role) VALUES (?, ?);'
        self.db_manager.execute_query(insert_query, (name, role))

    def get_user_by_id(self, user_id):
        select_query = 'SELECT * FROM users WHERE id = ?;'
        cursor = self.db_manager.execute_query(select_query, (user_id,))
        return cursor.fetchone() if cursor else None


    def delete_user_by_id(self, user_id):
        delete_query = 'DELETE FROM users WHERE id = ?;'
        self.db_manager.execute_query(delete_query, (user_id,))

class Admin(User):
    def create_admin_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            department TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        '''
        self.db_manager.execute_query(create_table_query)

    def add_admin(self, user_id, department):
        insert_query = 'INSERT INTO admins (user_id, department) VALUES (?, ?);'
        self.db_manager.execute_query(insert_query, (user_id, department))

class Customer(User):
    def create_customer_table(self):
        create_table_query = '''
CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            address TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
        '''
        self.db_manager.execute_query(create_table_query)

    def add_customer(self, user_id, address):
        insert_query = 'INSERT INTO customers (user_id, address) VALUES (?, ?);'
        self.db_manager.execute_query(insert_query, (user_id, address))

if __name__ == "__main__":
    db_manager = DatabaseManager("banking_system.db")
    db_manager.open_connection()

    user_manager = User(db_manager)
    user_manager.create_user_table()
    user_manager.add_user("Яхье", "customer")
    user_manager.add_user("Бекболот", "admin")
    admin_manager = Admin(db_manager)
    admin_manager.create_admin_table()
    admin_manager.add_admin(2, "IT")
    customer_manager = Customer(db_manager)
    customer_manager.create_customer_table()
    customer_manager.add_customer(1, "ул. Ленина, д. 10")

    users = db_manager.find_user_by_name("Яхье")
    print("Найденные пользователи:", users)


    transaction_queries = [
        ('INSERT INTO users (name, role) VALUES (?, ?);', ("Бексултан Назарбаев", "customer")),
        ('INSERT INTO customers (user_id, address) VALUES (?, ?);', (3, "ул. Масалиева, д. 5"))
    ]
    db_manager.execute_transaction(transaction_queries)

    db_manager.close_connection()