from typing import TypeVar, Any, Callable, AsyncGenerator, NamedTuple
from datetime import date
import pytest
from fastapi import FastAPI
from sqlalchemy import exc
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from httpx import AsyncClient

from models.base_model import Base
from models import Department, Employee, Device, User
from repository.repository_meta import RepositoryMeta
from schemas.device_schema import DeviceEmployeePostRequestSchema
from services import DeviceService
from services.user_service import HashingMixin

DATABASE_URL = "sqlite+aiosqlite:///async_test.db"

async_engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
test_async_session = async_sessionmaker(async_engine, expire_on_commit=False)


@pytest.fixture(scope='module')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='module')
async def session(anyio_backend) -> AsyncSession:
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with test_async_session(bind=connection) as session:
            yield session


@pytest.fixture(scope='module')
def override_get_db(session, anyio_backend) -> Callable:
    async def _override_get_db():
        yield session

    return _override_get_db


@pytest.fixture(scope='module')
def test_app(anyio_backend, override_get_db: Callable) -> FastAPI:
    from core.database import get_db_connection
    from main import app

    app.dependency_overrides[get_db_connection] = override_get_db
    return app


@pytest.fixture(scope='module')
async def async_client(anyio_backend, test_app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=test_app, base_url="http://localhost:8080") as ac:
        yield ac


@pytest.fixture(name='superuser', scope='module')
async def get_superuser(anyio_backend, session):
    superuser = User(
        id=1,
        email='superuser@gmail.com',
        hashed_password=HashingMixin().get_password_hash('superuser'),
        is_superuser=True)
    session.add(superuser)
    await session.commit()
    return superuser


@pytest.fixture(name='not_superuser', scope='module')
async def get_user(anyio_backend, session):
    user = User(
        id=2,
        email='not_superuser@gmail.com',
        hashed_password=HashingMixin().get_password_hash('not_superuser'),
        is_superuser=False)
    session.add(user)
    await session.commit()
    return user


@pytest.fixture(name='user3', scope='module')
async def get_user3(anyio_backend, session):
    user = User(
        id=3,
        email='user3@gmail.com',
        hashed_password=HashingMixin().get_password_hash('user3'),
        is_superuser=False)
    session.add(user)
    await session.commit()
    return user


@pytest.fixture(name='not_superuser_token', scope='module')
async def get_not_superuser_token(async_client, not_superuser):
    user_token = await async_client.post(
        '/token', data={'username': 'not_superuser@gmail.com', 'password': 'not_superuser'})
    return user_token.json()['access_token']


@pytest.fixture(scope='module')
async def authorized_not_superuser(anyio_backend, test_app: FastAPI, not_superuser_token):
    async with AsyncClient(app=test_app, base_url="http://localhost:8080") as ac:
        ac.headers = {**ac.headers, "Authorization": f'Bearer {not_superuser_token}'}
        yield ac


@pytest.fixture(name='superuser_token', scope='module')
async def get_superuser_token(anyio_backend, async_client, superuser):
    user_token = await async_client.post('/token', data={'username': 'superuser@gmail.com', 'password': 'superuser'})
    return user_token.json()['access_token']


@pytest.fixture(scope='module')
async def authorized_superuser(async_client, superuser_token):
    async_client.headers = {**async_client.headers, "Authorization": f'Bearer {superuser_token}'}
    return async_client


@pytest.fixture(scope='module', name='departments')
def get_departments():
    return [
        Department(id=1, name='new_department1'),
        Department(id=2, name='new_department2'),
        Department(id=3, name='new_department3')
    ]


@pytest.fixture(scope='module', name='employees')
def get_employees():
    return [
        Employee(id=1, name='Anna', surname='Karenina', department_id=1, card_id=11111111,
                 card_start_date=date.today(), card_finish_date=date.today()),

        Employee(id=2, name='Jane', surname='Austen', department_id=1, card_id=2222222,
                 card_start_date=date.today(), card_finish_date=date.today()),

        Employee(id=3, name='Aleksander', surname='Pushkin', department_id=3, card_id=3333333,
                 card_start_date=date.today(), card_finish_date=date.today())
    ]


@pytest.fixture(scope='module', name='devices')
def get_devices():
    return [
        Device(id=1, name='Contact reader №1', imei='111111qwerty', route='enter', department_id=1),
        Device(id=2, name='Contact reader №2', imei='222222qwerty', route='enter', department_id=2),
        Device(id=3, name='Contact reader №3', imei='333333qwerty', route='enter', department_id=3)
    ]


@pytest.fixture(name="department", scope='module')
async def insert_department(anyio_backend, session) -> Department:

    new_department = Department(id=1, name="dep1")

    session.add(new_department)
    await session.commit()

    return new_department


@pytest.fixture(name='employee', scope='module')
async def insert_employee(anyio_backend, session, department) -> Employee:
    employee = Employee(id=1, name='Anna', surname='Karenina', department_id=department.id, card_id=11111111,
                        card_start_date=date.today(), card_finish_date=date.today())
    session.add(employee)
    await session.commit()
    return employee


