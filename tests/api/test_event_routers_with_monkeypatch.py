import pytest
from httpx import AsyncClient
from services.event_service import EventService

pytestmark = pytest.mark.anyio


async def test_mock_ent_get(authorized_superuser: AsyncClient, monkeypatch):
    data = {
        'card_id': 1,
        'imei': 1,
        'Entry': {'entry': 'Admission are permitted'}
    }

    async def mock_check_entry_possibility(*args, **kwargs):
        return data['Entry']

    monkeypatch.setattr(EventService, "check_entry_possibility", mock_check_entry_possibility)

    response = await authorized_superuser.get(f"/drop_in/{data['card_id']}/{data['imei']}")
    assert response.status_code == 200
    assert response.json() == data['Entry']

