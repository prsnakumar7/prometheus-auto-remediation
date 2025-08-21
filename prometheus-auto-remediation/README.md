# Prometheus → Alertmanager → Flask Auto-Remediation

Self-healing demo: High CPU alert from Prometheus triggers Alertmanager,
which calls a Flask webhook that runs a remediation command on the target node.

## How it works
1. Target Node → Prometheus (metrics via node_exporter)
2. Prometheus → Alertmanager (fires `HighCPUUsage`)
3. Alertmanager → Flask (`/alerts` webhook)
4. Flask → Target Node (SSH remediation)

## Quick start
```bash
# Flask
cd flask_app
cp .env.example .env
python -m venv venv && . venv/bin/activate
pip install -r requirements.txt
python remediate_high_cpu.py
```

Run Prometheus/Alertmanager with the configs in `prometheus/` and `alertmanager/`.

## Diagram
See `diagrams/Architecture.png`.
