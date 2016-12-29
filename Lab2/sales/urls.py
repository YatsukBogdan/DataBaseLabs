from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.sales_editor, name='sales_editor'),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^update$', views.update, name='update'),
    url(r'^insert$', views.insert, name='insert'),
    url(r'^salesfilter$', views.salesfilter, name='salesfilter'),
    url(r'^loadxml$', views.loadxml, name='loadxml')
]