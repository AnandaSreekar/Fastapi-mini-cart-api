from fastapi.testclient import TestClient
import main


def test_get_item_returns_item_when_exists():
    main.items.clear()
    with TestClient(main.app) as client:
        post_response = client.post("/items", params={"item": "apple"})
        assert post_response.status_code == 200

        get_response = client.get("/items/0")
        assert get_response.status_code == 200
        assert get_response.json() == "apple"


def test_get_item_returns_404_when_missing():
    main.items.clear()
    with TestClient(main.app) as client:
        response = client.get("/items/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Item not found"
