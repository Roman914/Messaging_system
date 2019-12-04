from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = [
            'pk',
            'sender',
            'receiver',
            'subject',
            'message',
            'isRead',
            'creationDate'
        ]
        read_only_fields = [
            'sender',
            'creationDate']

    def validate(self, attrs):
        attrs['sender'] = self.context['request'].user
        return attrs
