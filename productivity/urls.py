from django.urls import path
from . import views

app_name = "productivity"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("predict/", views.predict_form, name="predict"),
    path("api/predict/", views.api_predict, name="api_predict"),
    path("api/summary/", views.api_summary, name="api_summary"),
    path("api/employee/<str:employee_id>/", views.api_employee, name="api_employee"),
]
