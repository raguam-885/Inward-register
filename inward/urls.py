from django.urls import path
from inward.views import upload_file, inward_view

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('list/', inward_view, name='inward_list')
]
