from utils.create_tables import create_tables_from_config
from utils.insert_data import insert_data_to_tables
from utils.download_files import download_and_extract_json_files


def main():
    path_to_files = 'data/'
    db_file = 'cricket-analytics-sqlite.db'
    download_and_extract_json_files(path_to_files)
    create_tables_from_config(db_file)
    insert_data_to_tables(path_to_files, db_file)


if __name__ == "__main__":
    main()
