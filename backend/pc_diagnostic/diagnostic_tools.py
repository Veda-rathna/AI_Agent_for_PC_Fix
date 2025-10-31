"""
Diagnostic Tools Module
Provides real diagnostic functions that the AI can call via tool use
"""

import subprocess
import json
import platform
import re
from datetime import datetime, timedelta
import psutil


def check_disk_health(drive_letter=None):
    """
    Run SMART diagnostics on drives to check for disk errors or failures
    
    Args:
        drive_letter: Specific drive to check (e.g., 'C'). None checks all drives
        
    Returns:
        dict: Diagnostic results including health status and errors
    """
    try:
        results = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'drives': []
        }
        
        # Get disk partitions
        partitions = psutil.disk_partitions()
        
        for partition in partitions:
            # Filter by drive letter if specified
            if drive_letter and not partition.device.startswith(drive_letter):
                continue
                
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                
                drive_info = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total_gb': round(usage.total / (1024**3), 2),
                    'used_gb': round(usage.used / (1024**3), 2),
                    'free_gb': round(usage.free / (1024**3), 2),
                    'percent_used': usage.percent,
                    'status': 'healthy' if usage.percent < 90 else 'warning',
                    'io_counters': None
                }
                
                # Try to get IO statistics
                try:
                    io_counters = psutil.disk_io_counters(perdisk=True)
                    disk_name = partition.device.rstrip('\\').replace(':', '')
                    if disk_name in io_counters:
                        counters = io_counters[disk_name]
                        drive_info['io_counters'] = {
                            'read_count': counters.read_count,
                            'write_count': counters.write_count,
                            'read_bytes': counters.read_bytes,
                            'write_bytes': counters.write_bytes
                        }
                except:
                    pass
                
                # Run WMIC check for disk status (Windows only)
                if platform.system() == 'Windows':
                    try:
                        cmd = f'wmic diskdrive get status,model,size /format:list'
                        output = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
                        drive_info['wmic_status'] = 'OK' if 'Status=OK' in output else 'Unknown'
                    except:
                        drive_info['wmic_status'] = 'Unable to query'
                
                results['drives'].append(drive_info)
                
            except PermissionError:
                results['drives'].append({
                    'device': partition.device,
                    'status': 'permission_denied',
                    'error': 'Unable to access drive'
                })
        
        # Add summary
        results['summary'] = {
            'total_drives': len(results['drives']),
            'healthy_drives': sum(1 for d in results['drives'] if d.get('status') == 'healthy'),
            'warning_drives': sum(1 for d in results['drives'] if d.get('status') == 'warning')
        }
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def scan_event_logs(log_type='System', hours_back=24, keywords=None):
    """
    Scan Windows Event Viewer for errors related to hardware or drivers
    
    Args:
        log_type: Type of event log ('System', 'Application', 'Hardware')
        hours_back: How many hours back to search
        keywords: List of keywords to filter by
        
    Returns:
        dict: Event log entries matching criteria
    """
    try:
        if platform.system() != 'Windows':
            return {
                'success': False,
                'error': 'Event log scanning only available on Windows',
                'timestamp': datetime.now().isoformat()
            }
        
        results = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'log_type': log_type,
            'hours_back': hours_back,
            'keywords': keywords or [],
            'events': []
        }
        
        # Build PowerShell command to query event logs
        # Get events from the last X hours
        time_filter = (datetime.now() - timedelta(hours=hours_back)).strftime('%Y-%m-%dT%H:%M:%S')
        
        # Build filter string
        filter_parts = [f"TimeCreated >= '{time_filter}'", "Level <= 3"]  # Level 3 = Warning and below (Error, Critical)
        
        if keywords:
            # Add keyword filters
            keyword_filter = ' or '.join([f"Message -like '*{kw}*'" for kw in keywords])
            filter_parts.append(f"({keyword_filter})")
        
        filter_string = ' and '.join(filter_parts)
        
        # PowerShell command to get events
        ps_command = f"""
        Get-WinEvent -FilterHashtable @{{
            LogName='{log_type}'; 
            StartTime=(Get-Date).AddHours(-{hours_back})
        }} -MaxEvents 50 -ErrorAction SilentlyContinue | 
        Where-Object {{$_.Level -le 3}} |
        Select-Object TimeCreated, Id, LevelDisplayName, Message, ProviderName |
        ConvertTo-Json
        """
        
        # Execute PowerShell command
        try:
            output = subprocess.check_output(
                ['powershell', '-Command', ps_command],
                text=True,
                timeout=30,
                stderr=subprocess.PIPE
            )
            
            if output.strip():
                events = json.loads(output)
                
                # Ensure events is a list
                if isinstance(events, dict):
                    events = [events]
                
                # Filter by keywords if specified
                if keywords:
                    filtered_events = []
                    for event in events:
                        message = event.get('Message', '').lower()
                        if any(kw.lower() in message for kw in keywords):
                            filtered_events.append(event)
                    events = filtered_events
                
                results['events'] = events[:20]  # Limit to 20 most recent
                results['total_found'] = len(events)
                results['showing'] = min(len(events), 20)
            else:
                results['events'] = []
                results['total_found'] = 0
                results['showing'] = 0
                
        except subprocess.TimeoutExpired:
            results['success'] = False
            results['error'] = 'Event log query timed out'
        except json.JSONDecodeError:
            results['events'] = []
            results['total_found'] = 0
            results['showing'] = 0
            results['note'] = 'No events found matching criteria'
        
        # Add summary
        results['summary'] = {
            'critical_errors': sum(1 for e in results['events'] if e.get('LevelDisplayName') == 'Critical'),
            'errors': sum(1 for e in results['events'] if e.get('LevelDisplayName') == 'Error'),
            'warnings': sum(1 for e in results['events'] if e.get('LevelDisplayName') == 'Warning')
        }
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def verify_driver_integrity(device_type='all'):
    """
    Check if system drivers are properly signed and up-to-date
    
    Args:
        device_type: Type of device drivers to verify 
                    ('display', 'network', 'audio', 'storage', 'all')
        
    Returns:
        dict: Driver integrity check results
    """
    try:
        if platform.system() != 'Windows':
            return {
                'success': False,
                'error': 'Driver verification only available on Windows',
                'timestamp': datetime.now().isoformat()
            }
        
        results = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'device_type': device_type,
            'drivers': []
        }
        
        # Map device types to device classes
        device_class_map = {
            'display': 'Display',
            'network': 'Net',
            'audio': 'MEDIA',
            'storage': 'DiskDrive',
            'all': None
        }
        
        device_class = device_class_map.get(device_type.lower())
        
        # Build PowerShell command to get driver info
        if device_class:
            ps_command = f"""
            Get-WmiObject Win32_PnPSignedDriver | 
            Where-Object {{$_.DeviceClass -eq '{device_class}'}} |
            Select-Object DeviceName, DriverVersion, DriverDate, IsSigned, Manufacturer, DeviceClass |
            ConvertTo-Json
            """
        else:
            ps_command = """
            Get-WmiObject Win32_PnPSignedDriver | 
            Where-Object {$_.DeviceClass -in @('Display', 'Net', 'MEDIA', 'DiskDrive')} |
            Select-Object DeviceName, DriverVersion, DriverDate, IsSigned, Manufacturer, DeviceClass |
            ConvertTo-Json
            """
        
        try:
            output = subprocess.check_output(
                ['powershell', '-Command', ps_command],
                text=True,
                timeout=30,
                stderr=subprocess.PIPE
            )
            
            if output.strip():
                drivers = json.loads(output)
                
                # Ensure drivers is a list
                if isinstance(drivers, dict):
                    drivers = [drivers]
                
                # Process driver information
                for driver in drivers:
                    driver_info = {
                        'device_name': driver.get('DeviceName'),
                        'driver_version': driver.get('DriverVersion'),
                        'driver_date': driver.get('DriverDate'),
                        'is_signed': driver.get('IsSigned'),
                        'manufacturer': driver.get('Manufacturer'),
                        'device_class': driver.get('DeviceClass'),
                        'status': 'OK' if driver.get('IsSigned') else 'UNSIGNED'
                    }
                    
                    # Parse driver date if available
                    if driver_info['driver_date']:
                        try:
                            # WMI date format: 20231015000000.000000-000
                            date_str = driver_info['driver_date'][:8]
                            driver_date = datetime.strptime(date_str, '%Y%m%d')
                            driver_info['driver_age_days'] = (datetime.now() - driver_date).days
                            
                            # Flag old drivers (> 2 years)
                            if driver_info['driver_age_days'] > 730:
                                driver_info['status'] = 'OUTDATED'
                        except:
                            pass
                    
                    results['drivers'].append(driver_info)
                
                results['total_drivers'] = len(results['drivers'])
            else:
                results['drivers'] = []
                results['total_drivers'] = 0
                
        except subprocess.TimeoutExpired:
            results['success'] = False
            results['error'] = 'Driver query timed out'
        except json.JSONDecodeError:
            results['drivers'] = []
            results['total_drivers'] = 0
            results['note'] = 'No drivers found'
        
        # Add summary
        results['summary'] = {
            'total_drivers': len(results['drivers']),
            'signed_drivers': sum(1 for d in results['drivers'] if d.get('is_signed')),
            'unsigned_drivers': sum(1 for d in results['drivers'] if not d.get('is_signed')),
            'outdated_drivers': sum(1 for d in results['drivers'] if d.get('status') == 'OUTDATED')
        }
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def check_gpu_status():
    """
    Check GPU status including drivers, temperature, and utilization
    
    Returns:
        dict: GPU diagnostic information
    """
    try:
        results = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'gpus': []
        }
        
        if platform.system() == 'Windows':
            # Try to get GPU info using WMIC
            try:
                cmd = 'wmic path win32_VideoController get name,driverversion,status /format:list'
                output = subprocess.check_output(cmd, shell=True, text=True, timeout=10)
                
                # Parse WMIC output
                gpu_blocks = output.strip().split('\n\n')
                for block in gpu_blocks:
                    if block.strip():
                        gpu_info = {}
                        for line in block.split('\n'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                gpu_info[key.strip().lower()] = value.strip()
                        
                        if gpu_info.get('name'):
                            results['gpus'].append({
                                'name': gpu_info.get('name'),
                                'driver_version': gpu_info.get('driverversion'),
                                'status': gpu_info.get('status', 'Unknown')
                            })
            except:
                pass
        
        # Add summary
        results['summary'] = {
            'total_gpus': len(results['gpus']),
            'healthy_gpus': sum(1 for g in results['gpus'] if g.get('status') == 'OK')
        }
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def test_memory():
    """
    Run memory diagnostic tests
    
    Returns:
        dict: Memory test results
    """
    try:
        results = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'memory_info': {}
        }
        
        # Get memory information
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        results['memory_info'] = {
            'total_gb': round(mem.total / (1024**3), 2),
            'available_gb': round(mem.available / (1024**3), 2),
            'used_gb': round(mem.used / (1024**3), 2),
            'percent_used': mem.percent,
            'status': 'healthy' if mem.percent < 85 else 'warning',
            'swap_total_gb': round(swap.total / (1024**3), 2),
            'swap_used_gb': round(swap.used / (1024**3), 2),
            'swap_percent': swap.percent
        }
        
        # Check for memory pressure
        if mem.percent > 90:
            results['memory_info']['alert'] = 'Critical: Very high memory usage detected'
        elif mem.percent > 85:
            results['memory_info']['alert'] = 'Warning: High memory usage detected'
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }


