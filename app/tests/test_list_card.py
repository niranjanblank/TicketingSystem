
def test_create_list_card(client, board_list_data_single):
    """ Test for creating card in a list """
    list_card_data = {
        "title": "Test Card",
        "desc": "Test Description",
        "list_id": board_list_data_single.id
    }
    response = client.post("/list_card", json=list_card_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == list_card_data["title"]
    assert data["desc"] == list_card_data["desc"]
    assert data["list_id"] == list_card_data["list_id"]

def test_get_list_card_by_list_id_endpoint_success(client, list_card_data):
    list_id = list_card_data[0].list_id
    response = client.get(f"/list_card/list/{list_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(list_card_data)
    for i, card in enumerate(data):
        assert card["title"] == list_card_data[i].title
        assert card["desc"] == list_card_data[i].desc
        assert card["list_id"] == list_card_data[i].list_id
