# Kubernetes Observability Lab (Logs + Metrics + Traces)

This repo contains a local observability lab built on top of a kind Kubernetes cluster.

Stack:

- **Logs**: Fluent Bit → OpenSearch → OpenSearch Dashboards
- **Metrics**: Prometheus + Alertmanager (via kube-prometheus-stack) → Grafana
- **Traces**: OpenTelemetry Collector → Jaeger
- **Demo app**: FastAPI service instrumented with OpenTelemetry

## Prerequisites

- Docker
- kubectl
- kind
- helm

## Quick Start

```bash
# 1. Create kind cluster
kind create cluster --name obs-lab --config kind-config.yaml

# 2. Create namespaces
kubectl apply -f k8s/namespaces.yaml

# 3. Install Helm components (logs, metrics, traces, otel)
# (see helm-values/ and commands in docs or script)

# 4. Build & push app image
cd app/traced-service
docker build -t <your-user>/traced-fastapi:v1 .
docker push <your-user>/traced-fastapi:v1

# 5. Deploy traced app
kubectl apply -f k8s/traced-app/deployment.yaml
