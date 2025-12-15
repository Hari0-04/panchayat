from django.urls import path
from . import views

urlpatterns = [
    # START / WELCOME PAGES
    path("", views.Startpage, name="Startpage"),
    path("welcome/", views.welcome, name="welcome"),
    path("welcome2/", views.welcome2, name="welcome2"),
    path("welcome3/", views.welcome3, name="welcome3"),
    path("welcome4/", views.welcome4, name="welcome4"),

    # LOGIN PAGES
    path("login/", views.loginpage, name="loginpage"),              # Public login
    path("login2/", views.loginpage2, name="loginpage2"),           # Admin login
    path("login3/", views.loginpage3, name="supervisor_login"),     # Supervisor login
    path("login4/", views.loginpage4, name="EOlogin"),                  # EO login

    # LOGOUT PAGES
    path("logout/", views.logout, name="logout"),
    path("logoutadmin/", views.logout2, name="logout2"),
    path("logoutsupervisor/", views.logout3, name="logout3"),
    path("logouteo/", views.logout4, name="logout4"),

    # SIGNUP / PUBLIC USERS
    path("signup/", views.signup_pub, name="signup"),
    path("public-signups/", views.public_signups, name="public_signups"),
    path("admpubsignup/", views.Admpubsignup, name="admpubsignup"),

    # COMPLAINTS / REQUESTS
    path("complaint/", views.complaint_form, name="complaint_form"),
    path("requestform/", views.requestform, name="requestform"),
    path("complaints/", views.view_complaints, name="view_complaints"),
    path("complaintssupervisor/", views.complaints_supervisor, name="complaints_supervisor"),
    path("requests/", views.requests_supervisor, name="requests_supervisor"),

    # EO MODULE
    path("eo_dashboard/", views.eo_dashboard, name="eo_dashboard"),
    path("eomain/", views.eo_dashboard, name="eo_mainpage"),
    path("eo/complaints/", views.eo_complaints, name="eo_complaints"),
    path("eo/requests/", views.eo_requests, name="eo_requests"),

    # ADMIN MODULE
    path("mainadmin/", views.Mainpageadmin, name="Mainpageadmin"),
    path("Addsupervisor/", views.Add_supervisor, name="Add_supervisor"),
    # urls.py
    path('admin/add-area/', views.add_area, name='add_area'),

    path("tasks/", views.Tasks, name="tasks"),
    path("upload_profile/", views.upload_profile, name="upload_profile"),
    # path("create_user/", views.create_user, name="create_user"),

    # POSTS / NOTIFICATIONS
    path("posts/", views.Posts, name="Posts"),
    path("notifications/", views.notification_page, name="notification_page"),
    path("notifications/delete/<int:post_id>/", views.delete_post, name='delete_post'),

    # SUPERVISOR MAIN PAGE
    path("Mainsupervisor/", views.Mainsupervisor, name="Mainsupervisor"),
    # EXTRA / GENERAL
    path("main/", views.Mainpage, name='mainpage'),
    path("logoutsupervisor/", views.logout3, name="logout3"),
    path('notifications/', views.notification_page, name='notification_page'),
    path("notifications/delete/<int:post_id>/", views.delete_post, name="delete_post"),
    path("forgotpassword/", views.Forgotpassword, name="Forgotpassword"),
    path("delete_user/<str:role>/<str:user_id>/", views.delete_user, name="delete_user"),
    path("signup-list/", views.signup_list, name="signup_list"),
    path("", views.dashboard_stats, name="dashboard"),
    path("requestform/", views.requestform, name="requestform"),
    path("admin/mainpage/", views.Mainpageadmin, name="mainpageadmin"),
    # Supervisor dashboard / My Tasks page
    






]
