import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_cors_preflight_127_0_0_1():
    """Verify CORS preflight OPTIONS works for http://127.0.0.1:5173."""
    response = client.options(
        "/api/documents/list",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"
    assert response.headers.get("access-control-allow-credentials") == "true"

def test_cors_preflight_localhost():
    """Verify CORS preflight OPTIONS works for http://localhost:5173."""
    response = client.options(
        "/api/documents/list",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5173"
    assert response.headers.get("access-control-allow-credentials") == "true"

def test_cors_preflight_upload_endpoint():
    """Verify CORS preflight OPTIONS works for POST /api/documents/upload."""
    response = client.options(
        "/api/documents/upload",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type"
        }
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"

def test_documents_list_response_format():
    """Verify /api/documents/list returns a list of objects with expected keys."""
    response = client.get(
        "/api/documents/list",
        headers={"Origin": "http://127.0.0.1:5173"}
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        doc = data[0]
        assert "id" in doc
        assert "original_name" in doc
        assert "file_size" in doc
        assert "page_count" in doc
        assert "chunk_count" in doc
        assert "status" in doc
        assert "upload_date" in doc