def check_network_connectivity(target='8.8.8.8'):
    """
    Test network connectivity and diagnose network issues
    
    Args:
        target: IP address or hostname to ping
        
    Returns:
        dict: Network diagnostic results
    """
    try:
        results = {
            'success': True,
            'timestamp': datetime.now().isoformat(),
            'target': target,
            'connectivity': {}
        }
        
        # Ping test
        param = '-n' if platform.system() == 'Windows' else '-c'
        command = ['ping', param, '4', target]
        
        try:
            output = subprocess.check_output(
                command,
                text=True,
                timeout=10,
                stderr=subprocess.PIPE
            )
            
            results['connectivity']['ping_success'] = True
            results['connectivity']['status'] = 'Connected'
            
            # Parse ping statistics
            if 'Average' in output or 'avg' in output:
                # Extract average time
                match = re.search(r'Average = (\d+)ms', output) or re.search(r'avg = ([\d.]+)', output)
                if match:
                    results['connectivity']['avg_latency_ms'] = float(match.group(1))
            
        except subprocess.CalledProcessError:
            results['connectivity']['ping_success'] = False
            results['connectivity']['status'] = 'No connectivity'
        except subprocess.TimeoutExpired:
            results['connectivity']['ping_success'] = False
            results['connectivity']['status'] = 'Timeout'
        
        # Get network interfaces
        try:
            net_if = psutil.net_if_stats()
            results['interfaces'] = []
            
            for interface, stats in net_if.items():
                results['interfaces'].append({
                    'name': interface,
                    'is_up': stats.isup,
                    'speed_mbps': stats.speed
                })
        except:
            pass
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
