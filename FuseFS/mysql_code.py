
import os
import mysql.connector

class MetadataStorage:
    def __init__(self, db_config):
        self.conn = mysql.connector.connect(**db_config)
        self.cursor = self.conn.cursor()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS table1 (
            file_id INT AUTO_INCREMENT PRIMARY KEY,
            file_name VARCHAR(255),
            file_size INT,
            last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_metadata(self, file_name, file_size):
        insert_query = '''
        INSERT INTO table1 (file_name, file_size)
        VALUES (%s, %s);
        '''
        self.cursor.execute(insert_query, (file_name, file_size))
        self.conn.commit()

    def get_metadata(self, file_name):
        select_query = '''
        SELECT * FROM table1 WHERE file_name = %s;
        '''
        self.cursor.execute(select_query, (file_name,))
        return self.cursor.fetchone()

    def update_metadata(self, file_name, file_size):
        update_query = '''
        UPDATE data SET file_size = %s, last_accessed = CURRENT_TIMESTAMP WHERE file_name = %s;
        '''
        self.cursor.execute(update_query, (file_size, file_name))
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

def insert_all_files_from_folder(folder_path, metadata_storage):
    for filename in os.listdir(folder_path):
        if filename.endswith(('.txt','pdf','.pptx','.docx')):
            file_path = os.path.join(folder_path, filename)
            file_size = os.path.getsize(file_path)
            metadata_storage.insert_metadata(filename, file_size)
            print(f"Inserted metadata for {filename} (size: {file_size} bytes)")

# Database connection configuration 
db_config = {
    'user': 'root',
    'password': 'Password',
    'host': 'localhost',
    'database': 'database name'
}

# Example Usage
metadata_storage = MetadataStorage(db_config)
metadata_storage.create_table()

folder_path = 'C:/Local Path' 
insert_all_files_from_folder(folder_path, metadata_storage)

metadata_storage.close()
