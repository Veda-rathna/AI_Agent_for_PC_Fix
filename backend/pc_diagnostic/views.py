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
import platform
from datetime import datetime

# Import hardware monitoring modules
from .hardware_monitor import HardwareMonitor
from .report_generator import ReportGenerator
from .hardware_hash import HardwareHashProtection

# Import diagnostic tools for tool use
from .diagnostic_tools import (
    check_disk_health,
    scan_event_logs,
    verify_driver_integrity,
    check_gpu_status,
    test_memory,
    check_network_connectivity
)

# Initialize hardware monitor and report generator
hardware_monitor = HardwareMonitor()
report_generator = ReportGenerator()
hardware_hash_protection = HardwareHashProtection()

# Local LLM API Configuration
LLM_API_BASE = "https://3ccc9499bbff.ngrok-free.app"
LLM_MODEL_ID = "reasoning-llama-3.1-cot-re1-nmt-v2-orpo-i1"

# Diagnostic Tools Configuration for Tool Use
DIAGNOSTIC_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_disk_health",
            "description": "Run SMART diagnostics on all drives to check for disk errors, failures, or low disk space. Use this when user reports slow performance, file access issues, or disk-related problems.",
            "parameters": {
                "type": "object",
                "properties": {
                    "drive_letter": {
                        "type": "string",
                        "description": "Specific drive to check (e.g., 'C'). Leave empty to check all drives"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "scan_event_logs",
            "description": "Scan Windows Event Viewer for errors related to hardware, drivers, crashes, or system failures. Essential for diagnosing BSODs, driver issues, hardware failures, and system crashes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "log_type": {
                        "type": "string",
                        "enum": ["System", "Application", "Hardware Events"],
                        "description": "Type of event log to scan. System for hardware/driver errors, Application for software crashes"
                    },
                    "hours_back": {
                        "type": "number",
                        "description": "How many hours back to search (default: 24)"
                    },
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Specific keywords to search for (e.g., ['GPU', 'driver', 'crash', 'BSOD', 'display'])"
                    }
                },
                "required": ["log_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "verify_driver_integrity",
            "description": "Check if system drivers are properly signed, up-to-date, and functioning correctly. Use when diagnosing hardware malfunctions, display issues, network problems, or audio issues.",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_type": {
                        "type": "string",
                        "enum": ["display", "network", "audio", "storage", "all"],
                        "description": "Type of device drivers to verify. Choose based on the issue: display for screen problems, network for connectivity, audio for sound issues, storage for disk problems, all for comprehensive check"
                    }
                },
                "required": ["device_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_gpu_status",
            "description": "Check GPU status including drivers, functionality, and hardware detection. Use for screen issues, display problems, graphics errors, or gaming performance issues.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "test_memory",
            "description": "Check RAM usage, memory pressure, and swap usage. Use when diagnosing crashes, freezes, slow performance, or out-of-memory errors.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_network_connectivity",
            "description": "Test network connectivity, ping times, and network interface status. Use for internet connection issues, network slowness, or connectivity problems.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "IP address or hostname to ping (default: 8.8.8.8 - Google DNS)"
                    }
                },
                "required": []
            }
        }
    }
]


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
        
        # Prepare the prompt for the reasoning model with tool use support
        messages = [
            {
                "role": "system",
                "content": """
You are an AI PC Diagnostic Assistant with access to real diagnostic tools.

**Available Diagnostic Tools:**
You can call real system diagnostic functions to gather specific data:
- check_disk_health: Run SMART diagnostics on drives
- scan_event_logs: Search Windows Event Viewer for errors
- verify_driver_integrity: Check driver signatures and versions
- check_gpu_status: Verify GPU hardware and drivers
- test_memory: Check RAM usage and health
- check_network_connectivity: Test network connectivity

**Diagnostic Workflow:**
1. Analyze the user's problem and available telemetry data
2. Use diagnostic tools to gather additional specific information when needed
3. Provide a comprehensive diagnosis based on all collected data
4. Give clear, actionable solutions prioritized by likelihood of success

**IMPORTANT - Tool Usage Rules:**
- **Call ONLY ONE tool at a time** (model limitation)
- After receiving tool results, you can call another tool if needed
- Choose the most relevant tool for the user's specific problem
- Always explain what you're checking and why
- Use tool results to provide evidence-based recommendations

**Response Guidelines:**
- Be conversational and easy to understand
- Explain technical findings in user-friendly terms
- Provide step-by-step manual instructions for user actions
- Use tool results to support your diagnosis
- Prioritize solutions from most to least likely to work

**Important:**
- You have access to real-time system telemetry data
- Correlate symptoms with actual system metrics
- Highlight any critical system health issues
- Recommend preventive measures
"""
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
        
        # Call the local reasoning model API with tool use support
        # Support iterative tool calling (one tool at a time)
        try:
            print(f"🤖 Sending request to LLM with {len(DIAGNOSTIC_TOOLS)} available tools...")
            
            # Track all tools used across iterations
            all_tools_used = []
            max_iterations = 5  # Prevent infinite loops
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                print(f"🔄 Iteration {iteration}")
                
                response = requests.post(
                    f"{LLM_API_BASE}/v1/chat/completions",
                    json={
                        "model": LLM_MODEL_ID,
                        "messages": messages,
                        "tools": DIAGNOSTIC_TOOLS,  # Include diagnostic tools
                        "temperature": 0.7,
                        "max_tokens": 3000
                    }
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
                
                # Check if model requested tool calls
                if 'choices' in result and len(result['choices']) > 0:
                    choice = result['choices'][0]
                    finish_reason = choice.get('finish_reason', 'unknown')
                    
                    # Handle tool calls if requested
                    if finish_reason == 'tool_calls' and choice.get('message', {}).get('tool_calls'):
                        tool_calls = choice['message']['tool_calls']
                        print(f"🔧 Model requested {len(tool_calls)} tool call(s)")
                        
                        # Process only the first tool call (model limitation)
                        tool_call = tool_calls[0]
                        function_name = tool_call['function']['name']
                        arguments = json.loads(tool_call['function']['arguments'])
                        
                        print(f"  ▶ Executing: {function_name}({arguments})")
                        
                        # Execute the actual diagnostic function
                        try:
                            if function_name == 'check_disk_health':
                                result_data = check_disk_health(**arguments)
                            elif function_name == 'scan_event_logs':
                                result_data = scan_event_logs(**arguments)
                            elif function_name == 'verify_driver_integrity':
                                result_data = verify_driver_integrity(**arguments)
                            elif function_name == 'check_gpu_status':
                                result_data = check_gpu_status(**arguments)
                            elif function_name == 'test_memory':
                                result_data = test_memory(**arguments)
                            elif function_name == 'check_network_connectivity':
                                result_data = check_network_connectivity(**arguments)
                            else:
                                result_data = {
                                    'success': False,
                                    'error': f'Unknown tool: {function_name}'
                                }
                            
                            all_tools_used.append({
                                'name': function_name,
                                'arguments': arguments,
                                'result': result_data
                            })
                            
                            print(f"  ✅ {function_name} completed")
                            
                        except Exception as tool_error:
                            result_data = {
                                'success': False,
                                'error': f'Tool execution failed: {str(tool_error)}'
                            }
                            all_tools_used.append({
                                'name': function_name,
                                'arguments': arguments,
                                'result': result_data
                            })
                            print(f"  ❌ {function_name} failed: {str(tool_error)}")
                        
                        # Add tool call and result to conversation
                        messages.append({
                            "role": "assistant",
                            "tool_calls": [
                                {
                                    "id": tool_call['id'],
                                    "type": tool_call['type'],
                                    "function": {
                                        "name": tool_call['function']['name'],
                                        "arguments": tool_call['function']['arguments']
                                    }
                                }
                            ]
                        })
                        messages.append({
                            "role": "tool",
                            "content": json.dumps(result_data),
                            "tool_call_id": tool_call['id']
                        })
                        
                        # Continue to next iteration to see if model wants more tools
                        continue
                        
                    else:
                        # No tool calls - we have the final response
                        prediction = choice.get('message', {}).get('content', '')
                        
                        if not prediction:
                            return Response(
                                {
                                    'success': False,
                                    'error': 'No content in model response'
                                },
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
                        
                        # Get usage information
                        usage = result.get('usage', {})
                        model_used = result.get('model', LLM_MODEL_ID)
                        
                        # Build response data
                        response_data = {
                            'success': True,
                            'message': prediction,
                            'prediction': prediction,
                            'model': model_used,
                            'finish_reason': 'tool_calls_completed' if all_tools_used else finish_reason,
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
                        
                        # Add tool information if tools were used
                        if all_tools_used:
                            response_data['tools_used'] = [tool['name'] for tool in all_tools_used]
                            response_data['tool_results'] = all_tools_used
                            response_data['iterations'] = iteration
                        
                        # Generate reports if requested
                        if generate_report:
                            try:
                                # Include tool results in the report
                                enhanced_telemetry = telemetry_data.copy()
                                if all_tools_used:
                                    enhanced_telemetry['diagnostic_tools_executed'] = all_tools_used
                                
                                # Generate JSON report
                                json_filename, json_filepath = report_generator.generate_json_report(
                                    input_text, enhanced_telemetry, prediction, session_id
                                )
                                
                                response_data['reports'] = {
                                    'json': {
                                        'filename': json_filename,
                                        'download_url': f'/api/download_report/{json_filename}'
                                    }
                                }
                                
                                print(f"📄 Report generated: {json_filename}")
                                
                            except Exception as report_error:
                                print(f"❌ Report generation error: {str(report_error)}")
                                response_data['report_error'] = f"Failed to generate reports: {str(report_error)}"
                        
                        return Response(response_data)
                
            # Max iterations reached without final response
            # Max iterations reached without final response
            return Response({
                'success': False,
                'error': 'Max tool calling iterations reached'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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


@api_view(['POST'])
def generate_hardware_hash(request):
    """
    Generate encrypted hardware hash file
    
    Request Body:
        {
            "password": "optional_custom_password"
        }
    
    Response:
        {
            "success": true,
            "file_path": "path/to/file",
            "hardware_hash": "hash_string",
            "download_url": "/api/download_hardware_hash/filename"
        }
    """
    try:
        password = request.data.get('password', 'default_password')
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        hostname = platform.node()
        filename = f"hardware_hash_{hostname}_{timestamp}.hwh"
        
        # Ensure hardware_hash directory exists
        hash_dir = os.path.join(settings.MEDIA_ROOT, 'hardware_hashes')
        os.makedirs(hash_dir, exist_ok=True)
        
        output_path = os.path.join(hash_dir, filename)
        
        # Generate hardware hash file
        result = hardware_hash_protection.create_hardware_hash_file(output_path, password)
        
        if result.get('success'):
            return Response({
                'success': True,
                'filename': filename,
                'file_path': output_path,
                'file_size': result.get('file_size'),
                'hardware_hash': result.get('hardware_hash'),
                'created': result.get('created'),
                'components_captured': result.get('components_captured'),
                'download_url': f'/api/download_hardware_hash/{filename}'
            })
        else:
            return Response({
                'success': False,
                'error': result.get('error', 'Unknown error occurred')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to generate hardware hash: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def analyze_hardware_hash(request):
    """
    Analyze uploaded hardware hash file and compare with current hardware
    
    Request:
        - file: Hardware hash file (.hwh)
        - password: Password for decryption (optional)
    
    Response:
        {
            "success": true,
            "comparison": {
                "overall_status": "changed|unchanged",
                "changes_detected": [...],
                "changeable_components_changes": [...]
            }
        }
    """
    try:
        if 'file' not in request.FILES:
            return Response({
                'success': False,
                'error': 'No file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        password = request.data.get('password', 'default_password')
        
        # Save uploaded file temporarily
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'temp_uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        temp_file_path = os.path.join(upload_dir, file.name)
        with open(temp_file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Analyze the file
        analysis_result = hardware_hash_protection.analyze_hardware_hash_file(temp_file_path, password)
        
        # Clean up temporary file
        try:
            os.remove(temp_file_path)
        except:
            pass
        
        if analysis_result.get('success'):
            return Response({
                'success': True,
                'comparison': analysis_result.get('comparison'),
                'file_info': analysis_result.get('comparison', {}).get('file_info'),
                'summary': analysis_result.get('comparison', {}).get('summary')
            })
        else:
            return Response({
                'success': False,
                'error': analysis_result.get('error', 'Analysis failed')
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to analyze hardware hash: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def download_hardware_hash(request, filename):
    """Download generated hardware hash file"""
    try:
        hash_dir = os.path.join(settings.MEDIA_ROOT, 'hardware_hashes')
        file_path = os.path.join(hash_dir, filename)
        
        # Security check
        if not os.path.exists(file_path) or not os.path.abspath(file_path).startswith(os.path.abspath(hash_dir)):
            raise Http404("Hardware hash file not found")
        
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': f'Failed to download file: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

