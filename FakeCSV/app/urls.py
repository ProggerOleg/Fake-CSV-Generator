from django.urls import path
from .views import *

urlpatterns = [
    path("", LoginUser.as_view(), name="login"),
    path("schemas/", schemas, name="schemas"),
    path("logout/", logout_user, name="logout"),
    path("new_schema/", create_schema, name="new_schema"),
    # path("name_schema", name_schema, name="name_schema")
    path('new_schema/<int:item_id>/delete/', delete_item, name='delete_item'),
    path('schemas/<int:schema_id>/delete/', delete_schema, name='delete_schema'),
    path('data_sets/<int:schema_id>/', data_sets, name='data_sets'),
    path('data_sets/<int:dataset_id>/download/', schema_dataset_download, name='dataset_download'),
]
