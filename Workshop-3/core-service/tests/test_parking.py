# tests/test_parking.py

from time import sleep


def test_health(client):
    res = client.get("/api/core/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_entry_creates_session_and_occupies_slot(client):
    # Registramos entrada
    res = client.post("/api/core/entries", json={"plate": "ABC123"})
    assert res.status_code == 200

    data = res.json()
    assert data["plate"] == "ABC123"
    assert data["slot_code"] in ["A01", "A02", "A03"]
    assert "session_id" in data

    # Slots: uno debe aparecer ocupado
    res_slots = client.get("/api/core/slots")
    assert res_slots.status_code == 200
    slots = res_slots.json()
    assert any(s["occupied"] for s in slots)


def test_double_entry_same_plate_not_allowed(client):
    # Primera entrada OK
    r1 = client.post("/api/core/entries", json={"plate": "XYZ999"})
    assert r1.status_code == 200

    # Segunda entrada misma placa debe fallar
    r2 = client.post("/api/core/entries", json={"plate": "XYZ999"})
    assert r2.status_code == 400
    assert "already inside" in r2.json()["detail"]


def test_exit_calculates_amount_and_frees_slot(client):
    # Crear entrada
    r_entry = client.post("/api/core/entries", json={"plate": "CAR001"})
    assert r_entry.status_code == 200
    slot_code = r_entry.json()["slot_code"]

    # Simular un pequeño tiempo (opcional)
    sleep(0.1)

    # Registrar salida
    r_exit = client.post("/api/core/exits", json={"plate": "CAR001"})
    assert r_exit.status_code == 200

    data = r_exit.json()
    assert data["plate"] == "CAR001"
    assert data["minutes"] >= 1
    assert data["amount"] > 0.0
    assert data["check_out_at"] is not None

    # Verificar que el slot quede libre (o no ocupado por esa sesión)
    r_slots = client.get("/api/core/slots")
    assert r_slots.status_code == 200
    slots = r_slots.json()
    # El slot donde estuvo CAR001 no debería reportar esa placa
    assert not any(s["code"] == slot_code and s.get("plate") == "CAR001" for s in slots)


def test_sessions_list_returns_recent_sessions(client):
    # Crear un par de entradas/salidas
    client.post("/api/core/entries", json={"plate": "TST111"})
    client.post("/api/core/exits", json={"plate": "TST111"})
    client.post("/api/core/entries", json={"plate": "TST222"})

    res = client.get("/api/core/sessions?limit=5")
    assert res.status_code == 200

    data = res.json()
    assert "items" in data
    assert len(data["items"]) >= 2
    # Cada item debe tener estructura consistente
    item = data["items"][0]
    assert "plate" in item
    assert "slot_code" in item
    assert "check_in_at" in item