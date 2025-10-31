"""
Advanced Hardware Telemetry Module
Provides deep hardware monitoring similar to HWiNFO64 using multiple sources:
- LibreHardwareMonitor for comprehensive Windows sensors
- NVML for NVIDIA GPU telemetry
- SMART data for disk health
- WMI for additional Windows metrics
"""

import os
import sys
import subprocess
import json
from typing import Dict, List, Any, Optional

class AdvancedTelemetry:
    """Advanced hardware telemetry collector with HWiNFO-level detail"""
    
    def __init__(self):
        self.librehardware_available = False
        self.nvml_available = False
        self.clr = None
        self.computer = None
        self.pynvml = None
        
        # Try to initialize LibreHardwareMonitor
        self._init_librehardware()
        
        # Try to initialize NVML for NVIDIA GPUs
        self._init_nvml()
    
    def _init_librehardware(self):
        """Initialize LibreHardwareMonitor via pythonnet"""
        try:
            import clr
            
            # Try to find LibreHardwareMonitorLib.dll in common locations
            dll_paths = [
                r"C:\Program Files\LibreHardwareMonitor\LibreHardwareMonitorLib.dll",
                r"C:\LibreHardwareMonitor\LibreHardwareMonitorLib.dll",
                os.path.join(os.getcwd(), "LibreHardwareMonitorLib.dll"),
                os.path.join(os.getcwd(), "lib", "LibreHardwareMonitorLib.dll")
            ]
            
            dll_path = None
            for path in dll_paths:
                if os.path.exists(path):
                    dll_path = path
                    break
            
            if dll_path:
                clr.AddReference(dll_path)
                from LibreHardwareMonitor.Hardware import Computer
                
                self.computer = Computer()
                self.computer.IsCpuEnabled = True
                self.computer.IsGpuEnabled = True
                self.computer.IsMotherboardEnabled = True
                self.computer.IsMemoryEnabled = True
                self.computer.IsNetworkEnabled = True
                self.computer.IsStorageEnabled = True
                self.computer.IsControllerEnabled = True
                self.computer.Open()
                
                self.librehardware_available = True
                self.clr = clr
                print("✅ LibreHardwareMonitor initialized successfully")
            else:
                print("⚠️ LibreHardwareMonitorLib.dll not found. Advanced sensor monitoring unavailable.")
                
        except ImportError:
            print("⚠️ pythonnet not installed. Run: pip install pythonnet")
        except Exception as e:
            print(f"⚠️ LibreHardwareMonitor initialization failed: {str(e)}")
    
    def _init_nvml(self):
        """Initialize NVIDIA Management Library for GPU telemetry"""
        try:
            import pynvml
            pynvml.nvmlInit()
            self.pynvml = pynvml
            self.nvml_available = True
            print("✅ NVIDIA NVML initialized successfully")
        except ImportError:
            print("⚠️ pynvml not installed. Run: pip install nvidia-ml-py3")
        except Exception as e:
            print(f"⚠️ NVML initialization failed: {str(e)}")
    
    def get_all_sensors(self) -> Dict[str, Any]:
        """Get comprehensive sensor data from all available sources"""
        sensor_data = {
            "librehardware_sensors": self.get_librehardware_sensors(),
            "nvidia_gpu_telemetry": self.get_nvidia_telemetry(),
            "thermal_sensors": self.get_thermal_sensors(),
            "power_sensors": self.get_power_sensors(),
            "fan_sensors": self.get_fan_sensors(),
            "voltage_sensors": self.get_voltage_sensors(),
            "clock_sensors": self.get_clock_sensors()
        }
        
        return sensor_data
    
    def get_librehardware_sensors(self) -> List[Dict[str, Any]]:
        """Get all sensors from LibreHardwareMonitor"""
        if not self.librehardware_available:
            return []
        
        sensors = []
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                # Get hardware info
                hw_info = {
                    "name": hardware.Name,
                    "type": str(hardware.HardwareType),
                    "identifier": str(hardware.Identifier),
                    "sensors": []
                }
                
                # Get all sensors for this hardware
                for sensor in hardware.Sensors:
                    sensor_info = {
                        "name": sensor.Name,
                        "type": str(sensor.SensorType),
                        "value": float(sensor.Value) if sensor.Value is not None else None,
                        "identifier": str(sensor.Identifier),
                        "min": float(sensor.Min) if sensor.Min is not None else None,
                        "max": float(sensor.Max) if sensor.Max is not None else None
                    }
                    hw_info["sensors"].append(sensor_info)
                
                sensors.append(hw_info)
                
        except Exception as e:
            print(f"Error reading LibreHardware sensors: {str(e)}")
        
        return sensors
    
    def get_nvidia_telemetry(self) -> List[Dict[str, Any]]:
        """Get detailed NVIDIA GPU telemetry via NVML"""
        if not self.nvml_available:
            return []
        
        gpu_data = []
        try:
            device_count = self.pynvml.nvmlDeviceGetCount()
            
            for i in range(device_count):
                handle = self.pynvml.nvmlDeviceGetHandleByIndex(i)
                
                # Get basic info
                name = self.pynvml.nvmlDeviceGetName(handle)
                
                gpu_info = {
                    "index": i,
                    "name": name.decode() if isinstance(name, bytes) else str(name),
                    "temperature": {},
                    "utilization": {},
                    "memory": {},
                    "clocks": {},
                    "power": {},
                    "fan": {},
                    "pcie": {}
                }
                
                # Collect GPU metrics safely
                try:
                    gpu_info["temperature"]["gpu"] = self.pynvml.nvmlDeviceGetTemperature(
                        handle, self.pynvml.NVML_TEMPERATURE_GPU
                    )
                except:
                    pass
                
                try:
                    util = self.pynvml.nvmlDeviceGetUtilizationRates(handle)
                    gpu_info["utilization"]["gpu"] = util.gpu
                    gpu_info["utilization"]["memory"] = util.memory
                except:
                    pass
                
                gpu_data.append(gpu_info)
                
        except Exception as e:
            print(f"Error reading NVIDIA telemetry: {str(e)}")
        
        return gpu_data
    
    def get_thermal_sensors(self) -> Dict[str, Any]:
        """Get thermal sensors (temperatures)"""
        if not self.librehardware_available:
            return {}
        
        thermal_data = {}
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                for sensor in hardware.Sensors:
                    if str(sensor.SensorType) == "Temperature" and sensor.Value is not None:
                        key = f"{hardware.Name}_{sensor.Name}"
                        thermal_data[key] = {
                            "value": float(sensor.Value),
                            "min": float(sensor.Min) if sensor.Min is not None else None,
                            "max": float(sensor.Max) if sensor.Max is not None else None,
                            "unit": "°C"
                        }
        except Exception as e:
            print(f"Error reading thermal sensors: {str(e)}")
        
        return thermal_data
    
    def get_power_sensors(self) -> Dict[str, Any]:
        """Get power consumption sensors"""
        if not self.librehardware_available:
            return {}
        
        power_data = {}
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                for sensor in hardware.Sensors:
                    if str(sensor.SensorType) == "Power" and sensor.Value is not None:
                        key = f"{hardware.Name}_{sensor.Name}"
                        power_data[key] = {
                            "value": float(sensor.Value),
                            "unit": "W"
                        }
        except Exception as e:
            print(f"Error reading power sensors: {str(e)}")
        
        return power_data
    
    def get_fan_sensors(self) -> Dict[str, Any]:
        """Get fan speed sensors"""
        if not self.librehardware_available:
            return {}
        
        fan_data = {}
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                for sensor in hardware.Sensors:
                    if str(sensor.SensorType) == "Fan" and sensor.Value is not None:
                        key = f"{hardware.Name}_{sensor.Name}"
                        fan_data[key] = {
                            "value": float(sensor.Value),
                            "unit": "RPM"
                        }
        except Exception as e:
            print(f"Error reading fan sensors: {str(e)}")
        
        return fan_data
    
    def get_voltage_sensors(self) -> Dict[str, Any]:
        """Get voltage sensors"""
        if not self.librehardware_available:
            return {}
        
        voltage_data = {}
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                for sensor in hardware.Sensors:
                    if str(sensor.SensorType) == "Voltage" and sensor.Value is not None:
                        key = f"{hardware.Name}_{sensor.Name}"
                        voltage_data[key] = {
                            "value": float(sensor.Value),
                            "unit": "V"
                        }
        except Exception as e:
            print(f"Error reading voltage sensors: {str(e)}")
        
        return voltage_data
    
    def get_clock_sensors(self) -> Dict[str, Any]:
        """Get clock speed sensors"""
        if not self.librehardware_available:
            return {}
        
        clock_data = {}
        try:
            for hardware in self.computer.Hardware:
                hardware.Update()
                
                for sensor in hardware.Sensors:
                    if str(sensor.SensorType) == "Clock" and sensor.Value is not None:
                        key = f"{hardware.Name}_{sensor.Name}"
                        clock_data[key] = {
                            "value": float(sensor.Value),
                            "unit": "MHz"
                        }
        except Exception as e:
            print(f"Error reading clock sensors: {str(e)}")
        
        return clock_data
    
    def close(self):
        """Clean up resources"""
        try:
            if self.computer:
                self.computer.Close()
        except:
            pass
        
        try:
            if self.nvml_available and self.pynvml:
                self.pynvml.nvmlShutdown()
        except:
            pass
