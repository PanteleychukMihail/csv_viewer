from django.urls import path
from .views import *

urlpatterns = [
    path('', UploadCSVView.as_view(), name='upload_csv'),
    path('csv-data/<str:collection_name>/', ShowCSVDatasView.as_view(), name='csv_data'),
    path('collection-list/', CollectionListView.as_view(), name='collection_list'),
]