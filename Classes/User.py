from Classes.Database import Database


class User:
    def __init__(self):
        pass

    def get_data(self, username):
        users = Database.get_data(
            self, "./Data/Players/Users.db", "users", None)
        for user in users:
            if user[0] == username:
                user_data = user
                return user_data
            
    def get_username(self):
        file = open("./Data/Players/CurrentUser.txt", "r")
        data = file.readlines()
        username = data[0]
        return username

    def login(self):
        Database.create_table(self, "./Data/Players/Users.db", "users",
                              "username STRING, password STRING, characters INTEGER, levels INTEGER")
        username = input("Enter username: ")

        # Check 'Users.db' for existing users
        users = Database.get_data(
            self, "./Data/Players/Users.db", "users", None)
        user_exists = False
        if self.get_data(username):
            user_exists = True

        # Create new user if not already exists
        if not user_exists:
            create = input(
                f"User account {username} does not exist, would you like to create one?\n")
            if create.lower() == "yes":
                Database.insert_value(self, "./Data/Players/Users.db",
                                      "users", username, "password", 1, 1)
                print(f"User account {username} created")

        # Update 'CurrentUser.txt'
        file = open("./Data/Players/CurrentUser.txt", "w")
        file.write(str(username))
        file.close()
        return username
