from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.home,name='home'),
    path("login/",views.signin,name='singin'),
    path("register/",views.signup,name='singup'),
    path("logout/",views.logout_view,name='logout'),
    path("profile/",views.profile,name="profile"),
    path("edit_profile/",views.edit_profile,name="edit_profile"),
    path('p/<int:id>/',views.post_view,name='post'),
    path("account/<str:name>",views.others,name="others_profile"),
    path("add/<int:id>",views.add_friend),
    path("save/",views.saveView),
    path("edit<int:p>/" ,views.edit_post),
    path("result" , views.search_result , name="search-result"),
    path("cancel/<int:id>",views.cancel_request),
    path("accept/<int:id>" , views.accept , name="accept-friend"),
]
