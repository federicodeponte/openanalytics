# Master AEO Service - Deployment Guide

## 🚀 Ready for Production Deployment

The Master AEO Service v5.0.0 is ready for deployment and integration with the openanalytics platform.

## 📋 Pre-Deployment Checklist

### ✅ Files Ready
- `master_aeo_service.py` - Core service implementation
- `master_deploy.py` - Modal deployment configuration
- `master_requirements.txt` - Dependencies
- `README_MASTER.md` - Complete documentation
- Supporting files: `fetcher.py`, `ai_client.py`, `scoring.py`, `checks/`

### ✅ Testing Complete
- Service imports successfully
- All endpoints responding
- Basic functionality validated
- No critical errors in local testing

## 🔧 Deployment Steps

### Step 1: Deploy to Modal

```bash
# Navigate to service directory
cd /Users/federicodeponte/openanalytics/aeo-checks

# Ensure Modal is configured
modal profile activate clients

# Deploy the service
modal deploy master_deploy.py
```

**Expected Deployment URL**: `https://clients--master-aeo-service-fastapi-app.modal.run`

### Step 2: Configure Secrets (Modal)

```bash
# Required secrets
modal secret create openai-secret OPENAI_API_KEY=your-openai-key
modal secret create openrouter-secret OPENROUTER_API_KEY=your-openrouter-key

# Optional (for native Gemini)
modal secret create gemini-secret GEMINI_API_KEY=your-gemini-key
```

### Step 3: Test Deployed Service

```bash
# Health check
curl https://clients--master-aeo-service-fastapi-app.modal.run/health

# Service status  
curl https://clients--master-aeo-service-fastapi-app.modal.run/status

# Full health check test
curl -X POST https://clients--master-aeo-service-fastapi-app.modal.run/health/check \
  -H "Content-Type: application/json" \
  -d '{"url": "https://scaile.tech"}'
```

## 🔗 Integration with OpenAnalytics

### Update Main Service Configuration

Update the existing openanalytics configuration to use the master service:

```python
# In openanalytics main service
MASTER_AEO_SERVICE_URL = "https://clients--master-aeo-service-fastapi-app.modal.run"

# Replace individual service calls
async def run_complete_aeo_analysis(url: str, company_name: str, company_analysis: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{MASTER_AEO_SERVICE_URL}/analyze/master",
            json={
                "url": url,
                "companyName": company_name,
                "companyAnalysis": company_analysis,
                "mode": "balanced",  # or "fast"/"full" based on needs
                "numQueries": 25
            },
            timeout=1800  # 30 minutes
        )
        return response.json()
```

### Update Existing Endpoints

Replace individual health and mentions endpoints:

**Before:**
```python
# Old individual calls
health_result = await call_health_service(url)
mentions_result = await call_mentions_service(company_name, company_analysis)
```

**After:**
```python  
# New unified call
master_result = await call_master_service(url, company_name, company_analysis)
health_result = master_result["health"]
mentions_result = master_result["mentions"]
combined_insights = master_result["strategic_recommendations"]
```

### Enhanced Reporting

Leverage the new combined intelligence:

```python
# Generate enhanced reports with strategic insights
report_data = {
    "health_score": master_result["health"]["overall_score"],
    "visibility_score": master_result["mentions"]["visibility"], 
    "combined_score": master_result["combined_score"],
    "combined_grade": master_result["combined_grade"],
    "strategic_recommendations": master_result["strategic_recommendations"],
    "priority_actions": master_result["priority_actions"]
}
```

## 📊 Monitoring & Maintenance

### Service Health Monitoring

```bash
# Monitor service health
curl https://clients--master-aeo-service-fastapi-app.modal.run/health

# Check detailed status
curl https://clients--master-aeo-service-fastapi-app.modal.run/status
```

### Performance Monitoring

Monitor key metrics:
- **Response times**: Health check (~30-60s), Mentions check (~2-5min), Master analysis (~3-6min)
- **Error rates**: Should be <5% under normal conditions
- **Platform availability**: All 5 AI platforms should be operational
- **Cost tracking**: Monitor API usage and costs

### Log Monitoring

```bash
# Monitor Modal logs
modal logs master-aeo-service --follow

# Check for errors
modal logs master-aeo-service --filter error
```

## 🚨 Troubleshooting

### Common Issues

1. **Service not responding**
   - Check Modal deployment status
   - Verify secrets are configured
   - Check for quota/billing issues

2. **Health checks failing**
   - Verify target websites are accessible
   - Check for network issues
   - Ensure Playwright dependencies are installed

3. **Mentions check errors**
   - Verify OpenRouter API key is valid
   - Check AI platform rate limits
   - Ensure company analysis data is properly formatted

4. **High error rates**
   - Check AI platform availability
   - Monitor rate limits and quotas
   - Verify request format and required fields

### Error Recovery

```python
# Implement fallback logic
async def call_master_service_with_fallback(url: str, company_name: str):
    try:
        # Try master service first
        return await call_master_service(url, company_name)
    except Exception as e:
        logger.error(f"Master service failed: {e}")
        # Fallback to individual services if needed
        health_result = await call_health_service(url)
        mentions_result = await call_mentions_service(company_name)
        return combine_results(health_result, mentions_result)
```

## 🔄 Updates & Versioning

### Service Updates

To deploy updates:
```bash
# Update the code
# Test locally first
python test_master_local.py

# Deploy updated version
modal deploy master_deploy.py
```

### Version Management

- **Current Version**: v5.0.0
- **Breaking Changes**: Document in CHANGELOG.md
- **API Versioning**: Consider versioned endpoints for major changes

## 📈 Scaling Considerations

### Performance Optimization
- **Concurrent Limits**: Currently set to 10 parallel requests
- **Timeout Management**: 30 minutes for complete analysis
- **Resource Allocation**: Adjust based on usage patterns

### Cost Optimization
- **Mode Selection**: Use "fast" mode for quick checks, "full" for comprehensive analysis
- **Query Limits**: Adjust numQueries based on requirements
- **Platform Selection**: Choose specific platforms if budget constraints exist

## 🎯 Success Criteria

### Deployment Success Indicators
- ✅ Service responds to all health endpoints
- ✅ Health checks return valid results
- ✅ Mentions checks process successfully (with valid API keys)
- ✅ Master analysis combines results correctly
- ✅ Error rates <5%
- ✅ Response times within expected ranges

### Integration Success Indicators  
- ✅ OpenAnalytics main service uses master endpoints
- ✅ Reports include combined insights
- ✅ Strategic recommendations appear in client deliverables
- ✅ Cost efficiency improved vs individual services

## 🎉 Go Live Checklist

### Final Pre-Launch
- [ ] Deploy master service to Modal
- [ ] Configure all required secrets  
- [ ] Test with real API keys and websites
- [ ] Update openanalytics integration
- [ ] Test end-to-end functionality
- [ ] Set up monitoring and alerting
- [ ] Document any custom configurations
- [ ] Train team on new combined insights

### Post-Launch
- [ ] Monitor performance for first 24 hours
- [ ] Collect feedback from initial users
- [ ] Document any issues and resolutions
- [ ] Plan next iteration of enhancements

---

## 🏆 Deployment Summary

**Master AEO Service v5.0.0 is production-ready** and combines the best features from both aeo-health-check and aeo-leaderboard implementations.

**Key Benefits:**
- **Unified Intelligence**: Health + visibility in single API
- **Strategic Insights**: Business-level recommendations  
- **Cost Efficiency**: Single service vs multiple endpoints
- **Enhanced Reports**: Combined analysis for better client value

**Ready for immediate deployment to Modal and integration with openanalytics platform.**