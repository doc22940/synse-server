"""Test the 'synse.routes.core' Synse Server module's plugins route."""
# pylint: disable=redefined-outer-name,unused-argument

import asynctest
import pytest
from sanic.response import HTTPResponse

import synse.commands
from synse import config
from synse.routes.core import plugins_route
from synse.scheme.base_response import SynseResponse


def mockreturn():
    """Mock method that will be used in monkeypatching the command."""
    r = SynseResponse()
    r.data = []
    return r


@pytest.fixture()
def mock_plugins(monkeypatch):
    """Fixture to monkeypatch the underlying Synse command."""
    mock = asynctest.CoroutineMock(synse.commands.get_plugins, side_effect=mockreturn)
    monkeypatch.setattr(synse.commands, 'get_plugins', mock)
    return mock_plugins


@pytest.fixture()
def no_pretty_json():
    """Fixture to ensure basic JSON responses."""
    config.options['pretty_json'] = False


@pytest.mark.asyncio
async def test_synse_config_route(mock_plugins, no_pretty_json):
    """Test successfully getting the plugins."""

    result = await plugins_route(None)

    assert isinstance(result, HTTPResponse)
    assert result.body == b'[]'
    assert result.status == 200
