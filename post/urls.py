from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostView.as_view(), name="post_view"),
    path("<int:post_id>", views.PostView.as_view(), name="post_id_view"),
    path("<str:case>", views.PostView.as_view(), name="post_id_view"),
    path("<int:post_id>", views.RecoverPostView.as_view(), name="post_recover_view"),
    path("<int:post_id>", views.LikeView.as_view(), name="like_view"),
]
