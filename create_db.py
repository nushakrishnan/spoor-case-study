# Ref: https://docs.python.org/3/library/sqlite3.html#tutorial

import pandas as pd
import sqlite3
import argparse


def main(csv_file, db_file):
    data = pd.read_csv(csv_file)
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            Class TEXT,
            Timestamp TEXT,
            Frame INTEGER,
            BoundingBox_Coord_1 REAL,
            BoundingBox_Coord_2 REAL,
            BoundingBox_Coord_3 REAL,
            BoundingBox_Coord_4 REAL,
            Confidence REAL
        )
    ''')

    data.to_sql('detections', connection, if_exists='append', index=False)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create a SQLite database from a CSV file.')

    parser.add_argument('csv_file',
                        type=str,
                        help='Path to the input CSV file.')
    parser.add_argument('db_file',
                        type=str,
                        help='Path to the output database file.')

    args = parser.parse_args()
    main(args.csv_file, args.db_file)
