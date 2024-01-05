import pytest

from schemas.device_schema import DeviceEmployeePostRequestSchema
from services import EventService, DeviceService

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    'access_to_device, has_permission',
    [
        (False, {'entry': 'Admission are prohibited'}),
        (True, {'entry': 'Admission are permitted'})


    ]
)
async def test_check_entry_possibility(
        fake_event_repository,
        fake_employee_repository,
        fake_device_repository,
        fake_department_repository,
        access_to_device: bool,
        has_permission: dict
):

    first_device = fake_device_repository.items[0]
    first_employee = fake_employee_repository.items[0]

    if access_to_device:
        data = {'device_id': first_device.id, 'employee_id': first_employee.id}

        await (DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository)
               .add_employee(DeviceEmployeePostRequestSchema(**data)))

    event = EventService(fake_device_repository,
                         fake_event_repository,
                         fake_employee_repository,
                         )

    data = {
        'card_id': first_employee.card_id,
        'imei': first_device.imei
    }

    retrieved_answer = await event.check_entry_possibility(**data)

    assert retrieved_answer == has_permission


async def test_create(
        fake_employee_repository,
        fake_device_repository,
        fake_event_repository
):

    event = EventService(fake_device_repository, fake_event_repository, fake_employee_repository)
    data = event.EntryPossibility(success=True, employee_id=1, device_id=1)
    retrieved = await event.create(data)

    assert retrieved is None



