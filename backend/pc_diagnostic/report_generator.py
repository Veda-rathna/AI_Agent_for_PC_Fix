import json
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self, reports_folder='reports'):
        self.reports_folder = reports_folder
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)

    def generate_json_report(self, user_issue, telemetry_data, ai_analysis, session_id=None):
        """Generate a JSON report for programmatic access"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pc_diagnosis_data_{timestamp}.json"
        filepath = os.path.join(self.reports_folder, filename)
        
        report_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "session_id": session_id,
                "user_issue": user_issue,
                "issue_types_detected": telemetry_data.get('issue_types_detected', []),
                "report_type": "pc_diagnosis"
            },
            "ai_analysis": ai_analysis,
            "telemetry_data": telemetry_data,
            "summary": self._generate_summary(telemetry_data)
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return filename, filepath

    def _generate_summary(self, telemetry_data):
        """Generate a summary of key metrics"""
        summary = {}
        
        # System summary
        system_info = telemetry_data.get('system_info', {})
        summary['system'] = {
            "platform": system_info.get('platform', 'Unknown'),
            "uptime_hours": round(system_info.get('uptime_seconds', 0) / 3600, 2)
        }
        
        # Performance summary
        cpu_info = telemetry_data.get('cpu', {})
        memory_info = telemetry_data.get('memory', {})
        summary['performance'] = {
            "cpu_usage_percent": cpu_info.get('total_usage', 0),
            "memory_usage_percent": memory_info.get('percentage', 0),
            "cpu_cores": cpu_info.get('total_cores', 0),
            "memory_total_gb": round(memory_info.get('total', 0) / (1024**3), 2)
        }
        
        # Issue-specific summary
        issue_specific = telemetry_data.get('issue_specific', {})
        summary['issue_specific_detected'] = list(issue_specific.keys())
        
        return summary

    def get_available_reports(self):
        """Get list of available reports in the reports folder"""
        reports = []
        if os.path.exists(self.reports_folder):
            for filename in os.listdir(self.reports_folder):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.reports_folder, filename)
                    reports.append({
                        'filename': filename,
                        'filepath': filepath,
                        'size': os.path.getsize(filepath),
                        'created': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat()
                    })
        return sorted(reports, key=lambda x: x['created'], reverse=True)
