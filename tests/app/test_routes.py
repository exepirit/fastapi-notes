import pytest
from fastapi.testclient import TestClient
from app import app
from database import schemes

SEPARATORS = (',', ':')


@pytest.fixture()
def app_client():
    client = TestClient(app)
    yield client


@pytest.mark.parametrize("board_id, board_name", [
    (1, "Board1"), (100500, "BoArD1")
])
def test__board__get_boards__returns_list_with_board(mocker, app_client, board_id, board_name):
    board = schemes.Board(id=board_id, name=board_name, notes=[])
    mocker.patch("database.crud.get_boards", return_value=[board])

    response = app_client.get("/api/board")

    assert response.ok
    expected_text = f"[{board.json(exclude={'board_id'}, separators=SEPARATORS)}]"
    assert response.text == expected_text


@pytest.mark.parametrize("board_name", [
    "Board2"
])
def test__board__add_board__returns_board(mocker, app_client, board_name):
    board = schemes.Board(id=1, name=board_name, notes=[])
    mocker.patch("database.crud.create_board", return_value=board)

    response = app_client.post("/api/board", json=board.dict(exclude={"board_id"}))

    assert response.ok
    assert response.text == board.json(exclude={"board_id"}, separators=SEPARATORS)


@pytest.mark.parametrize("board_id, board_name", [
    (666, "Board666")
])
def test__board__get_board__returns_one_board(mocker, app_client, board_id, board_name):
    board = schemes.Board(id=board_id, name=board_name, notes=[])
    get_board = mocker.patch("database.crud.get_board", return_value=board)

    response = app_client.get(f"/api/board/{board_id}")

    assert response.ok
    assert get_board.called
    assert get_board.call_args[0][1] == board_id
    assert response.text == board.json(separators=SEPARATORS)


@pytest.mark.parametrize("board_id", [
    1, 2, 1024
])
def test__board__delete_board__method_is_called(mocker, app_client, board_id):
    board = schemes.Board(id=board_id, name="")
    delete_board = mocker.patch("database.crud.delete_board", return_value=True)

    response = app_client.delete(f"/api/board/{board_id}")

    assert response.ok
    assert delete_board.called
    assert delete_board.call_args[0][1] == board
    assert response.text == "null"
