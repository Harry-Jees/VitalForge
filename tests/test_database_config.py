import re
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import httpx
import pytest

from config import MYSQL_DATABASE
from database.supabase_credentials import (
    CredentialRetrievalError,
    fetch_database_credential,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FUNCTION_URL = (
    "https://jzqfajacvwiedsobnwyg.supabase.co/functions/v1/get-vitalforge-key"
)


def test_database_is_fixed_to_defaultdb():
    assert MYSQL_DATABASE == "defaultdb"


def test_supabase_function_configuration_uses_expected_endpoint():
    from config import VITALFORGE_FUNCTION_URL

    assert VITALFORGE_FUNCTION_URL == (
        "https://jzqfajacvwiedsobnwyg.supabase.co/functions/v1/get-vitalforge-key"
    )


def test_env_example_contains_function_configuration():
    env_example = (PROJECT_ROOT / ".env.example").read_text(encoding="utf-8")

    assert "VITALFORGE_APP_API_KEY=\n" in env_example
    assert (
        "VITALFORGE_FUNCTION_URL="
        "https://jzqfajacvwiedsobnwyg.supabase.co/functions/v1/get-vitalforge-key\n"
    ) in env_example


def test_schema_does_not_create_or_switch_databases():
    schema = (PROJECT_ROOT / "database" / "schema.sql").read_text(encoding="utf-8")
    assert not re.search(r"(?im)^\s*(?:CREATE\s+DATABASE\b|USE\b)", schema)


def test_fetches_credential_with_get_and_x_api_key(monkeypatch):
    response = Mock(status_code=200)
    response.json.return_value = {"credential": "mock-aiven-password"}
    get = Mock(return_value=response)
    monkeypatch.setattr("database.supabase_credentials.httpx.get", get)

    credential = fetch_database_credential("mock-app-key", FUNCTION_URL)

    assert credential == "mock-aiven-password"
    get.assert_called_once_with(
        FUNCTION_URL,
        headers={"x-api-key": "mock-app-key"},
        timeout=15.0,
    )
    response.raise_for_status.assert_called_once_with()


def test_supabase_key_takes_precedence_and_credential_is_cached(monkeypatch):
    import config

    fetch = Mock(return_value="mock-aiven-password")
    monkeypatch.setattr(config, "_ENV_MYSQL_PASSWORD", "")
    monkeypatch.setattr(config, "MYSQL_PASSWORD", "legacy-password")
    monkeypatch.setattr(config, "VITALFORGE_APP_API_KEY", "mock-app-key")
    monkeypatch.setattr(config, "VITALFORGE_FUNCTION_URL", FUNCTION_URL)
    monkeypatch.setattr(
        "database.supabase_credentials.fetch_database_credential",
        fetch,
    )
    monkeypatch.setattr(config, "_REMOTE_MYSQL_PASSWORD", None)

    assert config.get_mysql_password() == "mock-aiven-password"
    assert config.get_mysql_password() == "mock-aiven-password"
    fetch.assert_called_once_with("mock-app-key", FUNCTION_URL)


def test_database_connection_uses_resolved_password(monkeypatch):
    from database import connection

    database_connection = Mock()
    connect = Mock(return_value=database_connection)
    monkeypatch.setattr(connection, "get_mysql_password", Mock(return_value="mock-password"))
    monkeypatch.setattr(connection.mysql.connector, "connect", connect)

    assert connection.get_database_connection() is database_connection
    assert connect.call_args.kwargs["password"] == "mock-password"


def test_startup_connection_check_returns_safe_supabase_diagnostic(monkeypatch):
    from database import connection

    monkeypatch.setattr(
        connection,
        "_open_database_connection",
        Mock(side_effect=CredentialRetrievalError("Supabase returned HTTP 401.")),
    )

    assert connection.check_database_connection() == (
        False,
        "Supabase returned HTTP 401.",
    )


def test_startup_checks_database_before_creating_app(monkeypatch):
    events = Mock()
    events.attach_mock(Mock(return_value=(True, None)), "connection_check")
    events.attach_mock(Mock(), "app")
    monkeypatch.setitem(
        sys.modules,
        "screens",
        SimpleNamespace(VitalForgeApp=events.app),
    )
    import main

    root = Mock()
    root.winfo_screenwidth.return_value = 1920
    root.winfo_screenheight.return_value = 1080

    monkeypatch.setattr(main.tk, "Tk", Mock(return_value=root))
    monkeypatch.setattr(main, "check_database_connection", events.connection_check)
    monkeypatch.setattr(main, "VitalForgeApp", events.app)

    main.main()

    assert [call[0] for call in events.method_calls] == [
        "connection_check",
        "app",
    ]
    root.mainloop.assert_called_once_with()


def test_missing_api_key_does_not_make_request(monkeypatch):
    get = Mock()
    monkeypatch.setattr("database.supabase_credentials.httpx.get", get)

    with pytest.raises(CredentialRetrievalError, match="Missing VITALFORGE_APP_API_KEY"):
        fetch_database_credential("", FUNCTION_URL)

    get.assert_not_called()


def test_timeout_is_reported_without_request_details(monkeypatch):
    monkeypatch.setattr(
        "database.supabase_credentials.httpx.get",
        Mock(side_effect=httpx.TimeoutException("mock timeout")),
    )

    with pytest.raises(CredentialRetrievalError, match="Timed out") as error:
        fetch_database_credential("mock-app-key", FUNCTION_URL)

    assert "mock-app-key" not in str(error.value)


def test_http_error_is_reported_without_response_body(monkeypatch):
    response = httpx.Response(
        401,
        request=httpx.Request("GET", FUNCTION_URL),
        text="mock-app-key",
    )
    get = Mock(return_value=response)
    monkeypatch.setattr("database.supabase_credentials.httpx.get", get)

    with pytest.raises(CredentialRetrievalError, match="HTTP 401") as error:
        fetch_database_credential("mock-app-key", FUNCTION_URL)

    assert "mock-app-key" not in str(error.value)


def test_unauthorized_error_explains_gateway_jwt_setting(monkeypatch):
    response = httpx.Response(
        401,
        request=httpx.Request("GET", FUNCTION_URL),
        text="Unauthorized",
    )
    monkeypatch.setattr(
        "database.supabase_credentials.httpx.get",
        Mock(return_value=response),
    )

    with pytest.raises(CredentialRetrievalError, match="platform JWT verification"):
        fetch_database_credential("mock-app-key", FUNCTION_URL)


@pytest.mark.parametrize(
    "payload",
    [
        [],
        {},
        {"credential": ""},
        {"credential": None},
        {"credential": 123},
    ],
)
def test_malformed_payload_is_rejected(monkeypatch, payload):
    response = Mock(status_code=200)
    response.json.return_value = payload
    monkeypatch.setattr(
        "database.supabase_credentials.httpx.get",
        Mock(return_value=response),
    )

    with pytest.raises(CredentialRetrievalError):
        fetch_database_credential("mock-app-key", FUNCTION_URL)


def test_invalid_json_is_rejected(monkeypatch):
    response = Mock(status_code=200)
    response.json.side_effect = ValueError("mock-app-key")
    monkeypatch.setattr(
        "database.supabase_credentials.httpx.get",
        Mock(return_value=response),
    )

    with pytest.raises(CredentialRetrievalError, match="invalid JSON") as error:
        fetch_database_credential("mock-app-key", FUNCTION_URL)

    assert "mock-app-key" not in str(error.value)


def test_function_url_must_be_the_configured_https_endpoint(monkeypatch):
    get = Mock()
    monkeypatch.setattr("database.supabase_credentials.httpx.get", get)

    with pytest.raises(CredentialRetrievalError, match="Invalid Supabase function URL"):
        fetch_database_credential("mock-app-key", "https://example.invalid/function")

    get.assert_not_called()
