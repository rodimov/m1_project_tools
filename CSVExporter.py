import sqlite3 as sql
import os
import csv


def export_to_csv(db_path, csv_path):
    conn = sql.connect(db_path)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")

    with open(csv_path, "w", newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])

        data = cursor.fetchone()

        while data is not None and len(data):
            csv_writer.writerow(data)
            data = cursor.fetchone()

        print(f'Exported: {db_path}')


def get_all_dir(path):
    return [name for name in os.listdir(path) if os.path.isdir(path + name)]


def get_all_db(path):
    return [name for name in os.listdir(path) if name.endswith(".db")]


def export_dir(path):
    servers_dirs = get_all_dir(path)

    for server_dir in servers_dirs:
        csv_path = path + server_dir + "_csv/"
        db_path = path + server_dir + "/db/"

        if not os.path.exists(csv_path):
            os.makedirs(csv_path)

        db_files = get_all_db(db_path)

        for db_file in db_files:
            csv_filename = os.path.splitext(db_file)[0] + '.csv'
            export_to_csv(db_path + db_file, csv_path + csv_filename)
