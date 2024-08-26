from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', views.upload_doc,name='upload_doc'),
    # path('process/', views.process, name='process'),
    path('process_doc/<int:doc_id>/', views.process_doc, name='start_process'),
    path('view-document/<int:document_id>/', views.view_document, name='view_document'),
    path('delete-document/<int:document_id>/', views.delete_document, name='delete_document'),
    path('login/',views.CustomLogin.as_view(),name='Login'),
    path('logout/',LogoutView.as_view(next_page='Login'),name='Logout'),
    path('register/',views.Register.as_view(),name='Register'),

]