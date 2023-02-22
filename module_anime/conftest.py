import uuid
import pytest

from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())

        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def api_client_with_credentials(db, create_user, api_client):
    user = create_user()

    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def api_client_with_admin_credentials(db, create_user, api_client):
    super_user = create_user(username='super_someone', is_staff=True, is_superuser=True)

    api_client.force_authenticate(user=super_user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login
