# tests/test_search.py
from unittest.mock import patch, MagicMock
from nocp.__main__ import Navidrome


def _make_nav():
    return Navidrome("http://localhost:4533", "user", "nocp", "pass", "1.16.1")


def test_search_hits_search3_view():
    nav = _make_nav()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "subsonic-response": {
            "searchResult3": {
                "artist": [{"id": "1", "name": "Artist One"}],
                "album": [],
                "song": [],
            }
        }
    }
    with patch("nocp.__main__.requests.get", return_value=mock_resp) as mock_get:
        result = nav.search("Artist One")

    url_called = mock_get.call_args[0][0]
    params_called = mock_get.call_args[1]["params"]
    assert "search3.view" in url_called
    assert params_called["query"] == "Artist One"
    assert params_called["artistCount"] == 5
    assert params_called["albumCount"] == 10
    assert params_called["songCount"] == 20
    assert result["subsonic-response"]["searchResult3"]["artist"][0]["name"] == "Artist One"


def test_search_returns_empty_sections_when_no_results():
    nav = _make_nav()
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "subsonic-response": {"searchResult3": {}}
    }
    with patch("nocp.__main__.requests.get", return_value=mock_resp):
        result = nav.search("nothing")

    sr = result["subsonic-response"]["searchResult3"]
    assert sr.get("artist", []) == []
    assert sr.get("album", []) == []
    assert sr.get("song", []) == []
