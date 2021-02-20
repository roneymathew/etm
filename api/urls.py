from django.conf.urls import url
from django.urls import path,include

from rest_framework import routers

from . import views

from rest_framework_simplejwt.views import TokenRefreshView


router = routers.DefaultRouter(trailing_slash=True)

urlpatterns = [
	url('', include(router.urls)),
    url('create_admin/',views.create_admin),
    url('create_empl/',views.create_empl),
    url('create_manager/',views.create_manager),
    url('create_task/',views.create_task),
    url('edit_task/',views.EditTask),
    url('delete_task/',views.DeleteTask),
    url('task_list/',views.TaskList),
    url('user_list/',views.UserList),
    url('notification_list/',views.NotificationList),
    url('create_review/',views.create_review),
    url('edit_review/',views.EditReview),
    url('delete_review/',views.DeleteReview),
    url('review_list/',views.ReviewList),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]