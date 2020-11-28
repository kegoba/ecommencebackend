from django.urls import path
from . import views



urlpatterns =[
    path("", views.Home, name="Home"),
    path("getproduct/", views.GetProduct, name="save_product"),
    path("men/", views.GetMenCategory, name="Mencategory"),
    path("women/", views.GetWomenCategory, name="Mencategory"),
    path("login/", views.Login_user, name="Login_user"),
    path("register/", views.Register_user, name="Register_user"),
    path("updateuser/<int:id>/", views.Update_user, name="Update_user"),
    path("vturecord/<int:id>/", views.Vtu_record, name="Vtu_record"),
    path("order/<int:id>/", views.Orders, name="Orders"),
    path("saveproduct/", views.Post_product.as_view() , name="save_product"),
    path("payment/", views.Payment , name="payment")
    #Update_user 
]
