
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("addPost", views.addPost, name="addPost"),
    #path("emails/<int:email_id>", views.email, name="email"),
    path("posts", views.index, name="index"),
    path("user/<int:user_id>", views.userPosts, name="userPosts"),
    path("addFollower", views.addFollower, name="addFollower"),
    path("removeFollower", views.removeFollower, name="removeFollower"),
    path("following", views.following, name="following"),
    path("editPost/<int:post_id>", views.editPost, name="editPost"),
    path("user/editPost/<int:post_id>", views.editPost, name="editPost"),
    path("post/<int:post_id>", views.post, name="post"),
    #path("likePost/<int:post_id>", views.likePost, name="likePost"),
    path("updateLikes/<int:post_id>", views.updateLikes, name="updateLikes"),
    path("user/updateLikes/<int:post_id>", views.updateLikes, name="updateLikes"),
    path("user/post/<int:post_id>", views.post, name="post"),
    path("deletePost", views.deletePost, name="deletePost"),

]
