from app.connectors.government_mock import GovernmentMockConnector
from app.connectors.api_bid_mock import ApiBidMockConnector
from app.connectors.commercial_mock import CommercialMockConnector

CONNECTORS = {
    "government_mock": GovernmentMockConnector(),
    "api_bid_mock": ApiBidMockConnector(),
    "commercial_mock": CommercialMockConnector(),
}

def get_connectors(include: list[str] | None = None):
    if include:
        return [CONNECTORS[k] for k in include if k in CONNECTORS]
    return list(CONNECTORS.values())
