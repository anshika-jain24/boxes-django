from django.urls import path

from .views import list_boxes, list_my_boxes, add_box, delete_box, update_box, register_user

app_name = 'boxes'

urlpatterns = [
    path('list', list_boxes, name='list_boxes'),
    path('my-boxes', list_my_boxes, name='list_my_boxes'),
    path('create', add_box, name='add_box'),
    path('update/<int:id>', update_box, name='update_box'),
    path('delete/<int:id>', delete_box, name='delete_box'),
    path('register', register_user, name='register_user'),
]
