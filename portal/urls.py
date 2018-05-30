from portal.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from portal import views as views

app_name = 'portal'

urlpatterns = [
	url(r'^like$',views.Like.as_view(),name='like'),
	url(r'^login/$',views.Login.as_view(),name='login'),
	url(r'^logout$',views.Logout.as_view(),name='logout'),
	url(r'^comment$',views.AddComment.as_view(),name='comment'),
	url(r'^adduser$',views.AddUser.as_view(),name='adduser'),
	url(r'^success$',views.Success.as_view(),name='success'),
	url(r'^login/login$',views.Login.as_view(),name='login'),
	url(r'^delete$',views.DeleteFile.as_view(),name='delete'),
	url(r'^validate/$',views.Validate.as_view(),name='validate'),
	url(r'^resolve$',views.MarkResolved.as_view(),name='resolve'),
	url(r'^dashboard/$',views.Dashboard.as_view(),name='dashboard'),
	url(r'^uploadpolicy/$',views.UploadPolicy.as_view(),name='uploadpolicy'),
	url(r'^userdocument/$',views.UserDocument.as_view(),name='userdocument'),
	url(r'^addanswer$',views.AddAnswer.as_view(),name='addanswer'),
	url(r'^dashboard/(?P<tab>.+)/$',views.Dashboard.as_view(),name='dashboard'),
	url(r'^download/(?P<pid>.+)/$',views.DownloadPolicy.as_view(),name='download'),
	url(r'^addquestion/(?P<tab>.+)/$',views.AddQuestion.as_view(),name='addquestion'),
	url(r'^downloaduserdoc/(?P<uid>.+)/$',views.DownloadUserDocument.as_view(),name='downloaduserdoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
