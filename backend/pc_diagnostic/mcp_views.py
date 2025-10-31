"""
AutoGen MCP Task Execution Views

API endpoints for executing MCP tasks using AutoGen orchestrator
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import logging
import os
import sys

# Add autogen_integration to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from autogen_integration.orchestrator import AutoGenOrchestrator

logger = logging.getLogger(__name__)

# Initialize orchestrator (singleton)
orchestrator = None

def get_orchestrator():
    """Get or create the AutoGen orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        try:
            orchestrator = AutoGenOrchestrator()
            logger.info("AutoGen orchestrator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AutoGen orchestrator: {str(e)}")
            orchestrator = None
    return orchestrator


@api_view(['POST'])
def execute_mcp_tasks(request):
    """
    Execute MCP tasks from model output
    
    Request Body:
        {
            "model_output": "Full AI model response including <MCP_TASKS>",
            "use_autogen": false,  // Optional: Use AutoGen agents vs direct execution
            "execution_mode": "direct"  // Optional: "direct" or "autogen"
        }
    
    Response:
        {
            "success": true,
            "tasks_requested": 5,
            "tasks_completed": 5,
            "tasks_failed": 0,
            "summary": "Task summary",
            "results": [...],
            "user_message": "User-friendly diagnostic message",
            "execution_summary": "Human-readable summary",
            "execution_timestamp": "ISO-8601 timestamp"
        }
    """
    try:
        # Get orchestrator
        orch = get_orchestrator()
        if not orch:
            return Response({
                'success': False,
                'error': 'AutoGen orchestrator not available',
                'details': 'Failed to initialize the task execution system'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        # Extract request data
        model_output = request.data.get('model_output', '')
        use_autogen = request.data.get('use_autogen', False)
        execution_mode = request.data.get('execution_mode', 'direct')
        
        # Override use_autogen based on execution_mode
        if execution_mode == 'autogen':
            use_autogen = True
        
        if not model_output:
            return Response({
                'success': False,
                'error': 'No model_output provided',
                'details': 'Please provide the AI model output containing MCP_TASKS'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info(f"Executing MCP tasks (mode: {execution_mode})")
        
        # Execute tasks
        result = orch.execute_mcp_tasks(model_output, use_autogen=use_autogen)
        
        # Add execution summary
        if result.get('success') and result.get('results'):
            result['execution_summary'] = orch.get_execution_summary(result['results'])
        
        # Determine HTTP status
        if result.get('success'):
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    except Exception as e:
        logger.error(f"Error in execute_mcp_tasks endpoint: {str(e)}")
        return Response({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def parse_mcp_tasks(request):
    """
    Parse MCP tasks from model output without executing them
    
    Request Body:
        {
            "model_output": "Full AI model response including <MCP_TASKS>"
        }
    
    Response:
        {
            "success": true,
            "tasks": [...],
            "summary": "Task summary",
            "task_count": 5,
            "categorized_tasks": {...},
            "user_message": "User-friendly message"
        }
    """
    try:
        from autogen_integration.parsers.mcp_parser import MCPTaskParser
        
        model_output = request.data.get('model_output', '')
        
        if not model_output:
            return Response({
                'success': False,
                'error': 'No model_output provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        parser = MCPTaskParser()
        
        # Extract MCP tasks
        mcp_data = parser.extract_mcp_tasks(model_output)
        
        if not mcp_data:
            return Response({
                'success': False,
                'error': 'No MCP_TASKS found in model output',
                'user_message': parser.get_user_friendly_message(model_output)
            }, status=status.HTTP_200_OK)
        
        tasks = mcp_data.get('tasks', [])
        summary = mcp_data.get('summary', '')
        
        # Categorize tasks
        categorized = parser.categorize_tasks(tasks)
        
        return Response({
            'success': True,
            'tasks': tasks,
            'summary': summary,
            'task_count': len(tasks),
            'categorized_tasks': categorized,
            'user_message': parser.get_user_friendly_message(model_output)
        })
    
    except Exception as e:
        logger.error(f"Error in parse_mcp_tasks endpoint: {str(e)}")
        return Response({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_orchestrator_status(request):
    """
    Get AutoGen orchestrator status and configuration
    
    Response:
        {
            "success": true,
            "orchestrator_available": true,
            "config": {...},
            "available_tools": [...]
        }
    """
    try:
        orch = get_orchestrator()
        
        if not orch:
            return Response({
                'success': True,
                'orchestrator_available': False,
                'message': 'Orchestrator not initialized'
            })
        
        # Get available tools
        available_tools = [
            "analyze_cpu_thermal",
            "inspect_disk_usage",
            "check_power_settings",
            "check_memory_usage",
            "verify_event_logs",
            "scan_system_files",
            "check_dism_health"
        ]
        
        return Response({
            'success': True,
            'orchestrator_available': True,
            'execution_modes': ['direct', 'autogen'],
            'recommended_mode': 'direct',
            'available_tools': available_tools,
            'config': {
                'execution_mode': orch.config.get('execution_mode'),
                'agents_configured': list(orch.config.get('agents', {}).keys())
            }
        })
    
    except Exception as e:
        logger.error(f"Error in get_orchestrator_status endpoint: {str(e)}")
        return Response({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
