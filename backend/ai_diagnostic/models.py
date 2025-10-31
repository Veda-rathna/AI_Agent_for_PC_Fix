from django.db import models
from django.utils import timezone
import uuid


class Conversation(models.Model):
    """Model to store conversation sessions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500, blank=True)  # Auto-generated from first message
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at']),
            models.Index(fields=['is_archived']),
        ]
    
    def __str__(self):
        return f"{self.title[:50]} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Message(models.Model):
    """Model to store individual messages in a conversation"""
    MESSAGE_TYPE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    
    # AI-specific metadata
    model_name = models.CharField(max_length=200, blank=True, null=True)
    finish_reason = models.CharField(max_length=100, blank=True, null=True)
    tokens_used = models.IntegerField(blank=True, null=True)
    
    # Store session ID for telemetry linking
    session_id = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['conversation', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}"


class ConversationMetadata(models.Model):
    """Store additional metadata about conversations"""
    conversation = models.OneToOneField(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='metadata'
    )
    total_messages = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)
    issue_category = models.CharField(max_length=100, blank=True, null=True)
    resolution_status = models.CharField(
        max_length=50, 
        choices=[
            ('unresolved', 'Unresolved'),
            ('resolved', 'Resolved'),
            ('in_progress', 'In Progress'),
        ],
        default='unresolved'
    )
    
    def __str__(self):
        return f"Metadata for {self.conversation.title}"
