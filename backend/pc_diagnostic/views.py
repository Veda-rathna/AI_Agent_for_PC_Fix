from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
import random
import requests
import os


# Local LLM API Configuration
LLM_API_BASE = "https://3ccc9499bbff.ngrok-free.app"
LLM_MODEL_ID = "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1"


@api_view(['POST'])
def diagnose(request):
    """
    AI-driven PC diagnostic endpoint
    Accepts a query and returns a diagnostic message
    """
    query = request.data.get('query', '')
    
    if not query:
        return Response(
            {'error': 'Query is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Simulate AI diagnostic responses
    diagnostics = [
        f"Analyzing your issue: '{query}'. Based on my assessment, this could be related to system resources.",
        f"I've processed your query: '{query}'. Consider checking your disk space and memory usage.",
        f"Regarding '{query}': I recommend running a system scan and updating your drivers.",
        f"Your query '{query}' suggests a possible software conflict. Try restarting the affected application.",
        f"After analyzing '{query}', I suggest clearing your cache and temporary files.",
    ]
    
    response_message = random.choice(diagnostics)
    
    return Response({
        'query': query,
        'diagnosis': response_message,
        'timestamp': request.data.get('timestamp', None)
    })


@api_view(['POST'])
def predict(request):
    """
    Handle prediction requests using the local reasoning model
    
    Request Body:
        {
            "input_text": "User's problem description",
            "telemetry_data": {...}  // Optional: system telemetry data
        }
    
    Response:
        {
            "success": true,
            "message": "The AI assistant's full response text",
            "model": "model-name",
            "finish_reason": "stop",
            "usage": {...},
            "metadata": {...}
        }
    """
    try:
        # Extract input from the request
        input_text = request.data.get('input_text', '')
        telemetry_data = request.data.get('telemetry_data', None)
        
        if not input_text:
            return Response(
                {
                    'success': False,
                    'error': 'No input provided. Please provide input_text in the request body.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prepare the user message with optional telemetry data
        user_message = input_text
        if telemetry_data:
            user_message += f"\n\nSystem Telemetry Data:\n{telemetry_data}"
        
        # Prepare the prompt for the reasoning model
        messages = [
            {
                "role": "system",
                "content": """
You are an AI PC Diagnostic Assistant designed to troubleshoot and resolve computer hardware and software issues.

Your role involves two layers of response:
1. Human-level conversation (visible to user)
2. Machine Control Protocol (MCP) task generation (hidden JSON block)

---

1️⃣ **Visible User Conversation**
- Respond naturally in an easy-to-understand tone.
- Ask clarifying questions if needed.
- Provide step-by-step manual or visual instructions that the user can perform themselves.
- These are physical or user-level checks such as:
  - "Check if the power cable is properly connected."
  - "Try booting in Safe Mode."
  - "Inspect your display for any visible damage."
- Never mention any JSON or internal system processing to the user.

---

2️⃣ **Hidden MCP Task Generation**
After your user-facing explanation, you must append a JSON block enclosed between <MCP_TASKS> and </MCP_TASKS>.

Rules for MCP tasks:
- Include only tasks that the system or diagnostic agent can perform or verify programmatically.
- These are system-level, telemetry, or command-based actions.
- Do not include tasks that require physical inspection or human intervention.
- Generate as many relevant and required tasks as possible to ensure a complete diagnostic scope.
  - Do not limit yourself to just 3–4 tasks.
  - Cover all key checks that can be done by the computer for that issue.

Examples of valid MCP tasks:
- "Check GPU driver version and integrity"
- "Scan Windows Event Log for GPU or display errors"
- "Verify if monitor is detected through DDC/CI"
- "Test PCI device enumeration for GPU"
- "Check power supply voltage sensor readings"
- "Analyze temperature logs for thermal shutdown patterns"

Examples of invalid MCP tasks (must not appear):
- "Check if the monitor cable is plugged in"
- "Inspect screen for cracks"
- "Clean the RAM sticks manually"

---

3️⃣ **Response Format**
Write the natural user response first.
Then include the structured JSON block exactly like this:

<MCP_TASKS>
{
  "tasks": [
    "Comprehensive system-level diagnostic task 1",
    "Comprehensive system-level diagnostic task 2",
    "Comprehensive system-level diagnostic task 3"
  ],
  "summary": "Brief description of what the MCP should analyze or verify."
}
</MCP_TASKS>

---

✅ **Example Output**

User: "My screen isn't turning on."

AI Output:
Let's narrow this down.
Please check whether your monitor cable is properly plugged into both ends.
Press the Caps Lock key — if the indicator light toggles, your PC is on but the display may not be initializing.
Try connecting your monitor to a different port or system to confirm the display is working.
If it still doesn't show anything, I'll now check your system drivers and logs for possible GPU or display-related faults.

<MCP_TASKS>
{
  "tasks": [
    "Check GPU driver version and integrity",
    "Verify GPU hardware presence through PCI bus enumeration",
    "Check Windows Event Logs for display driver initialization failures",
    "Scan system for recent BSOD or display-related kernel events",
    "Validate DirectX diagnostic logs for rendering initialization errors",
    "Check if connected monitor is detected through DDC/CI handshake",
    "Inspect power delivery telemetry for GPU and display subsystems"
  ],
  "summary": "Perform deep analysis of GPU, display drivers, and event logs to detect potential display initialization failures."
}
</MCP_TASKS>
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        # Call the local reasoning model API
        response = requests.post(
            f"{LLM_API_BASE}/v1/chat/completions",
            json={
                "model": LLM_MODEL_ID,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000
            },
            timeout=120  # Reasoning models may take longer
        )
        
        # Check if the request was successful
        if response.status_code != 200:
            return Response(
                {
                    'success': False,
                    'error': f'Model API error: {response.status_code}',
                    'details': response.text
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Parse the response
        result = response.json()
        
        # Extract the model's response
        if 'choices' in result and len(result['choices']) > 0:
            choice = result['choices'][0]
            
            # Get the assistant's message content
            prediction = choice.get('message', {}).get('content', '')
            finish_reason = choice.get('finish_reason', 'unknown')
            
            # Get usage information
            usage = result.get('usage', {})
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', 0)
            
            # Get model info
            model_used = result.get('model', LLM_MODEL_ID)
            
            if not prediction:
                return Response(
                    {
                        'success': False,
                        'error': 'No content in model response'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            return Response({
                'success': True,
                'message': prediction,  # Main field for frontend to display
                'prediction': prediction,  # Kept for backward compatibility
                'model': model_used,
                'finish_reason': finish_reason,
                'usage': {
                    'prompt_tokens': prompt_tokens,
                    'completion_tokens': completion_tokens,
                    'total_tokens': total_tokens
                },
                'metadata': {
                    'id': result.get('id', ''),
                    'created': result.get('created', ''),
                    'object': result.get('object', ''),
                    'system_fingerprint': result.get('system_fingerprint', '')
                },
                'processing_time': result.get('created', 0)  # Timestamp for reference
            })
        else:
            return Response(
                {
                    'success': False,
                    'error': 'No choices in model response'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    except requests.exceptions.Timeout:
        return Response(
            {
                'success': False,
                'error': 'Request to model timed out. The reasoning model may be processing a complex query.'
            },
            status=status.HTTP_504_GATEWAY_TIMEOUT
        )
    except requests.exceptions.ConnectionError:
        return Response(
            {
                'success': False,
                'error': 'Could not connect to local model server',
                'details': f'Make sure the server is running at {LLM_API_BASE}'
            },
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        return Response(
            {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    """Handle file uploads"""
    try:
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        if not file.name:
            return Response(
                {'error': 'No file selected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ensure upload directory exists
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the file
        file_path = os.path.join(upload_dir, file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # TODO: Process the file with your model
        # Example: result = your_model.predict_from_file(file_path)
        
        return Response({
            'success': True,
            'message': f'File {file.name} uploaded successfully',
            'filename': file.name
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
