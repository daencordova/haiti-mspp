from .model import Model


class UserModel(Model):
    def __init__(self):
        super(UserModel, self).__init__()

    def get_all(self):
        fields = ["user_id", "fullname", "username", "role"]

        columns = self.get_columns(fields)
        query = f"SELECT {columns} FROM users"

        return [self.to_dict(row, fields) for row in self.get(query)]

    def save(self, **kwargs):
        sql = """
            INSERT INTO users (
                user_id,
                fullname,
                username,
                email,
                password,
                role
            )
            VALUES (
                '{user_id}',
                '{fullname}',
                '{username}',
                '{email}',
                '{password}',
                '{role}'
            )
        """

        query = sql.format(**kwargs)

        return kwargs["user_id"] if self.set(query) else None

    def get_password(self, user_id):
        query = f"SELECT password FROM users WHERE user_id='{user_id}'"
        row = self.get(query, one_row=True)

        if not row:
            return None

        return self.to_dict(row, fields=["password"])

    def get_for_login(self, username):
        fields = ["user_id", "username", "email", "password", "role"]

        columns = self.get_columns(fields)
        query = f"SELECT {columns} FROM users WHERE username='{username}'"
        row = self.get(query, one_row=True)

        if not row:
            return None

        return self.to_dict(row, fields)

    def get_by(self, field, value):
        fields = [
            "user_id",
            "fullname",
            "username",
            "email",
            "role",
            "status",
            "created_at",
            "updated_at",
        ]

        columns = self.get_columns(fields)
        query = f"SELECT {columns} FROM users WHERE {field}='{value}'"
        row = self.get(query, one_row=True)

        if not row:
            return None

        return self.to_dict(row, fields)

    def search_by(self, field, value):
        query = f"SELECT COUNT(*) FROM users WHERE {field}='{value}'"
        return self.if_exists(query)

    def change_password(self, id, password):
        query = f"UPDATE users SET password='{password}' WHERE user_id='{id}'"
        return self.set(query)

    def delete(self, id):
        query = f"DELETE FROM users WHERE user_id='{id}'"
        return self.set(query)

    def migrate_table(self):
        sql = """
            CREATE TABLE users (
                user_id uuid PRIMARY KEY,
                fullname VARCHAR(70) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(70) UNIQUE NOT NULL,
                password VARCHAR(250) NOT NULL,
                role VARCHAR(15) NOT NULL DEFAULT 'user',
                status BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """

        self.migrate(sql, name="users")
