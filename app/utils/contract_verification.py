import json
import os
from typing import Any

from vcr import VCR

from app.utils.api_client import TestAPI
from app.utils.exceptions import ContractVerificationError
from app.utils.helpers import get_all_dict_keys


class ContractVerifier:
    def __init__(self):
        self.cassettes_dir = "cassettes"
        self.create_booking_cassette = os.path.join(self.cassettes_dir, "create_booking_success.yaml")
        self.find_booking_cassette = os.path.join(self.cassettes_dir, "find_booking_success.yaml")
        self.delete_booking_cassette = os.path.join(self.cassettes_dir, "delete_booking_success.yaml")

    def load_cassette_responses(self):
        return {
            "create_booking": self.load_create_booking_response(self.create_booking_cassette),
            "find_booking": self.load_find_booking_response(self.find_booking_cassette),
            "delete_booking": self.load_delete_booking_status(self.delete_booking_cassette),
        }

    def load_create_booking_response(self, cassette_file) -> dict[str, Any]:
        with VCR(cassette_library_dir=self.cassettes_dir).use_cassette(cassette_file) as cassette:
            return json.loads(cassette.responses[0]["body"]["string"])

    def load_find_booking_response(self, cassette_file) -> dict[str, Any]:
        with VCR(cassette_library_dir=self.cassettes_dir).use_cassette(cassette_file) as cassette:
            return json.loads(cassette.responses[0]["body"]["string"])

    def load_delete_booking_status(self, cassette_file) -> dict[str, Any]:
        with VCR(cassette_library_dir=self.cassettes_dir).use_cassette(cassette_file) as cassette:
            return cassette.responses[0]["status"]["code"]

    @staticmethod
    def compare_responses(response, cassette_response) -> bool:
        return get_all_dict_keys(response) == get_all_dict_keys(cassette_response)

    def verify_contract(self):
        verified_contracts = []
        failed_contracts = []

        # Load cassette responses
        cassette_responses = self.load_cassette_responses()
        create_booking_cassette_response = cassette_responses["create_booking"]
        find_booking_cassette_response = cassette_responses["find_booking"]
        delete_booking_cassette_status = cassette_responses["delete_booking"]

        # Call API for new responses
        create_booking_response = TestAPI.create_booking().json()
        booking_id = create_booking_response["bookingid"]
        find_booking_response = TestAPI.get_booking_by_id(booking_id).json()
        delete_booking_status = TestAPI.delete_booking(booking_id).status_code

        # Compare responses
        if self.compare_responses(create_booking_response, create_booking_cassette_response):
            verified_contracts.append("Create booking")
        else:
            failed_contracts.append("Create booking")

        if self.compare_responses(find_booking_response, find_booking_cassette_response):
            verified_contracts.append("Find booking")
        else:
            failed_contracts.append("Find booking")

        if delete_booking_status == delete_booking_cassette_status:
            verified_contracts.append("Delete booking")
        else:
            failed_contracts.append("Delete booking")

        if failed_contracts:
            raise ContractVerificationError(failed_contracts)
        else:
            print(f"Contract verified successfully for cassettes: {', '.join(verified_contracts)}")


def test_contract_verification():
    verifier = ContractVerifier()
    verifier.verify_contract()
