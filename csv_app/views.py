from typing import Any, Dict

from django.contrib import messages
from django.urls import reverse

from .csv_processor import CSVProcessor, MongoDBManager

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView


class UploadCSVView(View):
    """View for uploading CSV files and saving them to MongoDB."""
    template_name = 'csv_app/csv_loader.html'

    def __init__(self) -> None:
        super().__init__()
        self.db_manager = MongoDBManager()

    def get(self, request: Any) -> Any:
        return render(request, self.template_name)

    def post(self, request: Any) -> Any:
        uploaded_file = request.FILES.get('csv_file')

        db_manager = self.db_manager
        csv_processor = CSVProcessor(db_manager)

        if not csv_processor.is_valid_csv(uploaded_file):
            messages.error(request, 'Is not a CSV file')
            return redirect('upload_csv')

        uploaded_file.seek(0)

        collection_name: str = uploaded_file.name
        new_collection_name: str = csv_processor.save_csv_to_mongo(uploaded_file, collection_name)

        return HttpResponseRedirect(reverse('csv_data', kwargs={'collection_name': new_collection_name}))


class ShowCSVDatasView(View):
    """View for displaying CSV data stored in MongoDB."""
    template_name = 'csv_app/csv_data.html'

    def __init__(self):
        super().__init__()
        self.db_manager = MongoDBManager()

    def get(self, request: Any, collection_name: str) -> Any:
        csv_processor = CSVProcessor(self.db_manager)
        collection = csv_processor.db[collection_name]
        data = list(collection.find())
        headers = list(data[0].keys()) if data else []

        return render(request, self.template_name,
                      {'csv_data': data, 'headers': headers, 'collection_name': collection_name})


class CollectionListView(TemplateView):
    """View for listing collections stored in MongoDB."""
    template_name = 'csv_app/collection_list.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        manager = MongoDBManager()
        db = manager.get_database()
        collections = db.list_collection_names()
        context['collections'] = collections
        return context
