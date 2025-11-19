#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import random
import time
from datetime import datetime, timedelta, timezone

from incident_timeline_extractor.timeline.builder import build_timeline
from incident_timeline_extractor.timeline.model import Event

now = datetime.now(timezone.utc)
events = []
for i in range(5000):
    ts = now + timedelta(seconds=random.randint(-300, 300))
    events.append(
        Event(
            id=f"evt-{i}",
            timestamp=ts,
            source=random.choice(["nginx", "syslog", "zabbix", "prometheus"]),
            severity=random.choice(["info", "warning", "error", "critical"]),
            message="synthetic event",
            raw={},
        )
    )

start = time.time()
timeline = build_timeline("PERF-CHECK", events)
duration = time.time() - start
print(f"Generated {len(timeline.events)} events in {duration:.3f}s")
PY
