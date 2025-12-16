# 🖥️ AI-Driven PC Diagnostic Assistant

An intelligent, full-stack application that leverages AI and AutoGen agents to diagnose PC issues through natural conversation. Built with Django REST Framework backend and React frontend, this system provides comprehensive hardware monitoring, multi-agent diagnostics, and automated report generation.

## 🌟 Overview

The AI-Driven PC Diagnostic Assistant is designed to help users troubleshoot computer problems through an interactive chat interface. The system automatically collects system telemetry, analyzes issues using AI-powered agents, and provides actionable diagnostic recommendations.

### Key Highlights

- **🤖 Multi-Agent AI System**: Uses AutoGen framework with specialized diagnostic agents (Hardware Specialist, OS Specialist, Network Specialist, Software Specialist)
- **📊 Real-Time Hardware Monitoring**: Comprehensive telemetry collection (CPU, memory, disk, network, GPU)
- **💬 Conversational Interface**: Chat-based UI with streaming responses and visual task tracking
- **📄 Automated Reports**: Generate detailed diagnostic reports in JSON format
- **🔒 Hardware Fingerprinting**: Unique device identification for tracking diagnostic history
- **🌐 RESTful API**: Well-documented endpoints for diagnostics, telemetry, and reports

## 🏗️ Architecture

```
AI_Agent_for_PC_Fix/
├── backend/                      # Django REST API
│   ├── pc_diagnostic/           # Main Django project
│   │   ├── settings.py          # Configuration
│   │   ├── urls.py              # API routing
│   │   ├── hardware_monitor.py  # System telemetry collection
│   │   ├── advanced_telemetry.py # GPU & sensor monitoring
│   │   ├── report_generator.py  # Diagnostic report generation
│   │   ├── hardware_hash.py     # Device fingerprinting
│   │   └── streaming_views.py   # Real-time streaming endpoints
│   ├── ai_diagnostic/           # Diagnostic API app
│   │   ├── views.py             # Basic diagnostic endpoints
│   │   ├── conversation_views.py # Streaming conversation logic
│   │   ├── models.py            # Database models
│   │   └── serializers.py       # API serializers
│   └── autogen_integration/     # AutoGen multi-agent system
│       ├── orchestrator.py      # Agent coordination
│       ├── agents/              # Specialized diagnostic agents
│       ├── tools/               # System interaction tools
│       └── parsers/             # Output parsing utilities
├── frontend/                     # React SPA
│   ├── src/
│   │   ├── App.js               # Main application
│   │   ├── components/          # Reusable UI components
│   │   └── pages/               # Page components
│   └── build/                   # Production build
└── reports/                      # Generated diagnostic reports
```

## ✨ Features

### Core Capabilities

- **🔍 Intelligent Diagnostics**: Multi-agent AI system analyzes issues from different perspectives (hardware, OS, network, software)
- **📈 System Telemetry**: Automatic collection of:
  - CPU usage, frequencies, and core statistics
  - Memory utilization and swap information
  - Disk usage across all partitions
  - Network I/O, adapters, and connectivity
  - GPU information (NVIDIA support)
  - Running processes and resource consumption
  - Temperature and fan speeds (with advanced telemetry)
  
- **💡 Issue Detection**: Automatically identifies issue categories:
  - Display/Video problems
  - Performance issues
  - Network connectivity
  - Audio problems
  - Storage issues
  - General hardware failures

- **📊 Visual Task Tracking**: Real-time display of agent activities and progress
- **🔄 Streaming Responses**: Live AI analysis with token-by-token streaming
- **📝 Diagnostic Reports**: Comprehensive JSON reports with all findings and recommendations
- **🎯 Context-Aware**: Maintains conversation history for better diagnostics

### Advanced Features

- **Hardware Fingerprinting**: Generate unique device IDs for tracking
- **Offline Mode**: Fallback diagnostics when AI services are unavailable
- **CORS Enabled**: Ready for local development and deployment
- **Modular Design**: Easy to extend with new agents or tools

