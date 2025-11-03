# 🚀 API Discovery Suite

AI-Powered API Testing & Discovery Platform with intelligent test case generation and comprehensive API analysis.

## 🌟 Features

### 🔍 **API Discovery**
- **Automatic API Detection** - Discover all APIs from New Relic monitoring data
- **Performance Analytics** - Real-time response times, error rates, and throughput analysis
- **Dependency Mapping** - Visual topology maps of your API ecosystem
- **Health Monitoring** - Continuous API status tracking
- **New Relic Integration** - Seamless connection with existing monitoring setup

### 📝 **PRD Test Case Generation**
- **Document Upload** - Support for PDF, DOC, DOCX, TXT formats
- **Azure DevOps Integration** - Sync with Epics and User Stories
- **AI-Powered Analysis** - Extract testable scenarios from requirements
- **Comprehensive Test Coverage** - Functional, edge case, integration, and E2E tests
- **Traceability Mapping** - Link tests back to requirements

### 🧪 **API Component Test Generation**
- **Swagger/OpenAPI Integration** - Import specifications automatically
- **Manual Test Creation** - Build custom test suites with full control
- **Multi-Framework Support** - Generate tests for various testing frameworks
- **Parameter Configuration** - Advanced test data and header management
- **Script Generation** - Export tests in multiple formats

## 🎯 Quick Start

### Prerequisites
- Node.js (v14 or higher)
- Python 3.8+ (for backend)
- New Relic account (for API discovery)
- Azure DevOps account (optional, for PRD integration)

### Installation

1. **Clone the repository**
   ```bash

   ```

2. **Install dependencies**
   ```bash

   # Backend dependencies
   python3 --version
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```

3. **Required Environment Variables**
   ```env
   # Google Gemini AI Configuration
   GOOGLE_API_KEY=your_google_api_key_here

   # New Relic Configuration
   NEWRELIC_API_KEY=your_newrelic_api_key
   NEWRELIC_ACCOUNT_ID=your_account_id

   # Azure DevOps (Optional)
   AZURE_DEVOPS_TOKEN=your_azure_token
   AZURE_ORGANIZATION=your_org_name

   # Application Settings
   PORT=5000
   DEBUG=true
   ```

5. **Start the application**
   ```bash
   # Start backend server
   python app.py
   ```

6. **Access the application**
   ```
   http://localhost:5000/ai
   ```

## 📋 Usage Guide

### 🔍 API Discovery

1. **Click "Launch LLM Discovery"** on the main page
2. **Connect your New Relic account**
   - Enter your New Relic API key
   - Select account region
   - Test connection
3. **Choose applications to scan**
   - Select monitored applications
   - Set time range for analysis
   - Configure discovery scope
4. **Add Swagger documentation** (optional)
   - Provide Swagger/OpenAPI URLs
   - Improve AI analysis accuracy
5. **Start AI analysis**
   - Click "Analyze & Discover APIs"
   - Wait 2-5 minutes for completion
6. **Review your API inventory**
   - Browse discovered endpoints
   - Check performance metrics
   - Explore dependency maps

### 📝 PRD Test Case Generation

#### Method 1: Upload PRD Document
1. **Click "PRD Test Case Generation"**
2. **Select "Upload PRD Document"**
3. **Choose your file** (PDF, DOC, DOCX, TXT)
4. **Click "Generate Test Cases"**
5. **Review and download results**

#### Method 2: Azure DevOps Integration
1. **Click "PRD Test Case Generation"**
2. **Select "Epic/User Story"**
3. **Enter Azure Token**
4. **Add Epic Number** (optional) and **User Story Numbers**
5. **Confirm details** and **generate test cases**

### 🧪 API Component Test Generation

#### Manual Test Creation
1. **Click "API Test Generation"**
2. **Select "Manual API Test Generation"**
3. **Enter API endpoint details**
4. **Configure parameters and data**
5. **Generate test scripts**

#### Swagger Integration
1. **Click "API Test Generation"**
2. **Select "Swagger API Test Generation"**
3. **Enter Swagger URL and endpoint**
4. **Fetch API specifications**
5. **Generate comprehensive test cases**

## 🤖 AI Assistant

The platform includes an intelligent AI assistant that can help with:

