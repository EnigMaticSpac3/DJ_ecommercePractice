from django.urls import path
# viewpages
from .views import item_list

app_name = 'core'

urlpatterns = [
    path('', item_list, name="item-list")
]

