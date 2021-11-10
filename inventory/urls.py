from django.urls import path
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list', views.ObjectListView.as_view(), name='list'),
    path('grid', views.ObjectGridView.as_view(), name='grid'),
    path('add', views.object_form, name='add'),
    path('<uuid:object_id>/change', views.object_form, name='change'),
    path('<uuid:object_id>/delete', views.object_form, name='delete'),
    path('login', views.dummylogin, name='dummylogin')
    #path('<uuid:reservation_id>/', views.info_reservation, name='modification'),
    #path('<uuid:reservation_id>/change', views.form_reservation, name='modification'),
    #path('<uuid:reservation_id>/delete', views.delete_reservation, name='delete'),
    #path('<uuid:reservation_id>/info', views.info_reservation, name='informations'),
    #path('<reservation_id>/pres', views.presentation, name='presentation')
]
