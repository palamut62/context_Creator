### 🔄 Project Awareness & Context
- **Always read `INITIAL.md`** at the start to understand project requirements and scope
- **Follow Context Engineering principles** from https://github.com/coleam00/context-engineering-intro
- **Use Turkish language** for all user-facing content and documentation
- **Support multiple AI coding assistants** - not just Claude, but also Cursor, GitHub Copilot, etc.

### 🧱 Code Structure & Architecture
- **Flask için modern pattern'ler kullan**: HTML templates, Bootstrap, responsive design ile düzenli layout
- **Pydantic AI multi-agent sistem**: Her agent farklı uzmanlık alanını temsil eder
- **Async/await pattern'leri**: API çağrıları için asenkron işlemler
- **Type hints ve Pydantic models**: Güçlü tip güvenliği
- **Modüler yapı**: Her component ayrı dosyada, clear separation of concerns

### 🔌 API Integration Standards
- **Environment variables**: Tüm API anahtarları .env dosyasında
- **Provider factory pattern**: Farklı LLM provider'ları için unified interface
- **Retry logic**: API çağrılarında exponential backoff
- **Rate limiting**: Her provider için uygun rate limits
- **Error handling**: Graceful degradation ve user-friendly error messages

### 🤖 Pydantic AI Agent Guidelines
- **Agent specialization**: Her agent belirli bir role sahip (System Analyst, Architect, etc.)
- **Dependency injection**: Shared resources için deps_type kullan
- **Tool registration**: @agent.tool decorator ile proper tool definition
- **Usage tracking**: ctx.usage ile token tracking across agents
- **Message history**: Conversation context için message_history kullan

### 🎨 Flask Web UI/UX Standards
- **Responsive design**: Bootstrap grid system ile mobile-friendly layout
- **Progress indicators**: Progress bars ve loading spinners ile user feedback
- **Form validation**: Real-time validation ve clear error messages
- **State management**: Flask session ile proper state handling
- **Export functionality**: HTTP file downloads ile export features

### 📋 Context Engineering Compliance
- **PRP Structure**: Name, description, purpose, core principles sections
- **Implementation Blueprint**: Detailed step-by-step implementation guide
- **Validation Loops**: Executable tests and quality checks
- **Anti-patterns**: Clear guidance on what to avoid
- **Confidence scoring**: 1-10 scale for implementation confidence

### 🧪 Testing & Quality
- **Unit tests**: pytest ile comprehensive test coverage
- **Integration tests**: API endpoints ve agent interactions
- **PRP validation**: Generated PRP files için quality checks
- **Performance tests**: Response time ve memory usage
- **User acceptance tests**: Real-world scenarios

### 📚 Documentation Standards
- **Turkish documentation**: Kullanıcı dokümantasyonu Türkçe
- **Code comments**: Complex logic için açıklayıcı comments
- **API documentation**: Docstrings ile comprehensive API docs
- **Usage examples**: Her feature için practical examples
- **Troubleshooting guide**: Common issues ve solutions

### 🔒 Security & Privacy
- **API key management**: Secure storage ve rotation
- **Input sanitization**: User inputs için proper validation
- **Rate limiting**: DoS protection
- **Error logging**: Sensitive information leak prevention
- **GDPR compliance**: User data handling best practices

### 🚀 Performance Optimization
- **Caching**: st.cache_data ve st.cache_resource kullan
- **Lazy loading**: Heavy operations için on-demand loading
- **Memory management**: Large objects için proper cleanup
- **Async operations**: Non-blocking API calls
- **Batch processing**: Multiple operations için batching

### 📊 Monitoring & Observability
- **Logging**: Structured logging ile proper log levels
- **Metrics**: Usage statistics ve performance metrics
- **Error tracking**: Exception handling ve reporting
- **User analytics**: Feature usage tracking
- **Health checks**: System status monitoring 