"""Module for handling CSV file processing and MongoDB interaction."""

import csv
from typing import List, TextIO

from pymongo import MongoClient

from csv_viewer import settings


class CSVProcessor:
    """A class to handle CSV file processing and MongoDB interaction."""

    def __init__(self, db_uri: str = settings.MONGO_DB_URI, db_name: str = settings.MONGO_DB_NAME):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]

    def is_csv(self, file) -> bool:
        """Check if the provided file is a valid CSV file."""

        try:
            uploaded_file_content = file.read(1024).decode('utf-8')
            dialect = csv.Sniffer().sniff(uploaded_file_content)
            return True

        except (csv.Error, UnicodeDecodeError):
            return False

    def get_collection_name(self, file_name: str, headers: List[str]) -> str:
        """Generate a collection name based on the file name and headers."""
        return f"{file_name}_{hash(''.join(headers))}"

    def save_csv_to_mongo(self, csv_file: TextIO, file_name: str) -> int:
        """Save the contents of a CSV file to MongoDB."""

        csv_content = csv_file.read().decode('utf-8')
        csv_reader = csv.reader(csv_content.splitlines())
        headers = next(csv_reader)
        data = []

        for row in csv_reader:
            data_row = dict(zip(headers, row))
            data.append(data_row)

        collection_name = self.get_collection_name(file_name, headers)
        collection = self.db[collection_name]

        if collection_name not in self.db.list_collection_names():
            collection = self.db.create_collection(collection_name)

        collection.delete_many({})
        collection.insert_many(data)
        csv_file.close()
        return len(data)
