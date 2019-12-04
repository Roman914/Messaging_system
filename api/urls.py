from django.urls import path
from .views import MessagesView, SingleMessageView


urlpatterns = [
    path('messages/', MessagesView.as_view(), name="messages"),
    path('messages/<pk>', SingleMessageView.as_view(), name="single-message")

]
