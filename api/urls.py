from django.urls import path
from . import views
urlpatterns = [
    path("<int:id>",views.post_details,name='post_details'),
    path("comments/<int:id>" , views.CommentsApi,name='comments'),
    path("u/<int:id>" , views.UserApi, name="user_info"),
    path('feed',views.feed,name='user_feed'),
    path("u/p/<str:id>",views.prpo, name="user's posts"),
    path("saves/",views.saved, name="savedPost"),
    path("share",views.share_view),
    path("inbox",views.inboxApi)
]
