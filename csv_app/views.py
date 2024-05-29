import csv

from _csv import reader
from io import TextIOWrapper

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from pymongo import MongoClient, collection

client = MongoClient('mongodb://localhost:27017/')
db = client['csv_files']


def is_csv(file):
    try:
        dialect = csv.Sniffer().sniff(TextIOWrapper(file).read(1024))
        return True
    except csv.Error:
        return False


def save_csv_to_mongo(csv_file, collection_name, database):
    csv_reader = reader(TextIOWrapper(csv_file, encoding='utf-8'))
    headers = next(csv_reader)
    data = []

    for row in csv_reader:
        data_row = dict(zip(headers, row))
        data.append(data_row)

    try:
        collection = database[collection_name]
    except KeyError:
        collection = database.create_collection(collection_name)

    collection.insert_many(data)
    csv_file.close()
    return len(data)


class UploadCSVView(View):
    template_name = 'csv_app/csv_loader.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        uploaded_file = request.FILES.get('csv_file')
        if not is_csv(uploaded_file):
            return HttpResponse('Не той тип файлу')

        collection_name = uploaded_file.name
        print(collection_name)
        save_csv_to_mongo(uploaded_file, collection_name, db)

        return HttpResponse('upload_success')
