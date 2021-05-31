from .model import Model


class FundModel(Model):
    def __init__(self):
        super(FundModel, self).__init__()

    def get_all(self):
        fields = ["fund_id", "name", "amount", "payment_type"]

        columns = self.get_columns(fields)
        query = f"SELECT {columns} FROM funds"

        return [self.to_dict(row, fields) for row in self.get(query)]

    def save(self, **kwargs):
        sql = """
            INSERT INTO funds (
                fund_id,
                name,
                amount,
                description,
                payment_type,
                institution_id
            )
            VALUES (
                '{fund_id}',
                '{name}',
                '{amount}',
                '{description}',
                '{payment_type}',
                '{institution_id}'
            );
        """

        query = sql.format(**kwargs)

        return kwargs["fund_id"] if self.set(query) else None

    def get_by(self, field, value):
        fields = [
            "fund_id",
            "name",
            "amount",
            "description",
            "payment_type",
            "status",
            "institution_id",
            "created_at",
            "updated_at"
        ]

        columns = self.get_columns(fields)
        query = f"SELECT {columns} FROM funds WHERE {field}='{value}'"
        row = self.get(query, one_row=True)

        if not row:
            return None

        return self.to_dict(row, fields)

    def search_by(self, field, value):
        query = f"SELECT COUNT(*) FROM funds WHERE {field}='{value}'"
        return self.if_exists(query)

    def migrate_table(self):
        sql = """
                CREATE TABLE funds (
                    fund_id uuid PRIMARY KEY,
                    name VARCHAR(150) NOT NULL,
                    amount NUMERIC(15, 2) NOT NULL,
                    description TEXT,
                    payment_type VARCHAR(15) NOT NULL,
                    status BOOLEAN NOT NULL DEFAULT TRUE,
                    institution_id uuid,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    CONSTRAINT fk_institution
                        FOREIGN KEY (institution_id)
                            REFERENCES institutions(id)
                            ON DELETE CASCADE
                );
            """

        self.migrate(sql, name="funds")


class CheckModel(Model):
    def __init__(self):
        super(CheckModel, self).__init__()

    def save(self, **kwargs):
        sql = """
            INSERT INTO checks (
                check_id,
                number,
                recipient,
                fund_id
            )
            VALUES (
                '{check_id}',
                '{number}',
                '{recipient}',
                '{fund_id}'
            );
        """

        query = sql.format(**kwargs)

        return True if self.set(query) else False

    def get_by(self, field, value, condition):
        fields = [
            "fund_id",
            "name",
            "amount",
            "description",
            "payment_type",
            "status",
            "institution_id",
            "check_id",
            "number",
            "recipient",
        ]

        columns = self.get_columns(fields)
        query = f"""
            SELECT {columns}
            FROM funds
            JOIN checks ON fund_id=checks.fund_id
            WHERE {condition}.{field}='{value}'
        """
        row = self.get(query, one_row=True)

        if not row:
            return None

        return self.to_dict(row, fields)

    def search_by(self, field, value):
        query = f"""
            SELECT COUNT(*)
            FROM funds
            JOIN checks ON fund_id=checks.fund_id
            WHERE checks.{field}='{value}'
        """
        return self.if_exists(query)

    def migrate_table(self):
        sql = """
            CREATE TABLE checks (
                check_id uuid PRIMARY KEY,
                number VARCHAR(100) NOT NULL,
                recipient VARCHAR(100) NOT NULL,
                fund_id uuid,
                CONSTRAINT fk_fund
                    FOREIGN KEY (fund_id)
                        REFERENCES funds(id)
                        ON DELETE CASCADE
            );
        """

        self.migrate(sql, name="checks")


class BankTransferModel(Model):
    def __init__(self):
        super(BankTransferModel, self).__init__()

    def save(self, **kwargs):
        sql = """
            INSERT INTO bank_transfers (
                bank_transfer_id,
                bank_name,
                account_name,
                fund_id
            )
            VALUES (
                '{bank_transfer_id}',
                '{bank_name}',
                '{account_name}',
                '{fund_id}'
            );
        """

        query = sql.format(**kwargs)

        return True if self.set(query) else False

    def get_by(self, field, value, condition):
        fields = [
            "fund_id",
            "name",
            "amount",
            "description",
            "payment_type",
            "status",
            "institution_id",
            "bank_transfer_id",
            "bank_name",
            "account_name",
        ]

        columns = self.get_columns(fields)
        query = f"""
            SELECT {columns}
            FROM funds
            JOIN checks ON fund_id=checks.fund_id
            WHERE {condition}.{field}='{value}'
        """
        row = self.get(query, one_row=True)

        if not row:
            return None

        return self.to_dict(row, fields)

    def search_by(self, field, value):
        query = f"""
            SELECT COUNT(*)
            FROM funds
            JOIN bank_transfers ON fund_id=bank_transfers.fund_id
            WHERE bank_transfers.{field}='{value}'
        """
        return self.if_exists(query)

    def migrate_table(self):
        sql = """
            CREATE TABLE bank_transfers (
                bank_transfer_id uuid PRIMARY KEY,
                bank_name VARCHAR(100) NOT NULL,
                account_name VARCHAR(100) NOT NULL,
                fund_id uuid,
                CONSTRAINT fk_fund
                    FOREIGN KEY (fund_id)
                        REFERENCES funds(id)
                        ON DELETE CASCADE
            );
        """

        self.migrate(sql, name="bank_transfers")
