from rest_framework import serializers
from .models import Conversation, Message, ConversationMetadata


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id', 'message_type', 'content', 'timestamp',
            'model_name', 'finish_reason', 'tokens_used', 'session_id'
        ]
        read_only_fields = ['id', 'timestamp']


class ConversationMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationMetadata
        fields = [
            'total_messages', 'total_tokens', 'issue_category', 'resolution_status'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    metadata = ConversationMetadataSerializer(read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'title', 'created_at', 'updated_at', 
            'is_archived', 'messages', 'metadata', 'message_count'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        return obj.messages.count()


class ConversationListSerializer(serializers.ModelSerializer):
    """Lighter serializer for listing conversations without full message history"""
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    metadata = ConversationMetadataSerializer(read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'title', 'created_at', 'updated_at', 
            'is_archived', 'message_count', 'last_message', 'metadata'
        ]
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return {
                'content': last_msg.content[:100] + '...' if len(last_msg.content) > 100 else last_msg.content,
                'type': last_msg.message_type,
                'timestamp': last_msg.timestamp
            }
        return None
