from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetView
from django.urls import include, path
from django.views.generic import TemplateView

from settings import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', TemplateView.as_view(template_name='index.html'), name='index'),

    path('account/', include('account.urls')),
    path('rate/', include('rate.urls')),

    ########
    path('password-reset/', PasswordResetView.as_view(
        template_name='registration/password-reset.html'), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
         template_name='registration/password-reset-done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password-reset-conf.html'), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='registration/password-reset-complete.html'), name='password_reset_complete'),
    path('password_change/<int:pk>/', views.ChangePassword.as_view(), name='password_change'),
    #######

    path('api/v1/rate/', include('rate.api.urls')),
    path('api/v1/user/', include('account.api.urls')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.handler404
handler500 = views.handler500
