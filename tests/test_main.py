"""Testing the main methods."""

from crosstown_traffic.models import TrafficRequest


def test_traffic_request_parses():
    request = TrafficRequest.model_validate(
        {
            "location": {
                "address": "1 Main St",
                "longitude": -73.0,
                "altitude": 10.0,
                "latitude": 42.0,
                "battery": "80%",
                "ip": "10.0.0.2",
                "network": "wifi",
            },
            "trigger": "arrive",
        }
    )
    assert request.location.latitude == 42.0
    assert request.trigger == "arrive"
