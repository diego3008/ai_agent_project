from app.agent import tools
import sys
from unittest.mock import patch


def test_sum():
    assert tools.sum.invoke({"num1": 2, "num2": 3}) == 5
    assert tools.sum.invoke({"num1": -1, "num2": 1}) == 0
    assert tools.sum.invoke({"num1": 0, "num2": 0}) == 0


def test_get_city_weather_success():
    mock_response = {
        "main": {"temp": 20},
        "weather": [{"description": "clear sky"}]
    }
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response
        result = tools.get_city_weather.invoke({"city": "London"})
        assert "The weather in London is 20 and clear sky" in result


def test_get_city_weather_api_key_error(monkeypatch):
    monkeypatch.setattr(tools, "OPENWEATHER_API", None)
    result = tools.get_city_weather.invoke({"city": "London"})
    assert "There was an error getting weather API key" in result 