## 🚀 Quick Start

### Prerequisites

- **Python** 3.8+ (3.11 recommended)
- **Node.js** 14+ and npm
- **Windows OS** (for full hardware monitoring features)
- **Git** for cloning the repository

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Veda-rathna/AI_Agent_for_PC_Fix.git
   cd AI_Agent_for_PC_Fix
   ```

2. **Set up the backend**
   ```powershell
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   ```

3. **Configure environment variables** (optional for AI features)
   Create a `.env` file in the `backend` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Set up the frontend**
   ```powershell
   cd ../frontend
   npm install
   ```

### Running the Application

1. **Start the Django backend** (Terminal 1):
   ```powershell
   cd backend
   python manage.py runserver
   ```
   Backend runs at `http://localhost:8000`

2. **Start the React frontend** (Terminal 2):
   ```powershell
   cd frontend
   npm start
   ```
   Frontend runs at `http://localhost:3000`

3. **Access the application**:
   Open your browser and navigate to `http://localhost:3000`

### Testing the System

1. Type a PC issue in the chat interface (e.g., "My computer is running slow")
2. Watch as the AI agents analyze your system
3. View real-time task progress and diagnostic recommendations
4. Download generated reports for detailed analysis

## 📡 API Documentation

### Core Endpoints

#### 1. **POST /api/predict/**
Main diagnostic endpoint with AI analysis and telemetry collection.

**Request:**
```json
{
  "query": "My computer is running slow",
  "issue_type": "performance",
  "generate_report": true,
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "query": "My computer is running slow",
  "analysis": "Detailed AI analysis...",
  "telemetry_summary": {
    "cpu_usage": 45.2,
    "memory_usage": 67.8,
    "disk_usage": 82.1
  },
  "session_id": "unique-session-id",
  "report_path": "reports/report_2025-12-16_123456.json"
}
```

#### 2. **GET /api/stream-conversation/**
Streaming endpoint for real-time AI responses.

**Query Parameters:**
- `query`: User's diagnostic query
- `issue_type`: (Optional) Issue category

**Response:** Server-Sent Events (SSE) stream with:
- Task updates
- Diagnostic steps
- AI analysis tokens
- Completion status

#### 3. **GET /api/telemetry/**
Retrieve current system telemetry without AI analysis.

**Query Parameters:**
- `issue_type`: (Optional) Specific issue category

**Response:**
```json
{
  "system_info": {...},
  "cpu": {...},
  "memory": {...},
  "disk": {...},
  "network": {...}
}
```

#### 4. **GET /api/reports/**
List all generated diagnostic reports.

**Response:**
```json
{
  "reports": [
    {
      "filename": "report_2025-12-16_123456.json",
      "size": "45.2 KB",
      "created": "2025-12-16 12:34:56"
    }
  ]
}
```

#### 5. **GET /api/download_report/<filename>/**
Download a specific diagnostic report.

#### 6. **GET /api/hardware-hash/**
Generate unique hardware fingerprint for device identification.

**Response:**
```json
{
  "hardware_hash": "a1b2c3d4e5f6...",
  "hash_components": {
    "cpu_id": "...",
    "motherboard_id": "...",
    "disk_serial": "..."
  }
}
```

## 🛠️ Technology Stack

### Backend
- **Django** 4.2.7 - Web framework
- **Django REST Framework** 3.15.2 - API development
- **AutoGen** - Multi-agent AI orchestration
- **psutil** 5.9.6 - System monitoring
- **GPUtil** 1.4.0 - GPU monitoring
- **WMI** 1.5.1 - Windows Management Instrumentation
- **django-cors-headers** 4.8.0 - CORS handling
- **OpenAI API** - LLM integration (GPT-4)
- **Groq API** - Alternative LLM provider

### Frontend
- **React** 18 - UI framework
- **Axios** - HTTP client
- **CSS3** - Styling with animations
- **Server-Sent Events** - Real-time streaming

