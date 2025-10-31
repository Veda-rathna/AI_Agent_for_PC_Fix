"""
Event Log Analyzer

Tools for analyzing Windows Event Logs
"""

import subprocess
import logging
import platform
from typing import Dict, Any, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class EventLogAnalyzer:
    """Tools for Windows Event Log analysis"""
    
    @staticmethod
    def verify_event_logs() -> Dict[str, Any]:
        """
        Verify Windows Event Logs for error messages related to crashes and blue screens
        
        Returns:
            Dictionary with event log analysis
        """
        try:
            result = {
                "success": True,
                "task": "Windows Event Log Verification",
                "data": {}
            }
            
            if platform.system() != "Windows":
                return {
                    "success": False,
                    "task": "Windows Event Log Verification",
                    "error": "Event log analysis only available on Windows"
                }
            
            # Get System errors (last 50)
            try:
                cmd = 'powershell -Command "Get-EventLog -LogName System -Newest 50 -EntryType Error | Select-Object TimeGenerated, Source, EventID, Message | ConvertTo-Json"'
                output = subprocess.check_output(cmd, shell=True, text=True, timeout=30)
                
                import json
                system_errors = json.loads(output) if output.strip() else []
                
                if isinstance(system_errors, dict):
                    system_errors = [system_errors]
                
                result["data"]["system_errors"] = system_errors
                result["data"]["system_error_count"] = len(system_errors) if system_errors else 0
                
            except subprocess.TimeoutExpired:
                result["data"]["system_errors_note"] = "System event log query timed out"
            except Exception as e:
                result["data"]["system_errors_note"] = f"Could not retrieve system errors: {str(e)}"
            
            # Get Application errors (last 50)
            try:
                cmd = 'powershell -Command "Get-EventLog -LogName Application -Newest 50 -EntryType Error | Select-Object TimeGenerated, Source, EventID, Message | ConvertTo-Json"'
                output = subprocess.check_output(cmd, shell=True, text=True, timeout=30)
                
                import json
                app_errors = json.loads(output) if output.strip() else []
                
                if isinstance(app_errors, dict):
                    app_errors = [app_errors]
                
                result["data"]["application_errors"] = app_errors
                result["data"]["application_error_count"] = len(app_errors) if app_errors else 0
                
            except subprocess.TimeoutExpired:
                result["data"]["application_errors_note"] = "Application event log query timed out"
            except Exception as e:
                result["data"]["application_errors_note"] = f"Could not retrieve application errors: {str(e)}"
            
            # Look for critical events (BSOD, crashes)
            try:
                cmd = 'powershell -Command "Get-EventLog -LogName System -Newest 100 | Where-Object {$_.EventID -in @(41, 1001, 6008)} | Select-Object TimeGenerated, Source, EventID, Message | ConvertTo-Json"'
                output = subprocess.check_output(cmd, shell=True, text=True, timeout=30)
                
                import json
                critical_events = json.loads(output) if output.strip() else []
                
                if isinstance(critical_events, dict):
                    critical_events = [critical_events]
                
                result["data"]["critical_events"] = critical_events
                result["data"]["critical_event_count"] = len(critical_events) if critical_events else 0
                
                # Event ID meanings:
                # 41: Kernel-Power - System rebooted without cleanly shutting down
                # 1001: BugCheck - BSOD occurred
                # 6008: EventLog - Unexpected shutdown
                
            except Exception as e:
                result["data"]["critical_events_note"] = f"Could not retrieve critical events: {str(e)}"
            
            # Analysis
            total_errors = result["data"].get("system_error_count", 0) + result["data"].get("application_error_count", 0)
            critical_count = result["data"].get("critical_event_count", 0)
            
            if critical_count > 0:
                result["analysis"] = f"⚠️ CRITICAL: {critical_count} system crash/BSOD event(s) detected"
                result["severity"] = "high"
            elif total_errors > 100:
                result["analysis"] = f"⚠️ High error volume: {total_errors} errors in recent logs"
                result["severity"] = "medium"
            elif total_errors > 0:
                result["analysis"] = f"⚡ {total_errors} errors found in event logs"
                result["severity"] = "low"
            else:
                result["analysis"] = "✅ No critical errors in recent event logs"
                result["severity"] = "low"
            
            logger.info(f"Event log verification completed: {result.get('analysis', 'No analysis')}")
            return result
            
        except Exception as e:
            logger.error(f"Event log verification failed: {str(e)}")
            return {
                "success": False,
                "task": "Windows Event Log Verification",
                "error": str(e)
            }
    
    @staticmethod
    def search_event_logs(keywords: List[str], hours_back: int = 24) -> Dict[str, Any]:
        """
        Search event logs for specific keywords
        
        Args:
            keywords: List of keywords to search for
            hours_back: How many hours back to search
            
        Returns:
            Dictionary with matching events
        """
        try:
            result = {
                "success": True,
                "task": f"Event Log Search for: {', '.join(keywords)}",
                "data": {}
            }
            
            if platform.system() != "Windows":
                return {
                    "success": False,
                    "task": "Event Log Search",
                    "error": "Event log search only available on Windows"
                }
            
            # Calculate start time
            start_time = datetime.now() - timedelta(hours=hours_back)
            start_time_str = start_time.strftime("%m/%d/%Y %H:%M:%S")
            
            matches = []
            for keyword in keywords:
                try:
                    cmd = f'powershell -Command "Get-EventLog -LogName System -After \\"{start_time_str}\\" | Where-Object {{$_.Message -like \\"*{keyword}*\\"}} | Select-Object TimeGenerated, Source, EventID, EntryType, Message | ConvertTo-Json"'
                    output = subprocess.check_output(cmd, shell=True, text=True, timeout=30)
                    
                    if output.strip():
                        import json
                        keyword_matches = json.loads(output)
                        if isinstance(keyword_matches, dict):
                            keyword_matches = [keyword_matches]
                        
                        matches.extend(keyword_matches)
                
                except Exception as e:
                    logger.warning(f"Search for '{keyword}' failed: {str(e)}")
            
            result["data"]["matches"] = matches
            result["data"]["match_count"] = len(matches)
            result["analysis"] = f"Found {len(matches)} event(s) matching search criteria"
            
            logger.info(f"Event log search completed: {len(matches)} matches")
            return result
            
        except Exception as e:
            logger.error(f"Event log search failed: {str(e)}")
            return {
                "success": False,
                "task": "Event Log Search",
                "error": str(e)
            }
