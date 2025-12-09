# Quick Start - Deployment Guide

## Access Your Application Now!

Your IntelliAgent application is successfully deployed and running!

### 🌐 Application URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://84.247.173.144 | Main web interface |
| **Frontend (Alt)** | http://84.247.173.144:3000 | Alternative port |
| **API Backend** | http://84.247.173.144:8080 | REST API |
| **API Docs** | http://84.247.173.144:8080/docs | Interactive API documentation |

### ✅ What's Working

- ✅ Frontend web interface accessible on port 80 and 3000
- ✅ Backend API running on port 8080
- ✅ PostgreSQL database running and healthy
- ✅ All containers up and running
- ✅ Firewall configured correctly

### 🚀 Quick Commands

#### Redeploy Application (Windows)
```cmd
cd d:\AgenteIA\build-deploy-ai-agent-python-docker
deploy.bat
```

#### View Application Status
```bash
ssh root@84.247.173.144 "cd /opt/intelliagent && docker compose -f compose.prod.yaml ps"
```

#### View Live Logs
```bash
ssh root@84.247.173.144 "cd /opt/intelliagent && docker compose -f compose.prod.yaml logs -f"
```

#### Restart Application
```bash
ssh root@84.247.173.144 "cd /opt/intelliagent && docker compose -f compose.prod.yaml restart"
```

### 📝 Test Your Deployment

1. **Test Frontend**:
   - Open browser: http://84.247.173.144
   - You should see the IntelliAgent interface

2. **Test API**:
   - Open browser: http://84.247.173.144:8080/docs
   - You should see the FastAPI Swagger documentation

3. **Test Backend Health**:
   ```bash
   curl http://84.247.173.144:8080/
   ```
   Expected response:
   ```json
   {"message":"Welcome to IntelliAgent API","project":"IntelliAgent","version":"1.0.0","docs":"/docs"}
   ```

### 🔐 Server Access

- **IP**: 84.247.173.144
- **User**: root
- **SSH Command**: `ssh root@84.247.173.144`

### 📂 Important Files

- **Deployment Config**: [compose.prod.yaml](compose.prod.yaml)
- **Environment Variables**: [.env](.env)
- **Deployment Script**: [deploy.bat](deploy.bat)
- **Full Documentation**: [DEPLOYMENT_INFO.md](DEPLOYMENT_INFO.md)

### ⚠️ Important Notes

1. **Environment Variables**: Make sure all required variables in `.env` are configured:
   - `OPENAI_API_KEY`: Required for AI features
   - `EMAIL_ADDRESS` & `EMAIL_PASSWORD`: For email notifications
   - `TRELLO_API_KEY`: For Trello integration

2. **API Access**: The backend API is accessible at `http://84.247.173.144:8080/api`

3. **Database**: PostgreSQL is running on port 5433 (external) / 5432 (internal)

### 🎯 Next Steps

1. **Test the Application**: Open http://84.247.173.144 and try creating a research task
2. **Configure Domain** (Optional): Point your domain to 84.247.173.144
3. **Setup SSL** (Recommended): Configure HTTPS for secure access
4. **Monitor Logs**: Keep an eye on logs for any issues

### 🆘 Troubleshooting

**Frontend not loading?**
```bash
ssh root@84.247.173.144 "cd /opt/intelliagent && docker compose -f compose.prod.yaml logs frontend"
```

**Backend not responding?**
```bash
ssh root@84.247.173.144 "cd /opt/intelliagent && docker compose -f compose.prod.yaml logs backend"
```

**Database issues?**
```bash
ssh root@84.247.173.144 "cd /opt/intelliagent && docker compose -f compose.prod.yaml logs db_service"
```

**Container not running?**
```bash
ssh root@84.247.173.144 "cd /opt/intelliagent && docker compose -f compose.prod.yaml up -d"
```

### 📊 Container Status

Current status (as of deployment):
```
✓ intelliagent_frontend - Running on ports 80, 3000
✓ intelliagent_backend  - Running on port 8080
✓ intelliagent_db       - Running (healthy) on port 5433
```

---

**Deployment Completed Successfully!** 🎉

Your IntelliAgent application is now live and ready to use at http://84.247.173.144
