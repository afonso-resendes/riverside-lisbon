from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "meetingRoomPersonalizada",
        views.meetingRoomPersonalizada,
        name="meetingRoomPersonalizada",
    ),
    path(
        "coworkingSimulation",
        views.coworkingSimulation,
        name="coworkingSimulation",
    ),
    path("user_wallet", views.wallet, name="wallet"),
    path("Gallery", views.gallery, name="gallery"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("activate/<uidb64>/<token>", views.activate, name="activate"),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'), name="reset_password"),


    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_sent.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_done.html'),
         name="password_reset_complete"),

]