### AI/ML Components
- **AutoGen Framework** - Multi-agent coordination
- **LangChain** - LLM application framework
- **OpenAI GPT-4** - Primary language model
- **Groq Llama** - Alternative fast inference

## 🤖 AutoGen Multi-Agent System

The diagnostic system uses specialized AI agents that collaborate to solve PC issues:

### Agent Types

1. **🔧 Hardware Specialist Agent**
   - Analyzes CPU, RAM, GPU, and storage issues
   - Interprets system telemetry data
   - Provides hardware upgrade recommendations

2. **🖥️ OS Specialist Agent**
   - Diagnoses Windows-specific issues
   - Registry and system file analysis
   - Driver and update recommendations

3. **🌐 Network Specialist Agent**
   - Network connectivity troubleshooting
   - DNS and routing diagnostics
   - Firewall and security analysis

4. **💻 Software Specialist Agent**
   - Application conflicts and crashes
   - Software compatibility issues
   - Performance optimization

### Orchestration

The `orchestrator.py` coordinates agent interactions:
- **Sequential Analysis**: Each agent provides focused expertise
- **Context Sharing**: Agents build on previous findings
- **Synthesis**: Final recommendations combine all insights
- **Tool Access**: Agents can execute system commands and collect data

## 📂 Project Structure Details

### Backend Modules

- **`hardware_monitor.py`**: Core telemetry collection
- **`advanced_telemetry.py`**: GPU and sensor monitoring (optional)
- **`report_generator.py`**: JSON report creation and management
- **`hardware_hash.py`**: Device fingerprinting
- **`streaming_views.py`**: SSE streaming endpoints
- **`mcp_views.py`**: Model Context Protocol integration

### Frontend Components

- **`src/App.js`**: Main application shell
- **`src/components/`**: Reusable UI components
  - ChatMessage
  - TaskDisplay
  - LoadingIndicator
  - ReportDownloader
- **`src/pages/`**: Route-based pages

## ⚙️ Configuration

### Django Settings

Edit `backend/pc_diagnostic/settings.py`:

```python
# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
```

### AutoGen Configuration

Configure AI models in `backend/autogen_integration/config/`:

```python
# config/llm_config.py
LLM_CONFIG = {
    "model": "gpt-4",
    "api_key": os.getenv("OPENAI_API_KEY"),
    "temperature": 0.7,
    "max_tokens": 2000
}
```

### Frontend API URL

Update API endpoint in `frontend/src/App.js`:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

## 🔧 Development

### Adding New Diagnostic Agents

1. Create a new agent in `backend/autogen_integration/agents/`:

```python
# agents/custom_agent.py
from autogen import AssistantAgent

def create_custom_agent(llm_config):
    return AssistantAgent(
        name="CustomSpecialist",
        system_message="You are a specialist in...",
        llm_config=llm_config
    )
```

2. Register the agent in `orchestrator.py`:

```python
from agents.custom_agent import create_custom_agent

# In create_agents()
custom_agent = create_custom_agent(llm_config)
agents.append(custom_agent)
```

### Adding New Telemetry Metrics

Extend `hardware_monitor.py`:

```python
def collect_custom_metrics():
    """Collect custom system metrics"""
    return {
        "custom_metric": get_custom_data(),
        # Add more metrics
    }
```

### Customizing the UI

- **Styling**: Modify `frontend/src/App.css` or `typography.css`
- **Components**: Add new components in `frontend/src/components/`
- **Themes**: Update color schemes in CSS variables

### Running Tests

