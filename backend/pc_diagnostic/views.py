from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
from django.http import FileResponse, Http404
import random
import requests
import os
import uuid
import json

# Import hardware monitoring modules
from .hardware_monitor import HardwareMonitor
from .report_generator import ReportGenerator

# Initialize hardware monitor and report generator
hardware_monitor = HardwareMonitor()
report_generator = ReportGenerator()

# Local LLM API Configuration
LLM_API_BASE = "https://3ccc9499bbff.ngrok-free.app"
LLM_MODEL_ID = "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1"


def generate_mock_analysis(issue_description, telemetry_data):
    """Generate a mock diagnostic analysis when LLM server is unavailable"""
    
    # Analyze the telemetry data to provide a basic diagnosis
    analysis_sections = []
    
    # System Overview
    system_info = telemetry_data.get('system_info', {})
    analysis_sections.append(f"""
## System Analysis for: {issue_description}

**System Information:**
- Platform: {system_info.get('platform', 'Unknown')}
- Processor: {system_info.get('processor', 'Unknown')}
- Architecture: {system_info.get('machine', 'Unknown')}
- Python Version: {system_info.get('python_version', 'Unknown')}
""")

    # CPU Analysis
    cpu_data = telemetry_data.get('cpu', {})
    if cpu_data:
        cpu_usage = cpu_data.get('total_usage', 0)
        analysis_sections.append(f"""
**CPU Analysis:**
- Current Usage: {cpu_usage:.1f}%
- Status: {'⚠️ High Usage' if cpu_usage > 80 else '✅ Normal' if cpu_usage < 50 else '⚡ Moderate Usage'}
""")

    # Memory Analysis
    memory_data = telemetry_data.get('memory', {})
    if memory_data:
        memory_usage = memory_data.get('percentage', 0)
        memory_total = memory_data.get('total', 0)
        analysis_sections.append(f"""
**Memory Analysis:**
- Usage: {memory_usage:.1f}% ({memory_total // (1024**3):.1f} GB total)
- Status: {'⚠️ High Memory Usage' if memory_usage > 85 else '✅ Normal' if memory_usage < 70 else '⚡ Moderate Usage'}
""")

    # Basic Recommendations
    recommendations = []
    
    if 'screen' in issue_description.lower() or 'display' in issue_description.lower():
        recommendations.extend([
            "1. **Update Graphics Drivers**: Check Device Manager for display adapter updates",
            "2. **Check Cable Connections**: Ensure monitor cables are securely connected",
            "3. **Adjust Refresh Rate**: Try lowering the display refresh rate",
            "4. **Test Different Monitor**: Connect to another display to isolate the issue"
        ])
    elif 'slow' in issue_description.lower() or 'performance' in issue_description.lower():
        if cpu_usage > 80:
            recommendations.append("1. **High CPU Usage Detected**: Check Task Manager for resource-intensive processes")
        if memory_usage > 85:
            recommendations.append("2. **High Memory Usage**: Consider closing unnecessary applications or adding more RAM")
        recommendations.extend([
            "3. **Disk Cleanup**: Run disk cleanup and defragmentation",
            "4. **Startup Programs**: Disable unnecessary startup programs",
            "5. **Malware Scan**: Run a full system antivirus scan"
        ])
    else:
        recommendations.extend([
            "1. **System Update**: Ensure Windows is up to date",
            "2. **Driver Updates**: Check Device Manager for any driver issues",
            "3. **Event Viewer**: Check Windows Event Viewer for error messages",
            "4. **Safe Mode**: Test if the issue persists in Safe Mode"
        ])

    # Combine all sections
    mock_response = "\n".join(analysis_sections)
    
    if recommendations:
        mock_response += "\n\n## Recommended Solutions:\n\n"
        mock_response += "\n".join(recommendations)
    
    mock_response += f"""

## Next Steps:
1. **Try the recommended solutions** in order of priority
2. **Monitor system performance** using the collected telemetry data
3. **Contact support** if issues persist with the detailed diagnostic report

---
*Note: This analysis was generated using offline diagnostic capabilities. For more detailed AI-powered analysis, ensure the reasoning model server is available.*
"""
    
    return mock_response


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
    Handle prediction requests using the local reasoning model with telemetry data
    
    Request Body:
        {
            "input_text": "User's problem description",
            "telemetry_data": {...},  // Optional: system telemetry data
            "generate_report": true   // Optional: generate downloadable report
        }
    
    Response:
        {
            "success": true,
            "message": "The AI assistant's full response text",
            "model": "model-name",
            "finish_reason": "stop",
            "session_id": "uuid",
            "telemetry_collected": true,
            "telemetry_summary": {...},
            "reports": {...},  // If generate_report=true
            "usage": {...},
            "metadata": {...}
        }
    """
    try:
        # Extract input from the request
        input_text = request.data.get('input_text', '')
        provided_telemetry = request.data.get('telemetry_data', None)
        generate_report = request.data.get('generate_report', False)
        
        if not input_text:
            return Response(
                {
                    'success': False,
                    'error': 'No input provided. Please provide input_text in the request body.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate session ID for this diagnosis
        session_id = str(uuid.uuid4())
        
        # Collect system telemetry data based on the issue type
        print(f"Collecting telemetry data for issue: {input_text}")
        
        if provided_telemetry:
            telemetry_data = provided_telemetry
        else:
            telemetry_data = hardware_monitor.get_system_health(input_text)
        
        # Check telemetry data size and potentially summarize if too large
        telemetry_json = json.dumps(telemetry_data, indent=2, default=str)
        telemetry_size = len(telemetry_json)
        
        # If telemetry data is very large (>20KB), create a summary instead
        if telemetry_size > 20000:
            print(f"⚠️ Telemetry data is large ({telemetry_size} chars), creating summary...")
            telemetry_summary = {
                'timestamp': telemetry_data.get('timestamp'),
                'system_info': telemetry_data.get('system_info'),
                'cpu': {
                    'total_usage': telemetry_data.get('cpu', {}).get('total_usage'),
                    'per_cpu_usage': 'omitted for brevity'
                },
                'memory': telemetry_data.get('memory'),
                'disk': 'omitted for brevity' if len(str(telemetry_data.get('disk', {}))) > 1000 else telemetry_data.get('disk'),
                'issue_specific': telemetry_data.get('issue_specific'),
                'note': 'Full telemetry data available in generated report'
            }
            telemetry_json = json.dumps(telemetry_summary, indent=2, default=str)
            print(f"✅ Summarized to {len(telemetry_json)} chars")
        
        # Prepare the enhanced prompt with telemetry data
        user_prompt = f"""
