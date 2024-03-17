class ContractVerificationError(Exception):
    def __init__(self, failed_contracts: list):
        super().__init__(f"Contract verification failed for cassettes: {', '.join(failed_contracts)}")