```powershell
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

## 🐛 Troubleshooting

### Common Backend Issues

**Issue**: `Module not found: autogen`
```powershell
pip install pyautogen
```

**Issue**: `Port 8000 already in use`
```powershell
python manage.py runserver 8001
```

**Issue**: `WMI not working`
- Ensure you're running on Windows
- Install: `pip install wmi pywin32`

**Issue**: `OpenAI API errors`
- Check your API key in environment variables
- Verify API quota and billing

### Common Frontend Issues

**Issue**: `CORS error`
- Ensure backend is running on port 8000
- Verify CORS settings in `settings.py`

**Issue**: `Cannot connect to API`
- Check that Django server is running
- Verify API_BASE_URL in frontend code

**Issue**: `Streaming not working`
- Check browser console for EventSource errors
- Ensure proper SSE headers in backend

### Performance Optimization

**High Memory Usage**:
- Limit telemetry collection frequency
- Reduce AutoGen agent count
- Implement caching for repeated queries

**Slow AI Responses**:
- Use Groq API for faster inference
- Reduce max_tokens in LLM config
- Implement response streaming

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in Django settings
- [ ] Configure production database (PostgreSQL recommended)
- [ ] Set up environment variables securely
- [ ] Configure static file serving
- [ ] Build React production bundle: `npm run build`
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure domain and DNS
- [ ] Set up monitoring and logging
- [ ] Implement rate limiting
- [ ] Configure backup system for reports

### Deployment Options

**Option 1: Traditional Hosting**
- Deploy Django on a VPS (DigitalOcean, Linode, AWS EC2)
- Serve React build with Nginx
- Use Gunicorn as WSGI server
- PostgreSQL for production database

**Option 2: Platform as a Service**
- Backend: Heroku, Railway, Render
- Frontend: Vercel, Netlify
- Database: Heroku Postgres, Supabase

**Option 3: Containerization**
- Docker containers for backend and frontend
- Docker Compose for local orchestration
- Deploy to AWS ECS, Google Cloud Run, or Azure

### Cloudflare Tunnel Setup

For secure remote access, see `backend/CLOUDFLARE_TUNNEL_GUIDE.md` for:
- Tunnel installation
- Configuration for backend/frontend
- DNS setup
- Security best practices

## 📊 Monitoring & Logs

### Backend Logs

AutoGen logs are stored in `backend/autogen_integration/logs/`:
- `autogen_integration.log`: Agent conversations
- `error.log`: Error tracking

View real-time logs:
```powershell
tail -f backend/autogen_integration/logs/autogen_integration.log
```

### Diagnostic Reports

Reports are saved in `backend/reports/` as JSON files:
- Full telemetry snapshots
- AI analysis results
- Timestamps and session IDs
- User queries and responses

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and commit: `git commit -m 'Add amazing feature'`
4. **Push to your fork**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AutoGen** team for the multi-agent framework
- **OpenAI** for GPT models
- **Groq** for fast inference capabilities
- **Django** and **React** communities
- All contributors and testers

## 📧 Contact & Support

- **Author**: Veda-rathna
- **Repository**: [github.com/Veda-rathna/AI_Agent_for_PC_Fix](https://github.com/Veda-rathna/AI_Agent_for_PC_Fix)
- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/Veda-rathna/AI_Agent_for_PC_Fix/issues)

## 🗺️ Roadmap

### Planned Features

- [ ] **User Authentication**: Multi-user support with diagnostic history
- [ ] **Database Integration**: Store diagnostics in PostgreSQL/MongoDB
- [ ] **Mobile App**: React Native companion app
- [ ] **PDF Reports**: Generate printable diagnostic reports
- [ ] **Real-time Monitoring**: Live system health dashboard
- [ ] **Community Solutions**: Share and vote on fixes
- [ ] **ML Predictions**: Predict failures before they occur
- [ ] **Multi-language Support**: Internationalization
- [ ] **Plugin System**: Extensible diagnostic modules
- [ ] **Cloud Sync**: Backup diagnostic history to cloud

### Version History

- **v1.0.0** - Initial release with basic diagnostics
- **v1.5.0** - Added AutoGen multi-agent system
- **v2.0.0** - Streaming responses and visual task tracking
- **v2.1.0** - Hardware fingerprinting and advanced telemetry

---

<div align="center">
  
**⭐ If you find this project helpful, please star it on GitHub! ⭐**

Made with ❤️ by the AI-Driven PC Diagnostic Assistant team

</div>
