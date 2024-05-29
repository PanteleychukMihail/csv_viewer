from django.urls import path
from .views import *

urlpatterns = [
    path('upload-csv/', UploadCSVView.as_view(), name='upload_csv'),
]