@pytest.fixture(name='device', scope='module')
async def insert_device(anyio_backend, session, department) -> Device:

    device = Device(id=1, name='Contact reader №1', imei='111111qwerty',
                    route='enter', department_id=department.id, opened=False)
    session.add(device)
    await session.commit()
    await session.refresh(device, attribute_names=['employees'])
    return device


ModelType = TypeVar("ModelType", bound=Any)


@pytest.mark.usefixtures("anyio_backend")
class FakeRepository(RepositoryMeta):
    unique_field: tuple = None

    def __init__(self, items: list = None) -> None:
        self._items = (items, [])[items is None]

    @property
    def items(self):
        return self._items

    async def create(self, item: ModelType) -> ModelType:
        for obj in self._items:
            for field in self.unique_field:
                if getattr(item, field) == getattr(obj, field):
                    raise exc.IntegrityError('Error unique item', 'params', 'orig')
        self._items.append(item)
        return item

    async def get(self, item_id: ModelType, bound=True) -> ModelType | None:
        search_obj = (obj for obj in self._items if obj.id == item_id)
        try:
            return next(search_obj)
        except StopIteration:
            return

    async def update(self, item: ModelType) -> ModelType:

        class UniqueErrorOrig:
            args = ('Unique constraint',)

        for obj in self._items:
            if getattr(obj, 'id') != getattr(item, 'id'):
                for field in self.unique_field:
                    if getattr(item, field) == getattr(obj, field):
                        raise exc.IntegrityError('non-unique item', 'params', UniqueErrorOrig)

        return item

    async def delete(self, item: ModelType) -> None:
        self._items.remove(item)

    async def list(self, page_size: int, start_index: int):
        return self._items[start_index:page_size]


@pytest.mark.usefixtures("anyio_backend")
class FakeDepartmentRepository(FakeRepository):
    unique_field = 'name',


@pytest.mark.usefixtures("anyio_backend")
class FakeEmployeeRepository(FakeRepository):
    unique_field = "card_id",

    async def get_by_card_id(self, card_id: int) -> Employee:
        for employee in self._items:
            if getattr(employee, 'card_id') == card_id:
                return employee

    async def update(self, item: ModelType) -> ModelType:

        class UniqueErrorOrig:
            args = ('Unique constraint',)

        class DateErrorOrig:
            args = ('Check constraint',)

        for obj in self._items:
            if getattr(obj, 'id') != getattr(item, 'id'):
                for field in self.unique_field:
                    if getattr(item, field) == getattr(obj, field):
                        raise exc.IntegrityError('non-unique item', 'params', UniqueErrorOrig)
            if obj.card_start_date > obj.card_finish_date:
                raise exc.IntegrityError('incorrect date', 'params', DateErrorOrig)

        return item


@pytest.mark.usefixtures("anyio_backend")
class FakeDeviceRepository(FakeRepository):
    unique_field = "imei",

    async def get_device_id_and_device_opened(self, imei: str):
        for device in self._items:
            if getattr(device, 'imei') == imei:
                return Device(id=device.id, opened=device.opened)


@pytest.mark.usefixtures("anyio_backend")
class FakeEventRepository(FakeRepository):
    unique_field = tuple()


@pytest.mark.usefixtures("anyio_backend")
class FakeUserRepository(FakeRepository):
    unique_field = 'email',


@pytest.fixture(scope='module', name='fake_employee_repository')
def get_employee_repository(anyio_backend, employees) -> FakeRepository:
    return FakeEmployeeRepository(employees)


@pytest.fixture(scope='module', name='fake_department_repository')
def get_department_repository(anyio_backend, departments) -> FakeRepository:
    return FakeDepartmentRepository(departments)


@pytest.fixture(scope='module', name='fake_device_repository')
def get_device_repository(anyio_backend, devices) -> FakeRepository:
    return FakeDeviceRepository(devices)


@pytest.fixture(scope='module', name='fake_event_repository')
def get_event_repository(anyio_backend) -> FakeRepository:
    return FakeEventRepository()


@pytest.fixture(scope='module', name='fake_user_repository')
def get_user_repository(anyio_backend) -> FakeRepository:
    return FakeUserRepository(
        [
            User(id=1, email='user1@gmail.com', hashed_password=HashingMixin().get_password_hash('user1'),
                 is_superuser=True),
            User(id=2, email='user2@gmail.com', hashed_password=HashingMixin().get_password_hash('user2'),
                 is_superuser=False),
        ]
    )


class BoundDataAccessControlTable(NamedTuple):
    employee: Employee
    device: Device
    device_service: DeviceService


@pytest.fixture(name='access_control', scope='module')
async def add_record_in_access_control_table(
        fake_device_repository,
        fake_department_repository,
        fake_employee_repository,
        anyio_backend
):

    device_service = DeviceService(fake_device_repository,
                                   fake_department_repository,
                                   fake_employee_repository)

    first_device = fake_device_repository.items[0]
    first_employee = fake_employee_repository.items[0]

    data = {'device_id': first_device.id, 'employee_id': first_employee.id}

    await device_service.add_employee(DeviceEmployeePostRequestSchema(**data))
    return BoundDataAccessControlTable(first_employee, first_device, device_service)

