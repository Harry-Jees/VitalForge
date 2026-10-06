"""Retrieve the database credential from the configured Supabase Edge Function."""

from urllib.parse import urlsplit

import httpx


class CredentialRetrievalError(RuntimeError):
    """Raised when the Supabase function cannot safely provide a credential."""


_FUNCTION_HOST = "jzqfajacvwiedsobnwyg.supabase.co"
_FUNCTION_PATH = "/functions/v1/get-vitalforge-key"


def fetch_database_credential(api_key: str, function_url: str) -> str:
    """Fetch the Aiven credential using the Edge Function's GET/x-api-key contract."""
    if not api_key.strip():
        raise CredentialRetrievalError(
            "Missing VITALFORGE_APP_API_KEY environment variable."
        )

    try:
        parsed_url = urlsplit(function_url)
        port = parsed_url.port
    except ValueError:
        raise CredentialRetrievalError(
            "Invalid Supabase function URL configuration."
        ) from None

    if (
        parsed_url.scheme != "https"
        or parsed_url.hostname != _FUNCTION_HOST
        or parsed_url.path != _FUNCTION_PATH
        or port is not None
        or parsed_url.username is not None
        or parsed_url.password is not None
        or parsed_url.query
        or parsed_url.fragment
    ):
        raise CredentialRetrievalError("Invalid Supabase function URL configuration.")

    try:
        response = httpx.get(
            function_url,
            headers={"x-api-key": api_key},
            timeout=15.0,
        )
    except httpx.TimeoutException:
        raise CredentialRetrievalError(
            "Timed out retrieving the database credential."
        ) from None
    except httpx.RequestError:
        raise CredentialRetrievalError(
            "Could not reach the Supabase credential function."
        ) from None

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as error:
        if error.response.status_code == 401:
            raise CredentialRetrievalError(
                "Supabase returned HTTP 401. Check the function API key and, "
                "if using x-api-key authentication, disable platform JWT "
                "verification for this function."
            ) from None
        if error.response.status_code == 503:
            raise CredentialRetrievalError(
                "Supabase returned HTTP 503. The function's required secrets "
                "are not configured."
            ) from None
        raise CredentialRetrievalError(
            f"Supabase credential function returned HTTP {error.response.status_code}."
        ) from None

    if response.status_code != 200:
        raise CredentialRetrievalError(
            f"Supabase credential function returned HTTP {response.status_code}."
        )

    try:
        payload = response.json()
    except ValueError:
        raise CredentialRetrievalError(
            "Supabase credential function returned invalid JSON."
        ) from None

    if not isinstance(payload, dict):
        raise CredentialRetrievalError(
            "Supabase credential function returned an invalid response."
        )

    credential = payload.get("credential")
    if not isinstance(credential, str) or not credential.strip():
        raise CredentialRetrievalError(
            "Supabase credential function response did not contain a credential."
        )

    return credential
