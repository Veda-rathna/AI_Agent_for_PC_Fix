from django.contrib import admin
from .models import Conversation, Message, ConversationMetadata


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['id', 'timestamp']
    fields = ['message_type', 'content', 'timestamp', 'model_name', 'tokens_used']


class ConversationMetadataInline(admin.StackedInline):
    model = ConversationMetadata
    extra = 0


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'is_archived', 'message_count']
    list_filter = ['is_archived', 'created_at']
    search_fields = ['title', 'id']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [ConversationMetadataInline, MessageInline]
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'message_type', 'content_preview', 'timestamp', 'model_name']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content', 'conversation__title']
    readonly_fields = ['id', 'timestamp']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


@admin.register(ConversationMetadata)
class ConversationMetadataAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'total_messages', 'total_tokens', 'resolution_status']
    list_filter = ['resolution_status', 'issue_category']
    search_fields = ['conversation__title']
