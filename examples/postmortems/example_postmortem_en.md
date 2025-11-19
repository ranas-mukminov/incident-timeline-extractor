# Postmortem for INC-EXAMPLE

- Incident ID: INC-EXAMPLE
- Date: 2025-11-20
- Severity: high

## Summary
HTTP errors on frontend caused partial outage.

## Impact
Users saw 502 errors for ~2 minutes.

## Root Cause
Backend timeouts during deploy.

## Contributing Factors
No circuit breaker on upstream.

## Timeline
- **2025-11-19 08:12:01 UTC** [nginx/web-1][error] 502 GET /
- **2025-11-19 08:12:15 UTC** [prometheus/web-1][critical] HTTP 5xx spiked
- **2025-11-19 08:12:25 UTC** [zabbix/db-1][error] DB latency high

## What Went Well
Fast alerting and rollback.

## What Can Be Improved
Add health checks and load test before deploys.

## Action Items
- [ ] Add DB timeout alarms (owner: sre, due: 2025-12-01)
- [ ] Document rollback steps (owner: eng, due: 2025-12-05)

## Lessons Learned
Test cross-service dependencies before changes.
