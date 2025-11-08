# tests/test_reports.py

def test_stats_overview_reflects_occupancy(client):
    # Sin entradas: todo libre
    res_empty = client.get("/api/core/stats/overview")
    assert res_empty.status_code == 200
    data_empty = res_empty.json()
    assert data_empty["occupied"] == 0
    assert data_empty["free"] >= 1

    # Crear una entrada
    client.post("/api/core/entries", json={"plate": "OCC001"})

    res = client.get("/api/core/stats/overview")
    assert res.status_code == 200
    data = res.json()

    assert data["occupied"] == 1
    assert data["free"] >= 0
    assert data["currentRatePerMinute"] > 0
    assert 0 <= data["occupancyPercent"] <= 100