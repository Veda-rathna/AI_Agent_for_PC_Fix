"""
Logging Configuration for AutoGen Integration
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logging(log_dir=None, log_level=logging.INFO, console=True):
    """
    Configure logging for AutoGen integration
    
    Args:
        log_dir: Directory for log files (defaults to ./logs)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console: Whether to also log to console
    """
    # Create log directory if it doesn't exist
    if log_dir is None:
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    
    os.makedirs(log_dir, exist_ok=True)
    
    # Create log filename with timestamp
    log_filename = os.path.join(log_dir, 'autogen_execution.log')
    
    # Create logger
    logger = logging.getLogger('autogen_integration')
    logger.setLevel(log_level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    logger.info("="*60)
    logger.info("AutoGen Integration Logging Initialized")
    logger.info(f"Log Level: {logging.getLevelName(log_level)}")
    logger.info(f"Log File: {log_filename}")
    logger.info("="*60)
    
    return logger


def log_task_execution(logger, task, result):
    """
    Log task execution result
    
    Args:
        logger: Logger instance
        task: Task description
        result: Task execution result dictionary
    """
    success = result.get('success', False)
    severity = result.get('severity', 'unknown')
    
    if success:
        if severity == 'high':
            logger.warning(f"Task '{task}' completed with HIGH severity: {result.get('analysis', 'No analysis')}")
        elif severity == 'medium':
            logger.info(f"Task '{task}' completed with MEDIUM severity: {result.get('analysis', 'No analysis')}")
        else:
            logger.info(f"Task '{task}' completed successfully: {result.get('analysis', 'No analysis')}")
    else:
        logger.error(f"Task '{task}' FAILED: {result.get('error', 'Unknown error')}")


def log_orchestrator_execution(logger, mcp_data, results):
    """
    Log overall orchestrator execution
    
    Args:
        logger: Logger instance
        mcp_data: MCP task data
        results: List of execution results
    """
    total = len(results)
    successful = len([r for r in results if r.get('success')])
    failed = total - successful
    
    logger.info("="*60)
    logger.info("MCP Task Execution Summary")
    logger.info(f"Summary: {mcp_data.get('summary', 'No summary')}")
    logger.info(f"Total Tasks: {total}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")
    
    # Log high severity issues
    high_severity = [r for r in results if r.get('severity') == 'high']
    if high_severity:
        logger.warning(f"HIGH SEVERITY ISSUES DETECTED: {len(high_severity)}")
        for issue in high_severity:
            logger.warning(f"  - {issue.get('task')}: {issue.get('analysis')}")
    
    logger.info("="*60)


# Initialize default logger
default_logger = setup_logging()
