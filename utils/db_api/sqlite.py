import sqlite3


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            added_at TIMESTAMP DEFAULT (datetime('now', '+2 hours')),
            Name varchar(255),
            baby_name varchar(255),
            nickname varchar(255),
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    def create_table_reviews(self):
        sql = """
            CREATE TABLE Reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                added_at TIMESTAMP DEFAULT (datetime('now', '+2 hours')),
                user_id int NOT NULL,
                Name varchar(255),
                nickname varchar(255),
                baby_name varchar(255),
                review varchar(255) NOT NULL
                );
"""
        self.execute(sql, commit=True)

    def create_table_month_reviews(self):
        sql = """
            CREATE TABLE Month_Reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                added_at TIMESTAMP DEFAULT (datetime('now', '+2 hours')),
                user_id int NOT NULL,
                Name varchar(255),
                nickname varchar(255),
                baby_name varchar(255),
                mark varchar(255),
                month_review varchar(255)
                );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, id: int, Name: str, nickname: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"
        sql = """
                INSERT INTO Users(id, Name, nickname) VALUES(?, ?, ?)
                """
        self.execute(sql, parameters=(id, Name, nickname), commit=True)


    def add_review(self, user_id: int, Name: str, nickname: str, baby_name:str, review: str):
        sql = """
                INSERT INTO Reviews(user_id, Name, nickname, baby_name, review) VALUES (?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id, Name, nickname, baby_name, review), commit=True)

    def add_month_review(self, Name: str, nickname: str, baby_name: str, month_review: str, user_id: str):
        sql = """
                        UPDATE Month_Reviews SET Name=?, nickname=?, baby_name=?, month_review=? WHERE user_id = ?  
                """
        self.execute(sql, parameters=(Name, nickname, baby_name, month_review, user_id), commit=True)

    def update_month_mark(self, mark: str, user_id: int):
        sql = f"""
                    INSERT INTO Month_Reviews(mark, user_id) VALUES (?, ?)
                        """
        return self.execute(sql, parameters=(mark, user_id), commit=True)


    def select_all_users(self):
        sql = """
                SELECT * FROM Users
                """
        return self.execute(sql, fetchall=True)


    def select_all_reviews(self):
        sql = """
                SELECT * FROM Reviews
                """
        return self.execute(sql, fetchall=True)

    def select_all_users_id(self):
        sql = """
                SELECT id FROM Users
                """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
                UPDATE Users SET email=? WHERE id=?
                """
        return self.execute(sql, parameters=(email, id), commit=True)

    def update_user_name(self, name, id):

        sql = f"""
                UPDATE Users SET name=? WHERE id=?
                """
        return self.execute(sql, parameters=(name, id), commit=True)

    # def update_is_baby(self, is_baby, id):
    #
    #     sql = f"""
    #             UPDATE Users SET is_baby=? WHERE id=?
    #             """
    #     return self.execute(sql, parameters=(is_baby, id), commit=True)

    def update_baby_name(self, baby_name, id):

        sql = f"""
                UPDATE Users SET baby_name=? WHERE id=?
                """
        return self.execute(sql, parameters=(baby_name, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def delete_month_reviews(self):
        self.execute("DELETE FROM Month_Reviews WHERE TRUE", commit=True)

def logger(statement):
    print(f"""
    _____________________________________________________        
    Executing: 
    {statement}
    _____________________________________________________
    """)