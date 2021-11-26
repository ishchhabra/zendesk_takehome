import json
import os

import pytest
import responses


@pytest.fixture(scope="function")
def responses_mocker():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture(scope="function")
def fixtures(request):
    module_dir = os.path.split(request.module.__file__)[0]
    fixture_name = f"{request.module.__name__}.json"
    fixture_path = os.path.join(module_dir, "fixtures", fixture_name)

    return json.load(open(fixture_path, "r"))


@pytest.fixture()
def mock_responses(responses_mocker: responses.RequestsMock, fixtures: str):
    for fixture in fixtures:
        responses_mocker.add(
            method=fixture["request"]["method"],
            url=fixture["request"]["url"],
            json=fixture["response"]["body"],
        )
