from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("adminlogin/", views.admin_login, name="admin_login"),
    path("instructorlogin/", views.instructor_login, name="instructor_login"),
    path("adminregister", views.admin_register, name="admin_register"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("instructor/dashboard/<str:insId>", views.instructor_dashboard, name="instructor_dashboard"),
    path("addprogram/",views.add_program, name="addprogram"),
    path("addinstructor/", views.add_instructor, name="add_instructor"),
    path("admin/program/", views.dashboard_program, name="dashboard_program"),
    path("admin/instructor/", views.dashboard_instructor, name="dashboard_instructor"),
    path("admin/register/", views.dashboard_register, name="dashboard_register"),
    path("deleteprogram/<int:id>/",views.delete_program, name="delete_program"),
    path("deleteinstructor/<str:insId>/",views.delete_instructor, name="delete_instructor"),
    path("deleteregistration/<int:id>/",views.delete_register, name="delete_register"),
    path("deletefeedback/<int:id>/",views.delete_feedback, name="delete_feedback"),
    path("instructor/edit/<str:insId>", views.edit_instructor, name="edit_instructor"),
    path("program/edit/<int:id>", views.edit_program, name="edit_program"),
    path("registration/edit/<int:id>", views.edit_register, name="edit_register"),
    path("program/", views.program_list, name="program_list"),
    path("program/info/<int:id>", views.more_info, name="more_info"),
    path("register/<int:id>", views.register_program, name="register_program"),
    path("feedback/", views.feedback, name="feedback"),
    path("feedback/list", views.dashboard_feedback, name="dashboard_feedback")
]
