"""
MCP Task Parser

Extracts and validates <MCP_TASKS> from AI model output
"""

import json
import re
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MCPTaskParser:
    """Parser for extracting MCP tasks from model output"""
    
    @staticmethod
    def extract_mcp_tasks(model_output: str) -> Optional[Dict]:
        """
        Extract MCP_TASKS JSON from model output
        
        Args:
            model_output: The full text output from the AI model
            
        Returns:
            Dictionary containing tasks and summary, or None if not found
        """
        try:
            # Use regex to find content between <MCP_TASKS> tags
            pattern = r'<MCP_TASKS>\s*(.*?)\s*</MCP_TASKS>'
            match = re.search(pattern, model_output, re.DOTALL | re.IGNORECASE)
            
            if not match:
                logger.warning("No <MCP_TASKS> block found in model output")
                return None
            
            # Extract the JSON content
            json_str = match.group(1).strip()
            
            # Parse JSON
            mcp_data = json.loads(json_str)
            
            # Validate structure
            if not MCPTaskParser.validate_mcp_structure(mcp_data):
                logger.error("Invalid MCP task structure")
                return None
            
            logger.info(f"Successfully extracted {len(mcp_data.get('tasks', []))} MCP tasks")
            return mcp_data
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in MCP_TASKS: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error extracting MCP tasks: {str(e)}")
            return None
    
    @staticmethod
    def validate_mcp_structure(mcp_data: Dict) -> bool:
        """
        Validate that MCP data has required structure
        
        Args:
            mcp_data: Parsed MCP task dictionary
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(mcp_data, dict):
            logger.error("MCP data is not a dictionary")
            return False
        
        if 'tasks' not in mcp_data:
            logger.error("MCP data missing 'tasks' field")
            return False
        
        if not isinstance(mcp_data['tasks'], list):
            logger.error("MCP 'tasks' field is not a list")
            return False
        
        if len(mcp_data['tasks']) == 0:
            logger.warning("MCP tasks list is empty")
            return False
        
        # Optional: validate summary exists
        if 'summary' not in mcp_data:
            logger.warning("MCP data missing 'summary' field (optional)")
        
        return True
    
    @staticmethod
    def categorize_tasks(tasks: List[str]) -> Dict[str, List[str]]:
        """
        Categorize tasks by type for routing to specialist agents
        
        Args:
            tasks: List of task descriptions
            
        Returns:
            Dictionary mapping categories to task lists
        """
        categories = {
            'thermal': [],
            'disk': [],
            'event_log': [],
            'system_files': [],
            'power': [],
            'network': [],
            'memory': [],
            'gpu': [],
            'general': []
        }
        
        for task in tasks:
            task_lower = task.lower()
            categorized = False
            
            # Thermal/CPU
            if any(word in task_lower for word in ['cpu', 'thermal', 'temperature', 'overheat', 'cooling']):
                categories['thermal'].append(task)
                categorized = True
            
            # Disk/Storage
            if any(word in task_lower for word in ['disk', 'storage', 'drive', 'ssd', 'hdd', 'partition']):
                categories['disk'].append(task)
                categorized = True
            
            # Event Logs
            if any(word in task_lower for word in ['event', 'log', 'error message', 'crash', 'blue screen', 'bsod']):
                categories['event_log'].append(task)
                categorized = True
            
            # System Files
            if any(word in task_lower for word in ['system file', 'sfc', 'corruption', 'integrity', 'dism']):
                categories['system_files'].append(task)
                categorized = True
            
            # Power Management
            if any(word in task_lower for word in ['power', 'battery', 'sleep', 'hibernation', 'energy']):
                categories['power'].append(task)
                categorized = True
            
            # Network
            if any(word in task_lower for word in ['network', 'internet', 'wifi', 'ethernet', 'connection']):
                categories['network'].append(task)
                categorized = True
            
            # Memory
            if any(word in task_lower for word in ['memory', 'ram', 'virtual memory', 'page file']):
                categories['memory'].append(task)
                categorized = True
            
            # GPU
            if any(word in task_lower for word in ['gpu', 'graphics', 'video', 'display', 'monitor', 'screen']):
                categories['gpu'].append(task)
                categorized = True
            
            # If not categorized, add to general
            if not categorized:
                categories['general'].append(task)
        
        # Remove empty categories
        categories = {k: v for k, v in categories.items() if v}
        
        logger.info(f"Categorized tasks: {', '.join([f'{k}({len(v)})' for k, v in categories.items()])}")
        
        return categories
    
    @staticmethod
    def get_user_friendly_message(model_output: str) -> str:
        """
        Extract the user-friendly message (everything before <MCP_TASKS>)
        
        Args:
            model_output: The full text output from the AI model
            
        Returns:
            User-friendly message without MCP tasks
        """
        try:
            # Split at <MCP_TASKS> and take the first part
            parts = re.split(r'<MCP_TASKS>', model_output, flags=re.IGNORECASE)
            return parts[0].strip()
        except Exception as e:
            logger.error(f"Error extracting user message: {str(e)}")
            return model_output
