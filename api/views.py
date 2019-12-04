from rest_framework import generics, mixins
from .models import Message
from django.db.models import Q
from .permissions import IsMessageOwner
from .serializers import MessageSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class MessagesView(generics.ListAPIView, mixins.CreateModelMixin):
    serializer_class = MessageSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('isRead',)

    # returns messages that sent and received by the authorized user.
    def get_queryset(self):
        return Message.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)).order_by('-pk')

    def perform_create(self, serializer):
        serializer.save(isRead=False)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SingleMessageView(generics.RetrieveDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'pk'
    permission_classes = (IsMessageOwner,)

    # updating "isRead" when the receiver read a single message
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.receiver == self.request.user:
            instance.isRead = True
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
