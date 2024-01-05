import asyncio
from sys import argv
from sqlalchemy import text

from models import Department, Device, Employee, User
from core.database import async_session
from models.base_model import Base
from services.user_service import HashingMixin
from core.environment import settings

all_departments = [
    Department(name='Human Resources'),
    Department(name='Accounting and Finance'),
    Department(name='IT'),
    Department(name='Marketing'),
    Department(name='Administration')
]


all_employees = [
    Employee(name='Anna', surname='Karenina', department_id=1, card_id=11111111),
    Employee(name='Fedor', surname='Dostoevskyi', department_id=2, card_id=2222222),
    Employee(name='Aleksander', surname='Pushkin', department_id=3, card_id=3333333),
]


all_devices = [
    Device(name='Contact reader №1', imei='111111qwerty', route='enter', department_id=1,
           employees=[all_employees[0]]),
    Device(name='Contact reader №2', imei='222222qwerty', route='enter', department_id=2,
           employees=[all_employees[0], all_employees[1]]),
    Device(name='Contact reader №3', imei='333333qwerty', route='enter', department_id=3,
           employees=[all_employees[0], all_employees[2]]),
    Device(name='Contact reader №4', imei='444444qwerty', route='enter', department_id=4,
           employees=[all_employees[0]]),
    Device(name='Contact reader №5', imei='555555qwerty', route='enter', department_id=5, opened=True),
]

superuser = User(
    email=settings.FIRST_SUPERUSER,
    hashed_password=HashingMixin.get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
    is_superuser=True
)


async def create_initial_data():
    async with async_session() as session:
        session.add_all(all_departments + all_employees+all_employees + [superuser])
        await session.commit()


async def delete_data_from_all_tables():
    async with async_session() as session:
        for table in Base.metadata.tables:
            await session.execute(text(f'DELETE FROM {table}'))
        await session.commit()


def main(task):
    if task == 'create':
        asyncio.run(create_initial_data())
    elif task == 'drop':
        asyncio.run(delete_data_from_all_tables())


if __name__ == '__main__':
    main(argv[1] if len(argv) == 2 else None)




