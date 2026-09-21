from app.agents.router import route_request


class FakeModel:
    def with_structured_output(self, _schema):
        return self

    def invoke(self, _payload):
        class R:
            route = "general"
        return R()


def test_router_shape():
    result = route_request({"message": "hello", "model": FakeModel()})
    assert result["route"] == "general"
