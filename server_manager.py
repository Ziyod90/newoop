import sqlite3


class Server:
    def __init__(self, name, ip, os, ram, cpu):
        self.name = name
        self.ip = ip
        self.os = os
        self.ram = ram
        self.cpu = cpu

    def show_info(self):
        print("-" * 40)
        print(f"ID: {getattr(self, 'id', "N/A")})")
        print(f"Name: {self.name}")
        print(f"IP: {self.ip}")
        print(f"OS: {self.os}")
        print(f"RAM: {self.ram} GB")
        print(f"CPU: {self.cpu} cores")
        print("-" * 40)


class Database:
    def __init__(self, database_name="servers.db"):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                ip TEXT NOT NULL UNIQUE,
                os TEXT NOT NULL,
                ram INTEGER NOT NULL,
                cpu INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def add_server(self, server):
        try:
            self.cursor.execute("""
                INSERT INTO servers (name, ip, os, ram, cpu)
                VALUES (?, ?, ?, ?, ?)
            """, (
                server.name,
                server.ip,
                server.os,
                server.ram,
                server.cpu
            ))

            self.connection.commit()

            print("\nServer successfully added!")
        except sqlite3.IntegrityError:
            print("\nError: server with this IP already exists!")

    def get_all_servers(self):
        self.cursor.execute("""
            SELECT id, name, ip, os, ram, cpu
            FROM servers
            order by id
        """)
        rows = self.cursor.fetchall()

        servers = []

        for row in rows:
            server = Server(
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
            )

            server.id = row[0]

            servers.append(server)

        return servers

    def find_server(self, name):
        self.cursor.execute("""
            SELECT id, name, ip, os, ram, cpu
            FROM servers
            WHERE name = ?
        """, (name,))

        row = self.cursor.fetchone()

        if row is None:
            return None

        server = Server(
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
        )

        server.id = row[0]

        return server

    def delete_server(self, server_id):
        self.cursor.execute("""
            DELETE FROM servers
            WHERE id = ?
        """, (server_id,))

        self.connection.commit()

        if self.cursor.rowcount == 0:
            print("\nServer not found!")
        else:
            print("\nServer successfully deleted!")

    def update_server(self, server_id, server):
        self.cursor.execute("""
            UPDATE servers
            SET name = ?, 
                ip = ?, 
                os = ?, 
                ram = ?,
                cpu = ?
            WHERE id =?
        """, (
            server.name,
            server.ip,
            server.os,
            server.ram,
            server.cpu
        ))

        self.connection.commit()

        if self.cursor.rowcount == 0:
            print("\nServer not found!")
        else:
            print("\nServer successfully updated!")

        def close(self):
            self.connection.close()


def get_integer(message):
    while True:
        try:
            value = int(input(message))

            if value <= 0:
                print("Please enter a number greater than zero!")
                continue

            return value

        except ValueError:
            print("Please enter a valid number!")

def create_server_from_input():
    print("\nEnter server information:")
    print("-" * 40)

    name = input("Name server: ").strip()
    ip = input("IP: ").strip()
    os = input("OS: ").strip()

    ram = input("RAM GB: ")
    cpu = input("CPU Cores: ")

    return Server(
        name=name,
        ip=ip,
        os=os,
        ram=ram,
        cpu=cpu
    )

def add_server(database):
    server = create_server_from_input()

    database.add_server(server)

def show_servers(database):
    servers = database.get_all_servers()

    if not servers:
        print("\nDatabase is empty!")

        return
    print("\n" + "=" * 40)
    print("ALL SERVERS")
    print(f"=" * 40)

    for server in servers:
        server.show_info()


def find_server(database):
    name = input("\nEnter server name: ").strip()

    server = database.find_server(name)

    if server is None:
        print("\nServer not found!")
        return

    print("\nServer found:")
    server.show_info()


def delete_server(database):
    server_id = get_integer(input("\nEnter server ID to delete: "))

    database.delete_server(server_id)

def update_server(database):
    server_id = get_integer(input("\nEnter server ID to update: "))
    server = create_server_from_input()

    database.update_server(server_id, server)

def show_menu():
    print("\n")
    print("=" * 40)
    print("       SERVER MANAGEMENT SYSTEM")
    print("=" * 40)
    print("1. Add server")
    print("2. Show all servers")
    print("3. Find server")
    print("4. Delete server")
    print("5. Update server")
    print("6. Exit")
    print("=" * 40)

def main():
    database = Database()

    try:
        while True:
            show_menu()

            choice = input("Select option: ").strip()

            if choice == "1":
                add_server(database)

            elif choice == "2":
                show_servers(database)

            elif choice == "3":
                find_server(database)

            elif choice == "4":
                delete_server(database)

            elif choice == "5":
                update_server(database)

            elif choice == "6":
                print("Thank you for using this program!")
                print("\nGoodbye!")

                break

            else:
                print("\nInvalid option. Please choose 1-6.")

    finally:
        database.close()


if __name__ == "__main__":
    main()