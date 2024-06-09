# results/urls.py
from django.urls import path
from .views import home_page, cbse_parser, icse_parser

urlpatterns = [path("", home_page, name="home"),
               path("cbse", cbse_parser, name="cbse_parser"),
               path("icse", icse_parser, name="icse_parser"),
               ]
