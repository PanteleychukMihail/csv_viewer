from .csv_processor import CSVProcessor

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


class UploadCSVView(View):
    template_name = 'csv_app/csv_loader.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        uploaded_file = request.FILES.get('csv_file')
        csv_processor = CSVProcessor()
        if not csv_processor.is_csv(uploaded_file):
            return HttpResponse('Не той тип файлу')

        uploaded_file.seek(0)

        collection_name = uploaded_file.name
        csv_processor.save_csv_to_mongo(uploaded_file, collection_name)

        return HttpResponse('upload_success')
