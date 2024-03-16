import vcr

from app.utils.api_client import TestAPI

vcr_config = vcr.VCR(
    cassette_library_dir="../../cassettes",
    record_mode="once",
    filter_headers=[("Authorization", "")],
    match_on=["method", "scheme", "host", "port", "path", "query", "headers"],
    decode_compressed_response=True,
).__dict__


def record_cassettes():
    booking_id = ""

    @vcr.use_cassette("booking_create_success.yaml", **vcr_config)
    def record_booking_create_success():
        nonlocal booking_id
        booking_id = TestAPI.create_booking().json()["bookingid"]

    @vcr.use_cassette("find_booking_success.yaml", **vcr_config)
    def record_find_booking_success():
        TestAPI.get_booking_by_id(booking_id=booking_id)

    @vcr.use_cassette("delete_booking_success.yaml", **vcr_config)
    def record_delete_booking_success():
        TestAPI.delete_booking(booking_id=booking_id)

    record_booking_create_success()
    record_find_booking_success()
    record_delete_booking_success()


if __name__ == "__main__":
    record_cassettes()
