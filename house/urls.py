from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import PostList, PostDetail, PostCreate, PostUpdate, CommentView, UserResponseList, comments_accept, comments_delete


urlpatterns = [
    path('', PostList.as_view(), name="housePage"),
    path('<int:pk>/detail/', PostDetail.as_view(), name="postDetail"),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/like/', CommentView.as_view(), name="comment"),
    path('comment/', UserResponseList.as_view(), name='response'),
    path('comment/<int:pk>/delete/', comments_delete, name='comment_delete'),
    path('comment/<int:pk>/accept/', comments_accept, name='comment_accept'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)