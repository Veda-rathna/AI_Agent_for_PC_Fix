from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, ConversationMetadata
from .serializers import (
    ConversationSerializer, 
    ConversationListSerializer,
    MessageSerializer
)
import re


def generate_conversation_title(first_message_content):
    """Generate a conversation title from the first user message"""
    # Take first 50 characters and clean it up
    title = first_message_content.strip()[:50]
    
    # Remove extra whitespace
    title = re.sub(r'\s+', ' ', title)
    
    # Add ellipsis if truncated
    if len(first_message_content) > 50:
        title += '...'
    
    return title


@api_view(['GET'])
def list_conversations(request):
    """
    List all conversations with pagination
    
    Query Parameters:
        - archived: Filter by archived status (true/false)
        - limit: Number of results (default 50)
        - offset: Pagination offset (default 0)
    """
    try:
        # Get query parameters
        is_archived = request.GET.get('archived', 'false').lower() == 'true'
        limit = int(request.GET.get('limit', 50))
        offset = int(request.GET.get('offset', 0))
        
        # Query conversations
        conversations = Conversation.objects.filter(is_archived=is_archived)
        total_count = conversations.count()
        
        # Apply pagination
        conversations = conversations[offset:offset + limit]
        
        # Serialize
        serializer = ConversationListSerializer(conversations, many=True)
        
        return Response({
            'success': True,
            'conversations': serializer.data,
            'total_count': total_count,
            'limit': limit,
            'offset': offset
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to list conversations: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_conversation(request, conversation_id):
    """
    Get a specific conversation with all messages
    """
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        serializer = ConversationSerializer(conversation)
        
        return Response({
            'success': True,
            'conversation': serializer.data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to get conversation: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_conversation(request):
    """
    Create a new conversation
    
    Request Body:
        {
            "title": "Optional custom title",
            "first_message": "Initial user message (optional)"
        }
    """
    try:
        title = request.data.get('title', '')
        first_message = request.data.get('first_message', '')
        
        # Create conversation
        conversation = Conversation.objects.create(
            title=title if title else 'New Conversation'
        )
        
        # Create metadata
        ConversationMetadata.objects.create(conversation=conversation)
        
        # Add first message if provided
        if first_message:
            Message.objects.create(
                conversation=conversation,
                message_type='user',
                content=first_message
            )
            
            # Update title based on first message if no custom title
            if not title:
                conversation.title = generate_conversation_title(first_message)
                conversation.save()
        
        serializer = ConversationSerializer(conversation)
        
        return Response({
            'success': True,
            'conversation': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to create conversation: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_message(request, conversation_id):
    """
    Add a message to an existing conversation
    
    Request Body:
        {
            "message_type": "user" | "assistant",
            "content": "Message content",
            "model_name": "Optional AI model name",
            "finish_reason": "Optional finish reason",
            "tokens_used": 0,
            "session_id": "Optional session ID"
        }
    """
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Extract message data
        message_type = request.data.get('message_type', 'user')
        content = request.data.get('content', '')
        
        if not content:
            return Response({
                'success': False,
                'error': 'Message content is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create message
        message = Message.objects.create(
            conversation=conversation,
            message_type=message_type,
            content=content,
            model_name=request.data.get('model_name'),
            finish_reason=request.data.get('finish_reason'),
            tokens_used=request.data.get('tokens_used'),
            session_id=request.data.get('session_id')
        )
        
        # Update conversation title if this is the first user message
        if conversation.messages.count() == 1 and message_type == 'user':
            if conversation.title == 'New Conversation':
                conversation.title = generate_conversation_title(content)
                conversation.save()
        
        # Update metadata
        metadata = conversation.metadata
        metadata.total_messages = conversation.messages.count()
        if message.tokens_used:
            metadata.total_tokens += message.tokens_used
        metadata.save()
        
        serializer = MessageSerializer(message)
        
        return Response({
            'success': True,
            'message': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to add message: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_conversation(request, conversation_id):
    """
    Update conversation metadata
    
    Request Body:
        {
            "title": "New title",
            "is_archived": true/false,
            "resolution_status": "resolved" | "unresolved" | "in_progress"
        }
    """
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        
        # Update fields
        if 'title' in request.data:
            conversation.title = request.data['title']
        
        if 'is_archived' in request.data:
            conversation.is_archived = request.data['is_archived']
        
        conversation.save()
        
        # Update metadata
        if 'resolution_status' in request.data:
            metadata = conversation.metadata
            metadata.resolution_status = request.data['resolution_status']
            metadata.save()
        
        serializer = ConversationSerializer(conversation)
        
        return Response({
            'success': True,
            'conversation': serializer.data
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to update conversation: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def delete_conversation(request, conversation_id):
    """
    Delete a conversation and all its messages
    """
    try:
        conversation = get_object_or_404(Conversation, id=conversation_id)
        conversation.delete()
        
        return Response({
            'success': True,
            'message': 'Conversation deleted successfully'
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to delete conversation: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def save_conversation_bulk(request):
    """
    Save an entire conversation in one request (useful for auto-save)
    
    Request Body:
        {
            "conversation_id": "uuid (optional, create new if not provided)",
            "title": "Conversation title",
            "messages": [
                {
                    "type": "user",
                    "content": "...",
                    "timestamp": "ISO datetime",
                    "model": "...",
                    "finishReason": "...",
                    "usage": {...}
                }
            ]
        }
    """
    try:
        conversation_id = request.data.get('conversation_id')
        title = request.data.get('title', 'New Conversation')
        messages_data = request.data.get('messages', [])
        
        if not messages_data:
            return Response({
                'success': False,
                'error': 'No messages provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create conversation
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                # Clear existing messages for fresh save
                conversation.messages.all().delete()
            except Conversation.DoesNotExist:
                conversation = Conversation.objects.create(title=title)
                ConversationMetadata.objects.create(conversation=conversation)
        else:
            conversation = Conversation.objects.create(title=title)
            ConversationMetadata.objects.create(conversation=conversation)
        
        # Create messages
        total_tokens = 0
        for msg_data in messages_data:
            tokens = 0
            if msg_data.get('usage'):
                tokens = msg_data['usage'].get('total_tokens', 0)
                total_tokens += tokens
            
            Message.objects.create(
                conversation=conversation,
                message_type=msg_data.get('type', 'user'),
                content=msg_data.get('content', ''),
                timestamp=msg_data.get('timestamp'),
                model_name=msg_data.get('model'),
                finish_reason=msg_data.get('finishReason'),
                tokens_used=tokens,
                session_id=msg_data.get('session_id')
            )
        
        # Update conversation title from first user message if default title
        if conversation.title == 'New Conversation':
            first_user_msg = next((m for m in messages_data if m.get('type') == 'user'), None)
            if first_user_msg:
                conversation.title = generate_conversation_title(first_user_msg.get('content', ''))
                conversation.save()
        
        # Update metadata
        metadata = conversation.metadata
        metadata.total_messages = len(messages_data)
        metadata.total_tokens = total_tokens
        metadata.save()
        
        serializer = ConversationSerializer(conversation)
        
        return Response({
            'success': True,
            'conversation': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to save conversation: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
