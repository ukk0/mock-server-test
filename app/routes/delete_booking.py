from fastapi import APIRouter

router = APIRouter()


@router.delete("/booking/{booking_id}")
async def delete_booking_mock_response():
    pass
