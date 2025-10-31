"""
System Diagnostics Tools

Windows diagnostic commands for CPU, Disk, Memory, and Power Management
"""

import subprocess
import psutil
import json
import logging
from typing import Dict, Any, List
import platform

logger = logging.getLogger(__name__)


class SystemDiagnostics:
    """Tools for system-level diagnostics"""
    
    @staticmethod
    def analyze_cpu_thermal() -> Dict[str, Any]:
        """
        Analyze CPU thermal sensor readings for overheating patterns
        
        Returns:
            Dictionary with CPU temperature and usage data
        """
        try:
            result = {
                "success": True,
                "task": "CPU Thermal Analysis",
                "data": {}
            }
            
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            cpu_freq = psutil.cpu_freq(percpu=False)
            
            result["data"]["cpu_usage_per_core"] = cpu_percent
            result["data"]["cpu_usage_average"] = sum(cpu_percent) / len(cpu_percent)
            result["data"]["cpu_count"] = psutil.cpu_count()
            
            if cpu_freq:
                result["data"]["cpu_frequency_mhz"] = {
                    "current": cpu_freq.current,
                    "min": cpu_freq.min,
                    "max": cpu_freq.max
                }
            
            # Try to get temperature using WMI (Windows)
            if platform.system() == "Windows":
                try:
                    cmd = 'wmic /namespace:\\\\root\\wmi PATH MSAcpi_ThermalZoneTemperature get CurrentTemperature'
                    output = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
                    
                    # Parse temperature (in tenths of Kelvin)
                    temps = []
                    for line in output.split('\n')[1:]:
                        line = line.strip()
                        if line and line.isdigit():
                            # Convert from tenths of Kelvin to Celsius
                            temp_celsius = (int(line) / 10.0) - 273.15
                            temps.append(round(temp_celsius, 2))
                    
                    if temps:
                        result["data"]["thermal_zones_celsius"] = temps
                        result["data"]["max_temperature_celsius"] = max(temps)
                        result["data"]["avg_temperature_celsius"] = sum(temps) / len(temps)
                        
                        # Analysis
                        if max(temps) > 80:
                            result["analysis"] = "⚠️ HIGH TEMPERATURE DETECTED - CPU overheating risk"
                            result["severity"] = "high"
                        elif max(temps) > 70:
                            result["analysis"] = "⚡ Elevated temperature - Monitor for thermal throttling"
                            result["severity"] = "medium"
                        else:
                            result["analysis"] = "✅ CPU temperature normal"
                            result["severity"] = "low"
                except subprocess.TimeoutExpired:
                    result["data"]["temperature_note"] = "WMI thermal query timed out"
                except Exception as e:
                    result["data"]["temperature_note"] = f"WMI thermal sensor not available: {str(e)}"
            
            logger.info(f"CPU thermal analysis completed: {result.get('analysis', 'No analysis')}")
            return result
            
        except Exception as e:
            logger.error(f"CPU thermal analysis failed: {str(e)}")
            return {
                "success": False,
                "task": "CPU Thermal Analysis",
                "error": str(e)
            }
    
    @staticmethod
    def inspect_disk_usage() -> Dict[str, Any]:
        """
        Inspect disk usage telemetry for signs of resource-intensive programs
        
        Returns:
            Dictionary with disk usage and process information
        """
        try:
            result = {
                "success": True,
                "task": "Disk Usage Analysis",
                "data": {}
            }
            
            # Get disk usage for all partitions
            partitions = psutil.disk_partitions()
            disk_info = []
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        "device": partition.device,
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "percent_used": usage.percent
                    })
                except PermissionError:
                    continue
            
            result["data"]["partitions"] = disk_info
            
            # Get disk I/O statistics
            disk_io = psutil.disk_io_counters()
            if disk_io:
                result["data"]["disk_io"] = {
                    "read_count": disk_io.read_count,
                    "write_count": disk_io.write_count,
                    "read_bytes": disk_io.read_bytes,
                    "write_bytes": disk_io.write_bytes,
                    "read_time_ms": disk_io.read_time,
                    "write_time_ms": disk_io.write_time
                }
            
            # Get top processes by disk I/O (requires elevated permissions)
            try:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'io_counters']):
                    try:
                        io = proc.info['io_counters']
                        if io:
                            processes.append({
                                "pid": proc.info['pid'],
                                "name": proc.info['name'],
                                "read_bytes": io.read_bytes,
                                "write_bytes": io.write_bytes
                            })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                
                # Sort by total I/O
                processes.sort(key=lambda x: x['read_bytes'] + x['write_bytes'], reverse=True)
                result["data"]["top_disk_processes"] = processes[:10]
                
            except Exception as e:
                result["data"]["process_note"] = f"Process I/O data requires admin: {str(e)}"
            
            # Analysis
            critical_partitions = [p for p in disk_info if p['percent_used'] > 90]
            if critical_partitions:
                result["analysis"] = f"⚠️ CRITICAL: {len(critical_partitions)} partition(s) nearly full"
                result["severity"] = "high"
            elif any(p['percent_used'] > 80 for p in disk_info):
                result["analysis"] = "⚡ Warning: Low disk space detected"
                result["severity"] = "medium"
            else:
                result["analysis"] = "✅ Disk space healthy"
                result["severity"] = "low"
            
            logger.info(f"Disk usage analysis completed: {result.get('analysis', 'No analysis')}")
            return result
            
        except Exception as e:
            logger.error(f"Disk usage analysis failed: {str(e)}")
            return {
                "success": False,
                "task": "Disk Usage Analysis",
                "error": str(e)
            }
    
    @staticmethod
    def check_power_settings() -> Dict[str, Any]:
        """
        Check power management configuration for performance limitations
        
        Returns:
            Dictionary with power scheme information
        """
        try:
            result = {
                "success": True,
                "task": "Power Settings Check",
                "data": {}
            }
            
            if platform.system() != "Windows":
                return {
                    "success": False,
                    "task": "Power Settings Check",
                    "error": "Power settings check only available on Windows"
                }
            
            # Get active power scheme
            try:
                cmd = "powercfg /getactivescheme"
                output = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
                result["data"]["active_scheme"] = output.strip()
                
                # Parse scheme GUID
                if "GUID:" in output:
                    guid = output.split("(")[1].split(")")[0] if "(" in output else None
                    if guid:
                        result["data"]["scheme_guid"] = guid
                
            except subprocess.TimeoutExpired:
                result["data"]["scheme_note"] = "Power scheme query timed out"
            except Exception as e:
                result["data"]["scheme_note"] = f"Could not get power scheme: {str(e)}"
            
            # Get power scheme list
            try:
                cmd = "powercfg /list"
                output = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
                result["data"]["available_schemes"] = output.strip()
            except Exception as e:
                result["data"]["list_note"] = f"Could not list schemes: {str(e)}"
            
            # Get battery status if laptop
            battery = psutil.sensors_battery()
            if battery:
                result["data"]["battery"] = {
                    "percent": battery.percent,
                    "power_plugged": battery.power_plugged,
                    "seconds_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited"
                }
                
                if not battery.power_plugged and battery.percent < 20:
                    result["analysis"] = "⚠️ Low battery - Performance may be throttled"
                    result["severity"] = "medium"
                elif battery.power_plugged:
                    result["analysis"] = "✅ AC power connected"
                    result["severity"] = "low"
            else:
                result["analysis"] = "Desktop system - No battery detected"
                result["severity"] = "low"
            
            logger.info(f"Power settings check completed: {result.get('analysis', 'No analysis')}")
            return result
            
        except Exception as e:
            logger.error(f"Power settings check failed: {str(e)}")
            return {
                "success": False,
                "task": "Power Settings Check",
                "error": str(e)
            }
    
    @staticmethod
    def check_memory_usage() -> Dict[str, Any]:
        """
        Analyze system memory usage and identify memory-intensive processes
        
        Returns:
            Dictionary with memory usage data
        """
        try:
            result = {
                "success": True,
                "task": "Memory Usage Analysis",
                "data": {}
            }
            
            # Get virtual memory stats
            vm = psutil.virtual_memory()
            result["data"]["virtual_memory"] = {
                "total_gb": round(vm.total / (1024**3), 2),
                "available_gb": round(vm.available / (1024**3), 2),
                "used_gb": round(vm.used / (1024**3), 2),
                "percent_used": vm.percent
            }
            
            # Get swap memory stats
            swap = psutil.swap_memory()
            result["data"]["swap_memory"] = {
                "total_gb": round(swap.total / (1024**3), 2),
                "used_gb": round(swap.used / (1024**3), 2),
                "free_gb": round(swap.free / (1024**3), 2),
                "percent_used": swap.percent
            }
            
            # Get top memory-consuming processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'memory_percent']):
                try:
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "memory_mb": round(proc.info['memory_info'].rss / (1024**2), 2),
                        "memory_percent": round(proc.info['memory_percent'], 2)
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            processes.sort(key=lambda x: x['memory_mb'], reverse=True)
            result["data"]["top_memory_processes"] = processes[:10]
            
            # Analysis
            if vm.percent > 90:
                result["analysis"] = "⚠️ CRITICAL: Very high memory usage - System may be slow"
                result["severity"] = "high"
            elif vm.percent > 80:
                result["analysis"] = "⚡ High memory usage detected"
                result["severity"] = "medium"
            else:
                result["analysis"] = "✅ Memory usage normal"
                result["severity"] = "low"
            
            logger.info(f"Memory usage analysis completed: {result.get('analysis', 'No analysis')}")
            return result
            
        except Exception as e:
            logger.error(f"Memory usage analysis failed: {str(e)}")
            return {
                "success": False,
                "task": "Memory Usage Analysis",
                "error": str(e)
            }
