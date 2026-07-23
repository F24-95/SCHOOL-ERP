import sys

sys.path.insert(0, ".")
from app.main import app

routes = []
for route in app.routes:
    if hasattr(route, "methods") and hasattr(route, "path"):
        for method in route.methods:
            if method in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                routes.append((method, route.path))

routes.sort(key=lambda x: x[1])

for method, path in routes:
    print(f"{method:7s} {path}")

print(f"\nTotal: {len(routes)} routes")
