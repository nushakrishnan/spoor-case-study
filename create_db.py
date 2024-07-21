# Ref: https://docs.python.org/3/library/sqlite3.html#tutorial

import pandas as pd
import sqlite3

csv_file = './data/predictions.csv'
db_file = './data/predictions.db'

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
