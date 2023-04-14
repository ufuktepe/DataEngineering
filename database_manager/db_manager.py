import psycopg2

from static import constants as const
from .db_error import DBError


class DBManager:
    def __init__(self):
        self.host = None            # Database server
        self.port = None            # Database port
        self.user = None            # Username for the database
        self.password = None        # Password for the database
        self.database = None        # Name of the database
        self.metadata_table = None  # Metadata table name
        self.results_table = None   # Results table name
        self.status_table = None    # Status table name

    def setup(self, config):
        """
        Assign database properties.
        """
        self.validate(config)
        self.host = config.db_host
        self.port = config.db_port
        self.user = config.db_username
        self.password = config.db_password
        self.database = config.db_name
        self.metadata_table = config.db_table_metadata
        self.results_table = config.db_table_results
        self.status_table = config.db_table_status

    def validate(self, config):
        """
        Validate database properties.
        """
        if config.db_host is None:
            raise DBError('Missing database host!')
        if config.db_port is None:
            raise DBError('Missing database port!')
        if config.db_username is None:
            raise DBError('Missing database username!')
        if config.db_password is None:
            raise DBError('Missing database password!')
        if config.db_name is None:
            raise DBError('Missing database name!')
        if config.db_table_metadata is None:
            raise DBError('Missing metadata table name!')
        if config.db_table_results is None:
            raise DBError('Missing results table name!')
        if config.db_table_status is None:
            raise DBError('Missing status table name!')

    def get_connection(self):
        """
        Return a connection object.
        """
        try:
            return psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Exception as e:
            raise DBError(msg=str(e))

    def get_layout(self, run_id):
        """
        Return the layout for the given run ID.
        """
        connection = self.get_connection()

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"""SELECT {const.LAYOUT_TITLE} FROM {self.metadata_table} WHERE acc='{run_id}'""")
                row = cursor.fetchone()
                return row[0] if row else None
        except Exception as e:
            raise DBError(msg=str(e))
        finally:
            if connection is not None:
                connection.close()

    def post_results(self, csv_path):
        """
        Post the results in the given csv file to the results table.
        """
        connection = self.get_connection()
        sql_stmnt = f"""COPY {self.results_table} (acc, taxon, confidence, abundance) FROM stdin WITH CSV HEADER DELIMITER as ','"""

        try:
            with connection.cursor() as cursor:
                with open(csv_path, 'r') as f:
                    cursor.copy_expert(sql=sql_stmnt, file=f)
            connection.commit()
        except Exception as e:
            raise DBError(msg=str(e))
        finally:
            if connection is not None:
                connection.close()

    def update_status(self, run_id, status):
        """
        Update the status table for the given run ID.
        """
        connection = self.get_connection()
        sql_stmnt = f""" UPDATE {self.status_table} SET status={status}, updated_at=NOW() WHERE acc='{run_id}'"""

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_stmnt)
            connection.commit()
        except Exception as e:
            raise DBError(msg=str(e))
        finally:
            if connection is not None:
                connection.close()

    def create_init_status(self, run_id):
        connection = self.get_connection()
        status = 0

        sql_stmnt = f"""INSERT INTO {self.status_table} (acc, status, created_at, updated_at) VALUES ('{run_id}',
         {status},NOW(), NOW())"""

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_stmnt)
            connection.commit()
        except Exception as e:
            raise DBError(msg=str(e))
        finally:
            if connection is not None:
                connection.close()



# Singleton
db_manager = DBManager()



