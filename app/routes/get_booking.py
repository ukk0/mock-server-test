from fastapi import APIRouter

router = APIRouter()


@router.get("/booking/{booking_id}")
async def get_booking_mock_response():
    pass
