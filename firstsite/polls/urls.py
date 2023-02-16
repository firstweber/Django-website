from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('offical/', views.officaltutor, name='tutor'),
    path('error/', views.test_error, name='error'),
    # path('<int:question_id>/', views.detail, name= 'detail'),  # <int:> only accept type:int. ex: /polls/5/
    # path('specifics/<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),  # ex: /polls/5/results/
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),  # ex: /polls/5/vote/    
]
