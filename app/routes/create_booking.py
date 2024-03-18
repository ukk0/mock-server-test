import json

from fastapi import APIRouter, HTTPException, Query, Request, Response
from vcr import VCR

from app.utils.helpers import determine_which_cassettes_to_use, validate_that_requests_match

router = APIRouter()
vcr = VCR(cassette_library_dir="cassettes")

with open("mock_config.json") as config_file:
    config = json.load(config_file)


@router.post("/booking")
async def create_booking_mock_response(request: Request, mock: str = Query(...)) -> Response:
    cassette_file = determine_which_cassettes_to_use(mock)
    if not cassette_file:
        raise HTTPException(status_code=404, detail=f"Cassette for '{mock}' not found.")
    with vcr.use_cassette(f"cassettes/create_booking/{cassette_file}.yaml") as cassette:
        request_data = {
            "method": request.method,
            "url": str(request.url),
            "scheme": request.url.scheme,
            "host": request.client.host,
            "path": request.url.path,
            "headers": dict(request.headers),
            "body": await request.body(),
            "query": dict(request.query_params),
        }
        # Validate that request sufficiently matches existing cassette
        try:
            validate_that_requests_match(cassette, request_data)
        except AssertionError as exc:
            raise HTTPException(
                status_code=400, detail="Request data does not match existing cassette for booking creation."
            ) from exc

        # Return JSON response and status code from cassette
        response_data = cassette.responses[0]["body"]["string"]
        status_code = cassette.responses[0]["status"]["code"]
        return Response(content=response_data, media_type="application/json", status_code=status_code)
