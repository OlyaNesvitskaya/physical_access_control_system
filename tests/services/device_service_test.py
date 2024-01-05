import pytest
from fastapi import HTTPException

from services import DeviceService
from schemas.device_schema import DeviceSchema, UpdateDeviceSchema, DeviceEmployeePostRequestSchema

pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    'page_size, start_index, number_of_records',
    [
        (3, 0, 3),
        (0, 0, 0),
        (5, 1, 2)
    ]
)
async def test_list(
        page_size,
        start_index,
        number_of_records,
        fake_device_repository,
        fake_department_repository,
        fake_employee_repository):

    retrieved = await (DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository)
                 .list(page_size=page_size, start_index=start_index))

    assert len(retrieved) == number_of_records
    assert retrieved == fake_device_repository.items[start_index:page_size]


async def test_get(fake_device_repository, fake_department_repository, fake_employee_repository):
    
    first_device = fake_device_repository.items[0]
    retrieved = await (DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository)
                 .get(first_device.id))

    assert retrieved.name == first_device.name
    assert retrieved.imei == first_device.imei
    assert retrieved.department_id == first_device.department_id
    assert retrieved.route == first_device.route


async def test_get_error(fake_device_repository, fake_department_repository, fake_employee_repository):
    
    with pytest.raises(HTTPException) as excinfo:
        await DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository).get(10)
        
    assert excinfo.type is HTTPException


async def test_create(fake_device_repository, fake_department_repository, fake_employee_repository):
    
    new_device = DeviceSchema(id=5, name='Contact reader №5', imei='555555qwerty', route='enter', department_id=1)
    retrieved = await (DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository)
                 .create(new_device))

    assert retrieved.name == new_device.name
    assert retrieved.imei == new_device.imei
    assert retrieved.department_id == new_device.department_id
    assert retrieved.route == new_device.route


async def test_error_create(fake_device_repository, fake_department_repository, fake_employee_repository):
    
    with pytest.raises(HTTPException) as excinfo:
        device = DeviceSchema(id=5, name='Contact reader №5', imei='555555qwerty', route='enter', department_id=1)
        await DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository).create(device)
        
    assert excinfo.type is HTTPException


async def test_update(fake_device_repository, fake_department_repository, fake_employee_repository):
    
    last_device = fake_device_repository.items[-1]
    retrieved = await (DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository)
                 .update(last_device.id, UpdateDeviceSchema(imei='101010qwerty')))
    
    assert retrieved.name == last_device.name
    assert retrieved.imei == last_device.imei
    assert retrieved.department_id == last_device.department_id
    assert retrieved.route == last_device.route
    assert retrieved.opened == last_device.opened


@pytest.mark.parametrize(
    'device_id, device_schema, type_exception, exception_value',
    [
        (1, UpdateDeviceSchema(department_id=100), HTTPException,
         "(400, 'Incorrect department_id. Department with supplied ID does not exist.')"),

        (2, UpdateDeviceSchema(imei='333333qwerty'), HTTPException,
         "(409, 'Device with imei:333333qwerty already exist.')"),

        (10, UpdateDeviceSchema(imei='555555qwerty'), HTTPException,
         "(400, 'Device with supplied ID does not exist.')"),
    ]
)
async def test_error_update(fake_device_repository, fake_department_repository,
                      fake_employee_repository, device_id, device_schema,
                      type_exception, exception_value):

    with (pytest.raises(type_exception) as excinfo):
        await DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository
                      ).update(device_id, device_schema)

    assert excinfo.type is type_exception
    assert str(excinfo.value) == exception_value


async def test_delete(fake_device_repository, fake_department_repository, fake_employee_repository):

    retrieved = await (DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository)
                 .delete(fake_device_repository.items[-1].id))

    assert retrieved is None


async def test_error_delete(fake_device_repository, fake_department_repository, fake_employee_repository):

    with pytest.raises(HTTPException) as excinfo:
        await (DeviceService(fake_device_repository, fake_department_repository, fake_employee_repository)
         .delete(100))

    assert excinfo.type is HTTPException


async def test_device_service_can_add_record_in_access_control_table(
        fake_device_repository,
        fake_department_repository,
        fake_employee_repository
):

    device_service = DeviceService(
        fake_device_repository,
        fake_department_repository,
        fake_employee_repository)

    first_device = fake_device_repository.items[0]
    first_employee = fake_employee_repository.items[0]

    data = {'device_id': first_device.id, 'employee_id': first_employee.id}

    await device_service.add_employee(DeviceEmployeePostRequestSchema(**data))

    assert first_employee == first_device.employees[0]


async def test_device_service_can_get_record_in_access_control_table(access_control):

    device_employees_list = await access_control.device_service.get_employees(access_control.device.id)

    assert access_control.device.employees == device_employees_list


async def test_device_service_can_remove_record_in_access_control_table(access_control):

    await access_control.device_service.remove_employee(
        access_control.device.id,
        access_control.employee.id
    )

    assert access_control.device.employees == []




