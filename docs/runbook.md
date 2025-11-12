<!-- → Architecture & Build by DocSynapse-->
<!-- Intelligent by Design. Crafted for Humanity. -->

# Aethersite Runbook

## Operational Procedures

### Starting the System

#### Development Mode

**Backend:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

#### Production Mode (Docker)

```bash
docker-compose up -d
```

#### Production Mode (Manual)

**Backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

### Stopping the System

#### Docker
```bash
docker-compose down
```

#### Manual
- Press `Ctrl+C` in terminal running the servers
- Or kill processes:
  ```bash
  # Find PIDs
  lsof -i :8000  # Backend
  lsof -i :3000  # Frontend
  
  # Kill processes
  kill <PID>
  ```

### Health Checks

#### Check Backend Health
```bash
curl http://localhost:8000/api/health
```

Expected: `{"status": "healthy", "service": "Aethersite API"}`

#### Check System Status
```bash
curl http://localhost:8000/api/status
```

Expected: `{"status": "active", "document_count": N, "system_health": "good"}`

#### Check Frontend
```bash
curl http://localhost:3000
```

Expected: HTML response with status 200

### Monitoring

#### Log Locations

**Backend Logs:**
- Development: Console output
- Docker: `docker-compose logs backend`
- Production: TODO: Configure log file location

**Frontend Logs:**
- Development: Browser console + terminal
- Docker: `docker-compose logs frontend`
- Production: TODO: Configure log aggregation

#### Key Metrics to Monitor

1. **Document Count**: Should increase as documents are added
2. **Search Response Time**: Should be < 100ms for typical queries
3. **Storage Usage**: Monitor `docmemory_storage/` directory size
4. **Memory Usage**: Monitor Python process memory
5. **API Response Times**: Monitor `/api/status` endpoint

**TODO**: Set up proper monitoring with Prometheus/Grafana

### Backup Procedures

#### Manual Backup

```bash
# Backup storage directory
tar -czf docmemory_backup_$(date +%Y%m%d_%H%M%S).tar.gz docmemory_storage/

# Backup database only
cp docmemory_storage/document_memories.db backups/
```

#### Automated Backup

**TODO**: Set up automated backup script:
- Daily backups
- Weekly full backups
- Monthly archive backups
- Backup rotation (keep last 30 days)

### Restore Procedures

#### From Backup

```bash
# Stop system
docker-compose down

# Restore storage directory
tar -xzf docmemory_backup_YYYYMMDD_HHMMSS.tar.gz

# Restart system
docker-compose up -d
```

### Common Operations

#### Add Document via API

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@document.pdf" \
  -F "title=My Document" \
  -F "tags=research,AI"
```

#### Search Documents

```bash
curl -X POST http://localhost:8000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{"query": "machine learning", "search_type": "hybrid", "limit": 10}'
```

#### Check Document Count

```bash
curl http://localhost:8000/api/status | jq '.document_count'
```

### Troubleshooting

#### Issue: Backend Won't Start

**Symptoms**: Port 8000 already in use or import errors

**Diagnosis:**
```bash
# Check if port is in use
lsof -i :8000

# Check Python dependencies
pip list | grep fastapi
pip list | grep uvicorn
```

**Solution:**
1. Kill process using port 8000
2. Reinstall dependencies: `pip install -r backend/requirements.txt`
3. Check Python version: `python --version` (should be 3.9+)

#### Issue: Frontend Can't Connect to Backend

**Symptoms**: CORS errors or connection refused

**Diagnosis:**
```bash
# Check backend is running
curl http://localhost:8000/api/health

# Check CORS configuration
cat backend/core/config.py | grep CORS_ORIGINS
```

**Solution:**
1. Ensure backend is running
2. Check CORS_ORIGINS includes frontend URL
3. Restart backend after config changes

#### Issue: Search Returns No Results

**Symptoms**: Empty results array

**Diagnosis:**
```bash
# Check document count
curl http://localhost:8000/api/status

# Check storage directory
ls -la docmemory_storage/
```

**Solution:**
1. Verify documents exist: `document_count > 0`
2. Check FAISS index exists: `ls docmemory_storage/*.bin`
3. Re-index if needed: TODO: Add re-indexing command

#### Issue: High Memory Usage

**Symptoms**: System slows down, memory warnings

**Diagnosis:**
```bash
# Check memory usage
ps aux | grep python
ps aux | grep node

# Check storage size
du -sh docmemory_storage/
```

**Solution:**
1. Restart services to clear cache
2. Check for memory leaks in logs
3. Consider increasing system resources
4. Optimize FAISS index (TODO: Add optimization guide)

#### Issue: Upload Fails

**Symptoms**: 500 error on upload endpoint

**Diagnosis:**
```bash
# Check backend logs
docker-compose logs backend | tail -50

# Check file permissions
ls -la docmemory_storage/
```

**Solution:**
1. Check file format is supported (PDF, DOCX, TXT)
2. Verify storage directory is writable
3. Check disk space: `df -h`
4. Review error logs for specific issue

### Maintenance Tasks

#### Daily

- [ ] Check system health endpoints
- [ ] Review error logs
- [ ] Monitor storage usage

#### Weekly

- [ ] Review backup completion
- [ ] Check for dependency updates
- [ ] Review performance metrics

#### Monthly

- [ ] Full system backup
- [ ] Update dependencies (if stable)
- [ ] Review and rotate logs
- [ ] Performance optimization review

### Emergency Procedures

#### System Down

1. **Check Status**:
   ```bash
   curl http://localhost:8000/api/health
   ```

2. **Check Logs**:
   ```bash
   docker-compose logs --tail=100
   ```

3. **Restart Services**:
   ```bash
   docker-compose restart
   ```

4. **If Still Down**:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

#### Data Corruption

1. **Stop System**:
   ```bash
   docker-compose down
   ```

2. **Restore from Backup**:
   ```bash
   # See Restore Procedures above
   ```

3. **Verify Data**:
   ```bash
   curl http://localhost:8000/api/status
   ```

4. **Restart System**

#### Security Incident

1. **Immediate Actions**:
   - Stop all services
   - Isolate affected systems
   - Preserve logs

2. **Investigation**:
   - Review access logs
   - Check for unauthorized changes
   - Review recent deployments

3. **Recovery**:
   - Restore from known good backup
   - Update credentials
   - Patch vulnerabilities

**TODO**: Develop detailed security incident response plan

### Performance Tuning

#### Backend Optimization

**TODO**: Add performance tuning guide:
- Database query optimization
- FAISS index optimization
- Caching strategies
- Connection pooling

#### Frontend Optimization

**TODO**: Add frontend optimization guide:
- Code splitting
- Image optimization
- Bundle size reduction
- CDN configuration

### Scaling Considerations

#### Horizontal Scaling

**TODO**: Add scaling guide:
- Load balancer configuration
- Database replication
- Session management
- Distributed FAISS index

#### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize FAISS index for larger datasets
- Add caching layer (Redis)

### Contact Information

**TODO**: Add:
- On-call rotation schedule
- Escalation procedures
- Vendor contacts
- Emergency contacts

### Change Management

**Before Making Changes:**

1. Review this runbook
2. Test in development environment
3. Create backup
4. Document changes
5. Notify team

**After Making Changes:**

1. Verify system health
2. Monitor for issues
3. Update documentation
4. Update runbook if needed
