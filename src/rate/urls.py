from django.urls import path

from rate import views

app_name = 'rate'

urlpatterns = [
    path('list/', views.RateList.as_view(), name='list'),
    path('download-csv/', views.RateDownloadCSV.as_view(), name='download-csv'),
    path('download-xlsx/', views.RateDownloadXLSX.as_view(), name='download-xlsx'),
    path('latest-rates/', views.LatestRatesView.as_view(), name='latest-rates'),
    path('edit/<int:pk>', views.EditRate.as_view(), name='edit'),
    path('delete/<int:pk>', views.DeleteRate.as_view(), name='delete'),
]
