from django.urls import path, include
from . import  views




urlpatterns = [
    path('',views.index, name = 'main'),
    path('about',views.about),
    path('contacts',views.contact),
    path('add_review',views.add_review.as_view()),
    path('review/<int:pk>/',views.review_detailed.as_view(),name = 'review_detailed')

]