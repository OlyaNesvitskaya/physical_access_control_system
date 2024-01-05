from datetime import date
from fastapi import Depends
from typing import NamedTuple

from models import Event
from repository import DeviceRepository, EventRepository, EmployeeRepository


class EventService:
    employee_repository: EmployeeRepository
    device_repository: DeviceRepository
    event_repository: EventRepository

    def __init__(
        self,
        device_repository: DeviceRepository = Depends(),
        event_repository: EventRepository = Depends(),
        employee_repository: EmployeeRepository = Depends(),
    ) -> None:

        self.device_repository = device_repository
        self.event_repository = event_repository
        self.employee_repository = employee_repository

    class EntryPossibility(NamedTuple):
        success: bool = False
        employee_id: int | None = None
        device_id: int | None = None

    async def create(
        self, event: EntryPossibility
    ) -> None:
        await self.event_repository.create(
            Event(device_id=event.device_id, employee_id=event.employee_id, success=event.success))

    async def check_entry_possibility(self, card_id: int, imei: str):
        result = await self.__check_if_access_is_permitted(card_id, imei)
        await self.create(result)
        return {'entry': ('Admission are prohibited', 'Admission are permitted')[result.success]}

    async def __check_if_access_is_permitted(self, card_id: int, imei: str):

        employee = await self.employee_repository.get_by_card_id(card_id)
        if not employee:
            return self.EntryPossibility()
        if employee.card_finish_date < date.today():
            return self.EntryPossibility(False, employee.id, None)
        device = await self.device_repository.get_device_id_and_device_opened(imei)

        if device:
            if device.opened:
                return self.EntryPossibility(True, employee.id, device.id)
            access = any(i.id == device.id for i in employee.devices)
            if access:
                return self.EntryPossibility(True, employee.id, device.id)
            return self.EntryPossibility(False, employee.id, device.id)

        return self.EntryPossibility(False, employee.id, None)




