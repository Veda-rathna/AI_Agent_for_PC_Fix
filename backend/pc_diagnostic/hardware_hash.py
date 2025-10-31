"""
Hardware Hash Protection Module

This module handles the generation and analysis of encrypted hardware hash files
for detecting unauthorized hardware changes (e.g., from service center replacements).
"""

import json
import hashlib
import base64
import os
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import platform
import psutil

try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False


class HardwareHashProtection:
    """
    Manages hardware hash generation and verification to detect hardware changes.
    """
    
    # Hardware components that can be changed in service centers
    CHANGEABLE_COMPONENTS = [
        'motherboard',
        'cpu',
        'gpu',
        'ram',
        'storage',
        'display',
        'battery',
        'network_adapter'
    ]
    
    # Hardware components that should remain constant
    PERMANENT_COMPONENTS = [
        'serial_number',
        'uuid',
        'bios_info'
    ]
    
    def __init__(self):
        """Initialize the hardware hash protection system"""
        self.wmi_conn = None
        if WMI_AVAILABLE and platform.system() == "Windows":
            try:
                self.wmi_conn = wmi.WMI()
            except:
                pass
        
        # Generate a static salt for encryption (in production, store this securely)
        self.salt = b'hardware_protection_salt_2025'
    
    def _generate_key(self, password: str) -> bytes:
        """Generate encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def extract_hardware_info(self) -> dict:
        """
        Extract critical hardware information from the system.
        
        Returns:
            dict: Comprehensive hardware information including changeable and permanent components
        """
        hardware_data = {
            "timestamp": datetime.now().isoformat(),
            "platform": platform.system(),
            "permanent_components": {},
            "changeable_components": {},
            "metadata": {
                "hostname": platform.node(),
                "os_version": platform.version(),
                "architecture": platform.machine()
            }
        }
        
        # Extract permanent components
        hardware_data["permanent_components"] = self._get_permanent_components()
        
        # Extract changeable components
        hardware_data["changeable_components"] = self._get_changeable_components()
        
        return hardware_data
    
    def _get_permanent_components(self) -> dict:
        """Extract hardware components that should not change"""
        permanent = {
            "system_uuid": None,
            "bios_serial": None,
            "motherboard_serial": None,
            "processor_id": None
        }
        
        if self.wmi_conn:
            try:
                # Get system UUID
                for cs in self.wmi_conn.Win32_ComputerSystemProduct():
                    permanent["system_uuid"] = cs.UUID
                    permanent["system_serial"] = cs.IdentifyingNumber
                
                # Get BIOS information
                for bios in self.wmi_conn.Win32_BIOS():
                    permanent["bios_serial"] = bios.SerialNumber
                    permanent["bios_version"] = bios.Version
                    permanent["bios_manufacturer"] = bios.Manufacturer
                
                # Get Motherboard information
                for board in self.wmi_conn.Win32_BaseBoard():
                    permanent["motherboard_serial"] = board.SerialNumber
                    permanent["motherboard_product"] = board.Product
                    permanent["motherboard_manufacturer"] = board.Manufacturer
                
                # Get Processor ID
                for cpu in self.wmi_conn.Win32_Processor():
                    permanent["processor_id"] = cpu.ProcessorId
                    
            except Exception as e:
                permanent["error"] = f"WMI error: {str(e)}"
        
        return permanent
    
    def _get_changeable_components(self) -> dict:
        """Extract hardware components that can be changed in service centers"""
        changeable = {
            "cpu": {},
            "gpu": {},
            "ram": {},
            "storage": {},
            "display": {},
            "network": {},
            "battery": {}
        }
        
        # CPU Information
        try:
            if self.wmi_conn:
                for cpu in self.wmi_conn.Win32_Processor():
                    changeable["cpu"] = {
                        "name": cpu.Name,
                        "cores": cpu.NumberOfCores,
                        "logical_processors": cpu.NumberOfLogicalProcessors,
                        "manufacturer": cpu.Manufacturer,
                        "max_clock_speed": cpu.MaxClockSpeed,
                        "current_clock_speed": cpu.CurrentClockSpeed
                    }
            else:
                changeable["cpu"] = {
                    "name": platform.processor(),
                    "cores": psutil.cpu_count(logical=False),
                    "logical_processors": psutil.cpu_count(logical=True)
                }
        except Exception as e:
            changeable["cpu"]["error"] = str(e)
        
        # GPU Information
        try:
            if self.wmi_conn:
                gpus = []
                for gpu in self.wmi_conn.Win32_VideoController():
                    gpus.append({
                        "name": gpu.Name,
                        "adapter_ram": gpu.AdapterRAM,
                        "driver_version": gpu.DriverVersion,
                        "video_processor": gpu.VideoProcessor,
                        "pnp_device_id": gpu.PNPDeviceID
                    })
                changeable["gpu"] = gpus
        except Exception as e:
            changeable["gpu"]["error"] = str(e)
        
        # RAM Information
        try:
            if self.wmi_conn:
                ram_modules = []
                for ram in self.wmi_conn.Win32_PhysicalMemory():
                    ram_modules.append({
                        "capacity": ram.Capacity,
                        "speed": ram.Speed,
                        "manufacturer": ram.Manufacturer,
                        "part_number": ram.PartNumber,
                        "serial_number": ram.SerialNumber,
                        "device_locator": ram.DeviceLocator
                    })
                changeable["ram"] = ram_modules
            else:
                memory = psutil.virtual_memory()
                changeable["ram"] = {
                    "total": memory.total
                }
        except Exception as e:
            changeable["ram"]["error"] = str(e)
        
        # Storage Information
        try:
            if self.wmi_conn:
                drives = []
                for drive in self.wmi_conn.Win32_DiskDrive():
                    drives.append({
                        "model": drive.Model,
                        "size": drive.Size,
                        "serial_number": drive.SerialNumber,
                        "interface_type": drive.InterfaceType,
                        "media_type": drive.MediaType
                    })
                changeable["storage"] = drives
            else:
                partitions = psutil.disk_partitions()
                changeable["storage"] = [
                    {
                        "device": p.device,
                        "mountpoint": p.mountpoint,
                        "fstype": p.fstype
                    } for p in partitions
                ]
        except Exception as e:
            changeable["storage"]["error"] = str(e)
        
        # Display Information
        try:
            if self.wmi_conn:
                displays = []
                for monitor in self.wmi_conn.Win32_DesktopMonitor():
                    displays.append({
                        "name": monitor.Name,
                        "pnp_device_id": monitor.PNPDeviceID,
                        "screen_width": monitor.ScreenWidth,
                        "screen_height": monitor.ScreenHeight
                    })
                changeable["display"] = displays
        except Exception as e:
            changeable["display"]["error"] = str(e)
        
        # Network Adapters
        try:
            if self.wmi_conn:
                adapters = []
                for adapter in self.wmi_conn.Win32_NetworkAdapter():
                    if adapter.PhysicalAdapter and adapter.MACAddress:
                        adapters.append({
                            "name": adapter.Name,
                            "mac_address": adapter.MACAddress,
                            "manufacturer": adapter.Manufacturer,
                            "pnp_device_id": adapter.PNPDeviceID
                        })
                changeable["network"] = adapters
        except Exception as e:
            changeable["network"]["error"] = str(e)
        
        # Battery Information
        try:
            if self.wmi_conn:
                batteries = []
                for battery in self.wmi_conn.Win32_Battery():
                    batteries.append({
                        "name": battery.Name,
                        "chemistry": battery.Chemistry,
                        "design_capacity": battery.DesignCapacity,
                        "full_charge_capacity": battery.FullChargeCapacity
                    })
                changeable["battery"] = batteries
            elif hasattr(psutil, 'sensors_battery'):
                battery = psutil.sensors_battery()
                if battery:
                    changeable["battery"] = {
                        "percent": battery.percent,
                        "power_plugged": battery.power_plugged
                    }
        except Exception as e:
            changeable["battery"]["error"] = str(e)
        
        return changeable
    
    def generate_hardware_hash(self, hardware_data: dict) -> str:
        """
        Generate a SHA-256 hash of the hardware data.
        
        Args:
            hardware_data: Dictionary containing hardware information
            
        Returns:
            str: Hexadecimal hash string
        """
        # Convert hardware data to JSON string
        hardware_json = json.dumps(hardware_data, sort_keys=True, default=str)
        
        # Generate SHA-256 hash
        hash_object = hashlib.sha256(hardware_json.encode())
        return hash_object.hexdigest()
    
    def encrypt_hardware_data(self, hardware_data: dict, password: str = "default_password") -> str:
        """
        Encrypt hardware data using Fernet (symmetric encryption).
        
        Args:
            hardware_data: Dictionary containing hardware information
            password: Password for encryption (default: "default_password")
            
        Returns:
            str: Base64 encoded encrypted data
        """
        # Generate encryption key
        key = self._generate_key(password)
        cipher = Fernet(key)
        
        # Convert to JSON and encrypt
        hardware_json = json.dumps(hardware_data, indent=2, default=str)
        encrypted_data = cipher.encrypt(hardware_json.encode())
        
        return base64.b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_hardware_data(self, encrypted_data: str, password: str = "default_password") -> dict:
        """
        Decrypt hardware data.
        
        Args:
            encrypted_data: Base64 encoded encrypted data
            password: Password for decryption
            
        Returns:
            dict: Decrypted hardware information
        """
        try:
            # Generate decryption key
            key = self._generate_key(password)
            cipher = Fernet(key)
            
            # Decode and decrypt
            decoded_data = base64.b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = cipher.decrypt(decoded_data)
            
            return json.loads(decrypted_data.decode('utf-8'))
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")
    
    def compare_hardware(self, original_data: dict, current_data: dict) -> dict:
        """
        Compare original hardware data with current hardware data.
        
        Args:
            original_data: Original hardware information
            current_data: Current hardware information
            
        Returns:
            dict: Comparison results showing changes
        """
        comparison = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "unchanged",
            "changes_detected": [],
            "warnings": [],
            "permanent_components_status": "intact",
            "changeable_components_changes": []
        }
        
        # Check permanent components (these should NEVER change)
        original_permanent = original_data.get("permanent_components", {})
        current_permanent = current_data.get("permanent_components", {})
        
        for key, original_value in original_permanent.items():
            if key == "error":
                continue
            current_value = current_permanent.get(key)
            if original_value != current_value and original_value is not None:
                comparison["changes_detected"].append({
                    "component": "permanent",
                    "field": key,
                    "original": original_value,
                    "current": current_value,
                    "severity": "critical",
                    "message": f"Critical: Permanent component '{key}' has changed!"
                })
                comparison["permanent_components_status"] = "compromised"
                comparison["overall_status"] = "changed"
        
        # Check changeable components
        original_changeable = original_data.get("changeable_components", {})
        current_changeable = current_data.get("changeable_components", {})
        
        for component_type in self.CHANGEABLE_COMPONENTS:
            original_component = original_changeable.get(component_type, {})
            current_component = current_changeable.get(component_type, {})
            
            # Skip if error in data
            if isinstance(original_component, dict) and "error" in original_component:
                continue
            if isinstance(current_component, dict) and "error" in current_component:
                continue
            
            # Compare components
            changes = self._compare_component(component_type, original_component, current_component)
            if changes:
                comparison["changeable_components_changes"].extend(changes)
                comparison["overall_status"] = "changed"
        
        # Add summary
        comparison["summary"] = {
            "total_changes": len(comparison["changes_detected"]) + len(comparison["changeable_components_changes"]),
            "critical_changes": len(comparison["changes_detected"]),
            "component_changes": len(comparison["changeable_components_changes"])
        }
        
        return comparison
    
    def _compare_component(self, component_type: str, original: any, current: any) -> list:
        """Compare individual component data"""
        changes = []
        
        # Handle list comparisons (e.g., multiple GPUs, RAM modules)
        if isinstance(original, list) and isinstance(current, list):
            if len(original) != len(current):
                changes.append({
                    "component": component_type,
                    "field": "count",
                    "original": len(original),
                    "current": len(current),
                    "severity": "medium",
                    "message": f"{component_type} count changed from {len(original)} to {len(current)}"
                })
            
            # Compare individual items
            for i, (orig_item, curr_item) in enumerate(zip(original, current)):
                if isinstance(orig_item, dict) and isinstance(curr_item, dict):
                    for key in orig_item:
                        if key in ["error", "driver_version"]:  # Skip certain fields
                            continue
                        if orig_item.get(key) != curr_item.get(key):
                            changes.append({
                                "component": f"{component_type}[{i}]",
                                "field": key,
                                "original": orig_item.get(key),
                                "current": curr_item.get(key),
                                "severity": "low",
                                "message": f"{component_type} {key} changed"
                            })
        
        # Handle dictionary comparisons
        elif isinstance(original, dict) and isinstance(current, dict):
            for key in original:
                if key in ["error", "current_clock_speed", "driver_version"]:  # Skip dynamic fields
                    continue
                if original.get(key) != current.get(key):
                    changes.append({
                        "component": component_type,
                        "field": key,
                        "original": original.get(key),
                        "current": current.get(key),
                        "severity": "low",
                        "message": f"{component_type} {key} changed"
                    })
        
        return changes
    
    def create_hardware_hash_file(self, output_path: str, password: str = "default_password") -> dict:
        """
        Create an encrypted, read-only hardware hash file.
        
        Args:
            output_path: Path where the hash file should be saved
            password: Password for encryption
            
        Returns:
            dict: Status and file information
        """
        try:
            # Extract hardware information
            hardware_data = self.extract_hardware_info()
            
            # Generate hash
            hardware_hash = self.generate_hardware_hash(hardware_data)
            hardware_data["hardware_hash"] = hardware_hash
            
            # Encrypt data
            encrypted_data = self.encrypt_hardware_data(hardware_data, password)
            
            # Create file package
            file_package = {
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "encrypted_data": encrypted_data,
                "hash": hardware_hash,
                "metadata": {
                    "platform": hardware_data["platform"],
                    "hostname": hardware_data["metadata"]["hostname"],
                    "generation_timestamp": hardware_data["timestamp"]
                }
            }
            
            # Write to file
            with open(output_path, 'w') as f:
                json.dump(file_package, f, indent=2)
            
            # Make file read-only
            os.chmod(output_path, 0o444)  # Read-only for all users
            
            return {
                "success": True,
                "file_path": output_path,
                "file_size": os.path.getsize(output_path),
                "hardware_hash": hardware_hash,
                "created": file_package["created"],
                "components_captured": {
                    "permanent": len(hardware_data["permanent_components"]),
                    "changeable": len(hardware_data["changeable_components"])
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_hardware_hash_file(self, file_path: str, password: str = "default_password") -> dict:
        """
        Analyze a hardware hash file and compare with current hardware.
        
        Args:
            file_path: Path to the hardware hash file
            password: Password for decryption
            
        Returns:
            dict: Analysis results showing any changes
        """
        try:
            # Read the file
            with open(file_path, 'r') as f:
                file_package = json.load(f)
            
            # Decrypt original data
            encrypted_data = file_package.get("encrypted_data")
            original_hardware_data = self.decrypt_hardware_data(encrypted_data, password)
            
            # Get current hardware data
            current_hardware_data = self.extract_hardware_info()
            
            # Compare
            comparison = self.compare_hardware(original_hardware_data, current_hardware_data)
            
            # Add file metadata
            comparison["file_info"] = {
                "version": file_package.get("version"),
                "created": file_package.get("created"),
                "original_hash": file_package.get("hash"),
                "current_hash": self.generate_hardware_hash(current_hardware_data)
            }
            
            return {
                "success": True,
                "comparison": comparison,
                "original_data": original_hardware_data,
                "current_data": current_hardware_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
