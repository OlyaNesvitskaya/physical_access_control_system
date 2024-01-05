from fastapi import APIRouter, Depends
from services import EventService
from schemas.event_schema import EventPostSchema

event_router = APIRouter(
     tags=["Event"]
)


@event_router.get("/drop_in/{card_id}/{imei}", response_model=EventPostSchema)
async def attempt_to_drop_in_the_door(
        card_id: int,
        imei: str,
        event_service: EventService = Depends()
) -> dict:

    is_possible = await event_service.check_entry_possibility(card_id, imei)
    return is_possible
