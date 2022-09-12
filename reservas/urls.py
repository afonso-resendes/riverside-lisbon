from django.urls import path
from . import views, views_pt
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("status/<str:price>/<str:payment_Method>/<str:payment_status>/<str:transactionID>/", views.index, name="index"),
    path("<str:transactionID>/cancelation", views.cancelation, name="cancelation"),
    path("<str:transactionID>/refund", views.refund, name="refund"),
    path("meetingRoomPersonalizada",views.meetingRoomPersonalizada,name="meetingRoomPersonalizada",),
    path("meetingRoomPersonalizada/form/<str:spgContext>/<str:transactionID>/<str:transactionSignature>/<str:bundleType>",views.meetingRoomPersonalizada,name="meetingRoomPersonalizada"),
    path("coworkingSimulation",views.coworkingSimulation,name="coworkingSimulation"),
    path("coworkingSimulation/form/<str:spgContext>/<str:transactionID>/<str:transactionSignature>",views.coworkingSimulation,name="coworkingSimulation"),
    path("ctanks", views.coworkingTanks, name="coworkingTanks"),
    path("user_wallet", views.wallet, name="wallet"),
    path("gallery", views.gallery, name="gallery"),
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
        
    #--------------------PT-----------------------------


    path("pt", views_pt.index, name="index_pt"),
    path(
        "pt/meetingRoomPersonalizada",
        views_pt.meetingRoomPersonalizada,
        name="meetingRoomPersonalizada_pt",
    ),
    path(
        "pt/coworkingSimulation",
        views_pt.coworkingSimulation,
        name="coworkingSimulation",
    ),
    path("pt/ctanks", views_pt.coworkingTanks, name="coworkingTanks"),
    path("pt/m5tanks", views_pt.m5Thanks, name="m5Thanks"),
    path("pt/m10tanks", views_pt.m10Thanks, name="m10Thanks"),
    path("pt/user_wallet", views_pt.wallet, name="wallet_pt"),
    path("pt/gallery", views_pt.gallery, name="gallery"),
    path("pt/signup", views_pt.signup, name="signup_pt"),
    path("pt/signin", views_pt.signin, name="signin_pt"),

    path('pt/eset_password/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html'), name="reset_password"),


    path('pt/reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_sent.html'),
         name="password_reset_done"),

    path('pt/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'),
         name="password_reset_confirm"),

    path('pt/reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_done.html'),
         name="password_reset_complete"),

]
