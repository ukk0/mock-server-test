import uvicorn
from fastapi import FastAPI

from app.routes import create_booking, delete_booking, get_booking, ping

app = FastAPI()

app.include_router(create_booking.router)
app.include_router(delete_booking.router)
app.include_router(get_booking.router)
app.include_router(ping.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
