from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import HousePage, PostDetail, PostCreate, PostUpdate, CommentView, UserResponseDelete, UserResponseAccept, UserResponseList


urlpatterns = [
    path('', HousePage.as_view(), name="housepage"),
    path('<int:pk>/detail/', PostDetail.as_view(), name="postdetail"),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/like/', CommentView.as_view(), name="comment"),
    path('response/', UserResponseList.as_view(), name='response'),
    path('response/<int:pk>/delete/', UserResponseDelete.as_view(), name='response_delete'),
    path('response/<int:pk>/accept/', UserResponseAccept.as_view(), name='response_accept'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)