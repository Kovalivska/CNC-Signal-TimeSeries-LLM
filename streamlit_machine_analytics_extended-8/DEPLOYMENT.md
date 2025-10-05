# CNC Machine Analytics - Deployment Guide

## 🚀 Production-Ready Streamlit Application

### Application Overview
This Streamlit web application provides comprehensive CNC machine data analysis with the following capabilities:

- **Real-time Analytics**: Process CSV/Parquet/JSON files with 90+ CNC signal fields
- **Intelligent Metrics**: Automated cycle time detection, setup time analysis, production output tracking
- **Interactive Visualization**: Dynamic time series charts, shift-based KPIs, and customizable dashboards
- **Multi-language Support**: German, English, and Russian query processing
- **Offline Operation**: Complete data processing without external dependencies

### Technology Stack
- **Frontend**: Streamlit 1.37.1
- **Data Processing**: pandas 2.2.2, DuckDB 1.1.0
- **Visualization**: Native Streamlit charts with pyarrow 16.1.0
- **Time Handling**: pytz 2024.1 for timezone management

## 🛠️ Local Development Setup

### Prerequisites
```bash
# Ensure Python 3.9+ is installed
python --version

# Verify conda/pip package manager
conda --version  # or pip --version
```

### Installation Steps
```bash
# 1. Navigate to application directory
cd streamlit_machine_analytics_extended-8

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch application
streamlit run app.py

# 4. Access application
# http://localhost:8502
```

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (Recommended)
```bash
# 1. Push project to GitHub repository
git add .
git commit -m "Deploy CNC Analytics App"
git push origin main

# 2. Visit https://streamlit.io/cloud
# 3. Connect GitHub repository
# 4. Select: streamlit_machine_analytics_extended-8/app.py
# 5. Deploy automatically
```

### Option 2: Docker Container
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

```bash
# Build and run
docker build -t cnc-analytics .
docker run -p 8501:8501 cnc-analytics
```

### Option 3: Local Network Deployment
```bash
# For LAN access (replace IP with your machine's IP)
streamlit run app.py --server.address 0.0.0.0 --server.port 8502

# Access from other devices: http://YOUR_IP:8502
```

### Option 4: Cloud VPS Deployment
```bash
# On Ubuntu/Debian VPS
sudo apt update
sudo apt install python3-pip python3-venv git

# Clone repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd streamlit_machine_analytics_extended-8

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install PM2 for process management
npm install -g pm2

# Create PM2 ecosystem file
cat > ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: 'cnc-analytics',
    script: 'streamlit',
    args: 'run app.py --server.address 0.0.0.0 --server.port 8502',
    cwd: '/path/to/streamlit_machine_analytics_extended-8',
    env: {
      PATH: '/path/to/streamlit_machine_analytics_extended-8/venv/bin:' + process.env.PATH
    }
  }]
}
EOF

# Start with PM2
pm2 start ecosystem.config.js
pm2 startup
pm2 save
```

## 🔧 Configuration Options

### Environment Variables
```bash
# .env file (optional)
STREAMLIT_SERVER_PORT=8502
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_THEME_BASE=light
STREAMLIT_SERVER_MAXUPLOADSIZE=200
```

### Custom Configuration
```bash
# ~/.streamlit/config.toml
[server]
port = 8502
address = "0.0.0.0"
maxUploadSize = 200

[theme]
base = "light"
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

## 🔍 Performance Considerations

### Recommended System Requirements
- **CPU**: 2+ cores
- **RAM**: 4GB+ (8GB recommended for large datasets)
- **Storage**: 1GB free space
- **Network**: Stable internet for deployment (not required for operation)

### Data Size Recommendations
- **Optimal**: < 1M rows per upload
- **Good Performance**: 1-10M rows
- **Large Datasets**: Consider data filtering or aggregation

### Performance Optimization
```python
# In app.py, adjust caching parameters:
@st.cache_data(ttl=3600, show_spinner=False)  # 1 hour cache
def load_files(files):
    # ... existing code
```

## 🛡️ Security Considerations

### Data Privacy
- **Offline-first**: All data processing happens locally
- **No external calls**: No data transmitted to external services
- **File upload security**: Only CSV/Parquet/JSON accepted

### Deployment Security
```bash
# For production deployment, consider:
# 1. HTTPS proxy (nginx/Apache)
# 2. Authentication layer
# 3. Rate limiting
# 4. File size restrictions
```

## 📊 Monitoring & Maintenance

### Health Checks
```bash
# Check if application is running
curl http://localhost:8502/_stcore/health

# Monitor logs
tail -f ~/.streamlit/logs/streamlit.log
```

### Backup Strategy
```bash
# Backup configuration and custom templates
tar -czf cnc-analytics-backup.tar.gz \
  streamlit_machine_analytics_extended-8/ \
  ~/.streamlit/
```

## 🆘 Troubleshooting

### Common Issues
1. **Port conflicts**: Change port with `--server.port XXXX`
2. **Memory issues**: Reduce dataset size or increase system RAM
3. **Module not found**: Reinstall requirements with `pip install -r requirements.txt`
4. **File upload errors**: Check file format and size limits

### Debug Mode
```bash
# Enable debug logging
streamlit run app.py --logger.level debug
```

## 📈 Scaling Options

### Horizontal Scaling
- Deploy multiple instances behind load balancer
- Use Docker Swarm or Kubernetes for orchestration
- Implement session affinity for file uploads

### Vertical Scaling
- Increase VM/container resources
- Optimize pandas operations for larger datasets
- Consider Dask for distributed computing

## 📞 Support & Documentation

### Resources
- **Application Documentation**: `README.md`
- **CNC Field Dictionary**: `resources/dictionary.md`
- **Preset Queries**: `templates/presets.json`
- **Streamlit Documentation**: https://docs.streamlit.io

### Contact Information
- **Project Lead**: Dr. Svitlana Kovalivska
- **Repository**: https://github.com/YOUR_USERNAME/Industrial_Signal_Processing_TimeSeriesAnalysis
- **Issues**: GitHub Issues section

---

**Last Updated**: January 2025  
**Version**: 8.0  
**License**: MIT
