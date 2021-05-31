from .model import Model


class InstitutionModel(Model):
    def __init__(self):
        super(InstitutionModel, self).__init__()

    def get_all(self):
        fields = ["institution_id", "code", "name"]

        columns = self.get_columns(fields)
        query = f"SELECT {columns} FROM institutions"

        return [self.to_dict(row, fields) for row in self.get(query)]

    def save(self, **kwargs):
        sql = """
            INSERT INTO institutions (
                institution_id,
                code,
                name,
                authorising_officer,
                email,
                telephone,
                website,
                address,
                user_id
            )
            VALUES (
                '{institution_id}',
                '{code}',
                '{name}',
                '{authorising_officer}',
                '{email}',
                '{telephone}',
                '{website}',
                '{address}',
                '{user_id}'
            )
        """

        query = sql.format(**kwargs)

        return kwargs["institution_id"] if self.set(query) else None

    def get_by(self, field, value):
        fields = [
            "institution_id",
            "code",
            "name",
            "authorising_officer",
            "email",
            "telephone",
            "website",
            "address",
            "status",
            "created_at",
            "updated_at",
            "user_id",
        ]

        columns = self.get_columns(fields)
        query = f"SELECT {columns} FROM institutions WHERE {field}='{value}'"
        row = self.get(query, one_row=True)

        if not row:
            return None

        return self.to_dict(row, fields)

    def search_by(self, field, value):
        query = f"SELECT COUNT(*) FROM institutions WHERE {field}='{value}'"
        return self.if_exists(query)

    def update(self, institution_id, **kwargs):
        sql = """
            UPDATE institutions
            SET code='{code}',
                name='{name}',
                authorising_officer='{authorising_officer}',
                email='{email}',
                telephone='{telephone}',
                website='{website}',
                address='{address}',
                status='{status}',
                user_id='{user_id}'
            WHERE institution_id='{institution_id}'
        """

        query = sql.format(institution_id=institution_id, **kwargs)

        return self.set(query)

    def delete(self, institution_id):
        query = f"DELETE FROM institutions WHERE institution_id='{institution_id}'"
        return self.set(query)

    def migrate_table(self):
        sql = """
            CREATE TABLE institutions (
                institution_id uuid PRIMARY KEY,
                code VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(150) UNIQUE NOT NULL,
                authorising_officer VARCHAR(170) NOT NULL,
                email VARCHAR(100),
                telephone VARCHAR(50),
                website VARCHAR(50),
                address VARCHAR(200),
                status BOOLEAN NOT NULL DEFAULT TRUE,
                user_id uuid,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_user
                    FOREIGN KEY (user_id)
                        REFERENCES users(id)
                        ON DELETE CASCADE
            );
        """

        self.migrate(sql, name="institutions")