- **Feature explanations** - Learn about platform capabilities
- **Setup guidance** - Step-by-step configuration help
- **Troubleshooting** - Common issues and solutions
- **Best practices** - Optimization tips and recommendations

### Sample Questions:
- "How to generate PRD test case"
- "What is API Discovery"
- "How to generate API Component test"
- "How to connect New Relic"
- "What are your pricing plans"

## 🛠️ Technology Stack

### Frontend
- **HTML5/CSS3** - Modern responsive design
- **JavaScript ES6+** - Interactive user experience
- **CSS Animations** - Smooth transitions and effects
- **Responsive Design** - Mobile and desktop compatibility

### Backend
- **Python/Flask** - REST API server
- **Google AI/Gemini** - LLM integration for intelligent analysis
- **New Relic API** - Monitoring data integration
- **Azure DevOps API** - Work item synchronization

### AI/ML
- **Google Gemini Pro** - Advanced language model
- **Natural Language Processing** - Requirement analysis
- **Pattern Recognition** - API endpoint detection
- **Intelligent Parsing** - Document content extraction

## 🔧 Configuration

### New Relic Setup
1. Go to New Relic → Account Settings → API Keys
2. Create a new API key with appropriate permissions
3. Add the key to your `.env` file

### Azure DevOps Setup
1. Go to Azure DevOps → User Settings → Personal Access Tokens
2. Create token with Work Items (Read) permissions
3. Add token and organization name to `.env`

### Google AI Setup
1. Visit Google AI Studio
2. Create a new API key
3. Add the key to your `.env` file

## 🚀 Deployment


## 📊 API Endpoints

### Core APIs
- `GET /` - Main application interface
- `POST /contact-llm` - Generate API test cases
- `POST /contact-testCase-llm` - Generate PRD test cases
- `POST /chat-box-llm` - AI assistant chat
- `POST /get-api-info` - Swagger API information
- `GET /get-available-prompts` - Available test prompts

### Integration APIs
- `POST /api/workitems` - Azure DevOps work item validation
- `POST /api/workitemsDetails` - Fetch work item details
- `POST /upload/raw` - Document upload processing
- `GET /llmapidiscovery` - API discovery interface


## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Add tests** for new functionality
5. **Commit your changes**
   ```bash
   git commit -m "Add: your feature description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request**


## 📋 Troubleshooting

### Common Issues

#### New Relic Connection Failed
- **Check API key permissions** - Ensure key has monitoring data access
- **Verify account ID** - Confirm correct New Relic account
- **Network connectivity** - Test API endpoint accessibility

#### PRD Upload Issues
- **File size limit** - Maximum 10MB per document
- **Supported formats** - PDF, DOC, DOCX, TXT only
- **File corruption** - Try re-saving the document

#### Azure DevOps Integration
- **Token permissions** - Ensure Work Items (Read) access
- **Organization name** - Verify correct Azure organization
- **Work item IDs** - Check Epic/User Story numbers exist

#### AI Response Issues
- **API key validity** - Confirm Google AI API key is active
- **Rate limits** - Check if you've exceeded API quotas
- **Network timeout** - Retry after a few minutes

### Performance Optimization
- **Regular cleanup** - Clear old uploaded files periodically
- **Cache management** - Configure appropriate cache settings
- **Database optimization** - Index frequently queried fields
- **Resource monitoring** - Monitor CPU and memory usage

## 🙏 Acknowledgments

- **New Relic** - API monitoring and discovery data
- **Azure DevOps** - Work item integration
- **Google AI** - Intelligent analysis capabilities
- **OpenAPI Initiative** - API specification standards

## 🔄 Changelog

### v1.0.0 (Latest)
- ✅ Initial release with core features
- ✅ New Relic API discovery integration
- ✅ PRD test case generation
- ✅ Manual API testing capabilities
- ✅ AI-powered chat assistant
- ✅ Azure DevOps integration

### Roadmap
- 🔜 **Advanced Analytics** - Custom dashboards and reports
- 🔜 **Team Collaboration** - Multi-user workspace support
- 🔜 **Login and Role Based Application**
- 🔜 **Database Implementation**
---

### Contributors to framework
* shuvendu