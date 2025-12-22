# Prometheus Monitoring - Clean Implementation

## ✅ What's Implemented

A **minimal, clean** Prometheus monitoring setup for your Django Online Shop:

### Components
1. **Django Prometheus Integration** - HTTP request metrics via middleware
2. **Prometheus Server** - Metrics collection and storage
3. **Grafana** - Visualization and dashboards
4. **PostgreSQL Exporter** - Database metrics
5. **Redis Exporter** - Cache metrics

### Changes Made
- Added `django-prometheus` to `requirements.txt`
- Added `django_prometheus` to `INSTALLED_APPS` (first position)
- Added Prometheus middleware (before and after)
- Added `/metrics` endpoint
- Added 4 monitoring services to `docker-compose.yml`

---

## 🚀 Quick Start

### 1. Access Services

All services are running:

```bash
# Check status
docker compose ps
```

**URLs:**
- **Django API**: http://localhost:8000/api/products/
- **Metrics Endpoint**: http://localhost:8000/metrics
- **Prometheus UI**: http://localhost:9090
- **Grafana UI**: http://localhost:3000 (admin/admin)

### 2. View Metrics

**Django Metrics:**
```bash
curl http://localhost:8000/metrics
```

**Prometheus Targets:**
- Go to http://localhost:9090/targets
- All should show as "UP" (green)

### 3. Query Metrics in Prometheus

Open http://localhost:9090/graph and try these queries:

**HTTP Request Rate:**
```promql
rate(django_http_requests_total_by_method_total[5m])
```

**Request Count by View:**
```promql
django_http_requests_total_by_view_transport_method_total
```

**Database Connections:**
```promql
pg_stat_database_numbackends{datname="onlineshop"}
```

**Redis Memory Usage:**
```promql
redis_memory_used_bytes
```

---

## 📊 Available Metrics

### Django Application (Automatic)
- `django_http_requests_total_by_method_total` - Requests by HTTP method
- `django_http_requests_total_by_transport_total` - Requests by transport
- `django_http_requests_total_by_view_transport_method_total` - Requests by view
- `django_http_requests_latency_seconds` - Request latency histogram
- `django_http_responses_total_by_status_total` - Responses by status code
- `django_http_responses_total_by_charset_total` - Responses by charset
- `django_http_responses_total_by_templatename_total` - Responses by template

### PostgreSQL (from postgres-exporter)
- `pg_stat_database_*` - Database statistics
- `pg_stat_activity_*` - Active connections
- `pg_up` - Database availability

### Redis (from redis-exporter)
- `redis_memory_used_bytes` - Memory usage
- `redis_connected_clients` - Connected clients
- `redis_commands_total` - Total commands executed
- `redis_up` - Redis availability

---

## 📈 Grafana Dashboards

### Setup Grafana

1. Open http://localhost:3000
2. Login: `admin` / `admin`
3. Prometheus datasource is auto-configured

### Import Dashboards

Go to **Dashboards → Import** and use these IDs:

- **Django**: `12229` - Django Application Metrics
- **PostgreSQL**: `9628` - PostgreSQL Database
- **Redis**: `11835` - Redis Dashboard

---

## 🔧 Configuration Files

### Modified Files

**`requirements.txt`:**
```txt
django-prometheus==2.3.1
prometheus-client==0.19.0
```

**`core/settings.py`:**
```python
INSTALLED_APPS = [
    "django_prometheus",  # First
    # ... rest of apps
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",  # First
    # ... other middleware
    "django_prometheus.middleware.PrometheusAfterMiddleware",  # Last
]
```

**`core/urls.py`:**
```python
urlpatterns = [
    # ... your URLs
    path("", include("django_prometheus.urls")),  # Adds /metrics endpoint
]
```

### New Files

**`prometheus/prometheus.yml`** - Prometheus configuration
**`grafana/provisioning/datasources/prometheus.yml`** - Grafana datasource

---

## 🎯 How to Use Custom Metrics (Optional)

If you want to track business metrics, use the `core/metrics.py` file:

```python
# In your views
from core.metrics import orders_created_total, product_views_total

# Track order creation
orders_created_total.labels(status='completed').inc()

# Track product views
product_views_total.labels(
    product_id=str(product.id),
    category=product.category.name
).inc()
```

---

## 🐛 Troubleshooting

### Metrics endpoint returns 404
- Restart Django: `docker compose restart web`
- Check URL: http://localhost:8000/metrics (no trailing slash)

### Prometheus can't scrape Django
- Check Django is running: `docker compose ps`
- Check Django logs: `docker compose logs web`
- Verify metrics work: `curl http://localhost:8000/metrics`

### No data in Grafana
- Check Prometheus targets: http://localhost:9090/targets
- Verify datasource: Grafana → Configuration → Data Sources
- Wait a few minutes for data to accumulate

---

## 📝 Architecture

```
┌─────────────┐
│   Grafana   │ ← Visualization
│  :3000      │
└──────┬──────┘
       │
┌──────▼──────┐
│ Prometheus  │ ← Metrics Collection
│  :9090      │
└──────┬──────┘
       │
       ├─────→ Django App :8000/metrics
       ├─────→ PostgreSQL Exporter :9187
       └─────→ Redis Exporter :9121
```

---

## ✨ Benefits

- **Zero Code Changes** - Metrics work automatically via middleware
- **Clean Implementation** - Minimal configuration, no messy code
- **Production Ready** - Standard Prometheus stack
- **Extensible** - Easy to add custom metrics when needed

---

## 🔗 Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [django-prometheus GitHub](https://github.com/korfuri/django-prometheus)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)

---

**Your Django Online Shop now has professional monitoring! 🎉**

