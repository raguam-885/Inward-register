from users.views import (
    admin_department_creation, 
    choice_field, user_creation, 
    department_list, 
    user_creation_choice_field, 
    user_list,
    cell_list,
    committee_list
)
from django.urls import path

urlpatterns = [
    path('department/create', admin_department_creation, name='department_creation'),
    path('user_create_choice/', user_creation_choice_field, name='user_creation_choice'),
    path('choice_field/', choice_field, name='choice_field'),
    path('create-user/', user_creation, name='create-user'),
    path('department/list', department_list, name="department_list"),
    path('user/list', user_list, name='user_list'),
    path('cell/list', cell_list, name='cell_name'),
    path('committee/list', committee_list, name='committee_list')
]
