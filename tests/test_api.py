from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_ping_ok_until_limited(monkeypatch):
    # Force small limits for quick test — app reads from settings on import
    # For simplicity, we just hit the default in-memory limiter (3 in 10s)
    r1 = client.get("/ping", params={"user_id": "eve"})
    assert r1.status_code == 200
    r2 = client.get("/ping", params={"user_id": "eve"})
    assert r2.status_code == 200
    r3 = client.get("/ping", params={"user_id": "eve"})
    assert r3.status_code == 200
    r4 = client.get("/ping", params={"user_id": "eve"})
    assert r4.status_code == 429
    assert r4.headers.get("Retry-After") is not None
