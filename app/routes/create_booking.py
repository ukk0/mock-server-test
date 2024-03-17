from fastapi import APIRouter

router = APIRouter()


@router.post("/booking")
async def create_booking_mock_response():
    pass