User Problem: {input_text}

System Telemetry Data:
{telemetry_json}

Please provide a comprehensive diagnosis and solution based on this real-time system data.
"""
        
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

---

IMPORTANT: You have access to real-time system telemetry data. Use this data to:
1. Identify the root cause of the issue based on the telemetry data
2. Provide specific diagnostic insights correlating symptoms with actual system metrics
3. Offer step-by-step solutions prioritized by likelihood of success
4. Recommend preventive measures to avoid future occurrences
5. Highlight any critical system health issues discovered in the telemetry data

Format your response with both the user-friendly conversation AND the MCP tasks block as shown above.
"""
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        # Call the local reasoning model API
        try:
            response = requests.post(
                f"{LLM_API_BASE}/v1/chat/completions",
                json={
                    "model": LLM_MODEL_ID,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 3000
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
                model_used = result.get('model', LLM_MODEL_ID)
                
                if not prediction:
                    return Response(
                        {
                            'success': False,
                            'error': 'No content in model response'
                        },
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                # Build response data
                response_data = {
                    'success': True,
                    'message': prediction,
                    'prediction': prediction,
                    'model': model_used,
                    'finish_reason': finish_reason,
                    'session_id': session_id,
                    'telemetry_collected': True,
                    'telemetry_summary': {
                        'timestamp': telemetry_data.get('timestamp'),
                        'system': telemetry_data.get('system_info', {}).get('platform'),
                        'cpu_usage': telemetry_data.get('cpu', {}).get('total_usage'),
                        'memory_usage': telemetry_data.get('memory', {}).get('percentage'),
                        'issue_specific_data': list(telemetry_data.get('issue_specific', {}).keys())
                    },
                    'usage': {
                        'prompt_tokens': usage.get('prompt_tokens', 0),
                        'completion_tokens': usage.get('completion_tokens', 0),
                        'total_tokens': usage.get('total_tokens', 0)
                    },
                    'metadata': {
                        'id': result.get('id', ''),
                        'created': result.get('created', ''),
                        'object': result.get('object', ''),
                        'system_fingerprint': result.get('system_fingerprint', '')
                    }
                }
                
                # Generate reports if requested
                if generate_report:
                    try:
                        # Generate JSON report
                        json_filename, json_filepath = report_generator.generate_json_report(
                            input_text, telemetry_data, prediction, session_id
                        )
                        
                        response_data['reports'] = {
                            'json': {
                                'filename': json_filename,
                                'download_url': f'/api/download_report/{json_filename}'
                            }
                        }
                        
                        print(f"Report generated: {json_filename}")
                        
                    except Exception as report_error:
                        print(f"Report generation error: {str(report_error)}")
                        response_data['report_error'] = f"Failed to generate reports: {str(report_error)}"
                
                return Response(response_data)
                
            else:
                return Response(
                    {
                        'success': False,
                        'error': 'No choices in model response'
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        except requests.exceptions.ConnectionError:
            print("LLM API Error: Connection failed. Using offline diagnostic mode.")
            
            # Use simplified fallback analysis
            prediction = generate_mock_analysis(input_text, telemetry_data)
            model_used = "Offline Diagnostic Engine"
            finish_reason = "offline_mode"
            usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            
            response_data = {
                'success': True,
                'prediction': prediction,
                'message': prediction,
                'model': model_used,
                'finish_reason': finish_reason,
                'session_id': session_id,
                'telemetry_collected': True,
                'telemetry_summary': {
                    'timestamp': telemetry_data.get('timestamp'),
                    'system': telemetry_data.get('system_info', {}).get('platform'),
                    'cpu_usage': telemetry_data.get('cpu', {}).get('total_usage'),
                    'memory_usage': telemetry_data.get('memory', {}).get('percentage'),
                    'issue_specific_data': list(telemetry_data.get('issue_specific', {}).keys())
                },
                'usage': usage,
                'metadata': {
                    'id': '',
                    'created': '',
                    'object': '',
                    'system_fingerprint': ''
                }
            }
            
            # Generate reports if requested
            if generate_report:
                try:
                    json_filename, json_filepath = report_generator.generate_json_report(
                        input_text, telemetry_data, prediction, session_id
                    )
                    
                    response_data['reports'] = {
                        'json': {
                            'filename': json_filename,
                            'download_url': f'/api/download_report/{json_filename}'
                        }
                    }
                except Exception as report_error:
                    print(f"Report generation error: {str(report_error)}")
                    response_data['report_error'] = f"Failed to generate reports: {str(report_error)}"
            
            return Response(response_data)
    
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


@api_view(['GET'])
def download_report(request, filename):
    """Download generated diagnostic reports"""
    try:
        reports_folder = report_generator.reports_folder
        file_path = os.path.join(reports_folder, filename)
        
        # Security check: ensure the file exists and is in the reports folder
        if not os.path.exists(file_path) or not os.path.abspath(file_path).startswith(os.path.abspath(reports_folder)):
            raise Http404("Report not found")
        
        # Return the file
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to download report: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def list_reports(request):
    """List available diagnostic reports"""
    try:
        available_reports = report_generator.get_available_reports()
        return Response({
            'success': True,
            'reports': available_reports,
            'total_reports': len(available_reports)
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to list reports: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_telemetry(request):
    """Get current system telemetry without AI analysis"""
    try:
        issue_description = request.GET.get('issue', 'general')
        telemetry_data = hardware_monitor.get_system_health(issue_description)
        
        return Response({
            'success': True,
            'telemetry_data': telemetry_data,
            'timestamp': telemetry_data.get('timestamp')
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to collect telemetry: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
