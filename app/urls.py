from django.urls import path
from .views import ItemListView, ItemDetailView, ItemCreateView, MyReportsListView, ItemUpdateView, ItemDeleteView
from .views import mark_as_recovered

urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),
    path('item/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('report/', ItemCreateView.as_view(), name='item_report'),
    path('item/<int:pk>/recovered/', mark_as_recovered, name='mark_recovered'),
    path('my-reports/', MyReportsListView.as_view(), name='my_reports'),
    path('item/<int:pk>/edit/', ItemUpdateView.as_view(), name='item_edit'),
    path('item/<int:pk>/delete/', ItemDeleteView.as_view(), name='item_delete'),
]