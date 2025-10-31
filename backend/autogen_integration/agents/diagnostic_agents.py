"""
Diagnostic Agents

AutoGen agents for executing diagnostic tasks (OPTIONAL)

Note: This module provides AutoGen agent support for advanced workflows.
The system works perfectly with direct execution mode without these agents.
"""

from typing import Dict, Any, List, Callable, Optional, TYPE_CHECKING
import logging
import json

from ..tools.system_diagnostics import SystemDiagnostics
from ..tools.event_logs import EventLogAnalyzer
from ..tools.file_checker import SystemFileChecker

logger = logging.getLogger(__name__)

# Try to import autogen, but make it optional
try:
    import autogen
    AUTOGEN_AVAILABLE = True
except ImportError:
    AUTOGEN_AVAILABLE = False
    logger.warning("AutoGen not installed - agent mode unavailable. Direct execution mode will be used.")
    
    # Create stub namespace for compatibility
    class autogen:
        class UserProxyAgent:
            def __init__(self, *args, **kwargs):
                raise ImportError("AutoGen not installed. Install with: pip install pyautogen")
        
        class AssistantAgent:
            def __init__(self, *args, **kwargs):
                raise ImportError("AutoGen not installed. Install with: pip install pyautogen")


class DiagnosticAgentFactory:
    """Factory for creating and configuring diagnostic agents"""
    
    def __init__(self, llm_config: Dict[str, Any] = None):
        """
        Initialize the agent factory
        
        Args:
            llm_config: Configuration for LLM (optional, uses local config if None)
        """
        self.llm_config = llm_config or self._get_default_llm_config()
        self.system_diagnostics = SystemDiagnostics()
        self.event_analyzer = EventLogAnalyzer()
        self.file_checker = SystemFileChecker()
    
    def _get_default_llm_config(self) -> Dict[str, Any]:
        """Get default LLM configuration"""
        return {
            "config_list": [{
                "model": "gpt-3.5-turbo",
                "api_key": "dummy",  # Will be overridden by environment or config
            }],
            "temperature": 0.7,
            "timeout": 120,
        }
    
    def create_user_proxy(self, human_input_mode: str = "NEVER") -> autogen.UserProxyAgent:
        """
        Create UserProxy agent that initiates task execution
        
        Args:
            human_input_mode: "ALWAYS", "NEVER", or "TERMINATE"
            
        Returns:
            Configured UserProxyAgent
        """
        user_proxy = autogen.UserProxyAgent(
            name="UserProxy",
            human_input_mode=human_input_mode,
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={
                "work_dir": "autogen_workdir",
                "use_docker": False,
            },
            system_message="""You are a user proxy agent that coordinates diagnostic task execution.
Your role is to initiate tasks and relay results back to the user."""
        )
        
        logger.info("Created UserProxy agent")
        return user_proxy
    
    def create_coordinator(self) -> autogen.AssistantAgent:
        """
        Create Coordinator agent that manages task delegation
        
        Returns:
            Configured AssistantAgent for coordination
        """
        coordinator = autogen.AssistantAgent(
            name="DiagnosticCoordinator",
            llm_config=self.llm_config,
            system_message="""You are a Diagnostic Coordinator Agent.

Your responsibilities:
1. Receive lists of diagnostic tasks
2. Delegate tasks to appropriate specialist agents
3. Collect and aggregate results
4. Provide summary of findings

When you receive a list of tasks, analyze each one and assign to:
- SystemAgent: CPU, memory, disk, power management tasks
- SecurityAgent: Event logs, system file checks, security scans

Coordinate execution and compile a comprehensive diagnostic report.
Reply TERMINATE when all tasks are completed and results compiled."""
        )
        
        logger.info("Created Coordinator agent")
        return coordinator
    
    def create_system_agent(self) -> autogen.AssistantAgent:
        """
        Create System diagnostic agent with tool functions
        
        Returns:
            Configured AssistantAgent with system diagnostic tools
        """
        
        # Define tool functions
        def analyze_cpu_thermal() -> str:
            """Analyze CPU thermal sensor readings for overheating patterns"""
            result = self.system_diagnostics.analyze_cpu_thermal()
            return json.dumps(result, indent=2)
        
        def inspect_disk_usage() -> str:
            """Inspect disk usage telemetry for resource-intensive programs or malware"""
            result = self.system_diagnostics.inspect_disk_usage()
            return json.dumps(result, indent=2)
        
        def check_power_settings() -> str:
            """Check system configuration for power management settings that could limit performance"""
            result = self.system_diagnostics.check_power_settings()
            return json.dumps(result, indent=2)
        
        def check_memory_usage() -> str:
            """Analyze system memory usage and identify memory-intensive processes"""
            result = self.system_diagnostics.check_memory_usage()
            return json.dumps(result, indent=2)
        
        # Create agent with function calling
        system_agent = autogen.AssistantAgent(
            name="SystemDiagnosticAgent",
            llm_config=self.llm_config,
            system_message="""You are a System Diagnostic Agent specializing in:
- CPU thermal analysis and performance monitoring
- Disk usage analysis and storage diagnostics  
- Memory usage tracking and optimization
- Power management configuration

You have access to diagnostic tools. When asked to perform a diagnostic task:
1. Use the appropriate tool function
2. Analyze the results
3. Provide clear findings and recommendations

Available tools:
- analyze_cpu_thermal(): Check CPU temperature and usage
- inspect_disk_usage(): Analyze disk space and I/O
- check_power_settings(): Review power management
- check_memory_usage(): Analyze RAM usage

Provide concise, actionable diagnostic insights.""",
            function_map={
                "analyze_cpu_thermal": analyze_cpu_thermal,
                "inspect_disk_usage": inspect_disk_usage,
                "check_power_settings": check_power_settings,
                "check_memory_usage": check_memory_usage,
            }
        )
        
        logger.info("Created System Diagnostic agent with tools")
        return system_agent
    
    def create_security_agent(self) -> autogen.AssistantAgent:
        """
        Create Security diagnostic agent with tool functions
        
        Returns:
            Configured AssistantAgent with security diagnostic tools
        """
        
        # Define tool functions
        def verify_event_logs() -> str:
            """Verify Windows Event Logs for error messages related to system crashes, freezes, or blue screens"""
            result = self.event_analyzer.verify_event_logs()
            return json.dumps(result, indent=2)
        
        def scan_system_files() -> str:
            """Scan system files for potential corruption and verify system file integrity using SFC"""
            result = self.file_checker.scan_system_files()
            return json.dumps(result, indent=2)
        
        def check_dism_health() -> str:
            """Check Windows image health using DISM tool"""
            result = self.file_checker.check_dism_health()
            return json.dumps(result, indent=2)
        
        # Create agent with function calling
        security_agent = autogen.AssistantAgent(
            name="SecurityDiagnosticAgent",
            llm_config=self.llm_config,
            system_message="""You are a Security Diagnostic Agent specializing in:
- Windows Event Log analysis
- System file integrity verification (SFC)
- Windows image health (DISM)
- Security and stability diagnostics

You have access to diagnostic tools. When asked to perform a diagnostic task:
1. Use the appropriate tool function
2. Analyze the results
3. Identify security or stability issues
4. Provide clear remediation steps

Available tools:
- verify_event_logs(): Check Windows Event Logs for errors
- scan_system_files(): Run SFC scan (requires admin)
- check_dism_health(): Check Windows image health (requires admin)

Note: Some tools require administrator privileges. Provide manual instructions if privileges are insufficient.

Provide concise, actionable security insights.""",
            function_map={
                "verify_event_logs": verify_event_logs,
                "scan_system_files": scan_system_files,
                "check_dism_health": check_dism_health,
            }
        )
        
        logger.info("Created Security Diagnostic agent with tools")
        return security_agent
    
    def create_all_agents(self, human_input_mode: str = "NEVER") -> Dict[str, Any]:
        """
        Create all diagnostic agents
        
        Args:
            human_input_mode: Human input mode for UserProxy
            
        Returns:
            Dictionary of all agents
        """
        agents = {
            "user_proxy": self.create_user_proxy(human_input_mode),
            "coordinator": self.create_coordinator(),
            "system_agent": self.create_system_agent(),
            "security_agent": self.create_security_agent(),
        }
        
        logger.info(f"Created {len(agents)} agents")
        return agents
