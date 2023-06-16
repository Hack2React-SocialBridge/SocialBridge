from tests.factories.users import UserFactory
from social_bridge.auth import verify_token
from social_bridge.repositories.users import get_user_by_email


def test_token_generation(client):
    user = UserFactory.create()
    r = client.post(
        "users/token/", json={"username": user.email, "password": "Elektryk1@"}
    )
    assert r.status_code == 200
    assert verify_token(r.json()["access_token"]) == user.email


def test_register_new_user(db, client):
    test_user_email = "register_test@example.it"
    r = client.post(
        "users/register/", json={
            "email": test_user_email,
            "password": "Elektryk1@",
            "first_name": "Test",
            "last_name": "Test",
        }
    )
    db_user = get_user_by_email(db, test_user_email)
    assert r.status_code == 201
    assert db_user.email == test_user_email
