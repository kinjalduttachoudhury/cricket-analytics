import sqlite3

from configs import DDL
from utils.base_logger import logger


def create_tables_from_config(db_file):
    """
    This function creates tables listed in configs.DDL, if they don't exist in SQLite database
    :param db_file: path of the database file for SQLite
    :type db_file: str
    """
    connection_obj = sqlite3.connect(db_file)
    cursor_obj = connection_obj.cursor()

    for table in DDL.ddl_config.keys():
        create_table_query = "create table if not exists {table} ({columns})".format(table=table, columns=",".join(
            DDL.ddl_config[table]))
        try:
            cursor_obj.execute(create_table_query)
        except Exception as e:
            logger.exception(e)
            connection_obj.close()
            raise
        else:
            logger.info("Table {table} is created".format(table=table))
    connection_obj.close()


if __name__ == "__main__":
    db_file = '../cricket-analytics-sqlite.db'
    create_tables_from_config(db_file)
