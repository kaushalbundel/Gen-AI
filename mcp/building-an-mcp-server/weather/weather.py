from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

#starting FastMCP server
# FASTMCP uses type hints and doc strings to generate tool definiions, making it easy to create and maintain MCP tools
mcp = FastMCP("weather") # weather is the server name

# constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0" # agent version is defined

### Creating helper function to query weather service API

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """
    Make a request to NWS API with proper error handling
    """
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}

    async with httpx.AsyncClient() as client:
        try:
            response  = await client.get(url=url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()

        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """
    Format the alert response in a readable manner.
    The response will be in json. we are parsing json and getting relavant terms.
    """
    props = feature["properties"]
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions available")}
"""

# Tool execution handler
# This peice of code provides the tool needed to the client to perform some designated work
# Like in this example, when we want a real time weather update the tool execution handler requests the API and shares the data for the client to process
# Understanding the decorator
## This is essentially a function. As the MCP server starts the decorator takes the function and registers into an internal lookup table 
## When the client needs this function, the client checks this table, finds out the function and executes it. The client understands the function arguments and provides them arguments accordingly. The function is executed and the results are then packaged back in valid json-rpc format and sent to the client
## The function needs two things: "A string identifier to the function", and arguments to the function
## The function is an async function since it usually involves connecting with some data source/api/opening, reading from a file
## There are some best practices involved in naming and creating such decorators: read up (https://oneuptime.com/blog/post/2026-01-30-tool-execution/view) (https://github.com/ComposioHQ/awesome-claude-skills/blob/master/mcp-builder/reference/mcp_best_practices.md?plain=1)
## The ideal return value is a list of content objects (usually TextContent). Text Contact object is similar to a dictionary that has two bits of information, the type of the incoming data and the actual data itself. This helps the client to parse the data in a better way
## example: 
## from mcp import types
# ## return [
#     types.TextContent(type="text", text="Here is the graph you requested:"),
#     types.ImageContent(type="image", data="base64_encoded_string", mime_type="image/png")
# ]
## Be sure to handle the errors gracefully. Also try to limit the length of output, summarise if necessary.

# creating tool execution handler
# refer the return format for the function above. The way it is done here is not ideal. This can be improved.
@mcp.tool()
async def get_alerts(state: str):
    """
    Get weather alerts for a US state.
    
    Args:
        State: Two letter US state code (eg. CA, NY)
    """

    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url=url)

    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No Active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n-----\n".join(alerts) # format is string


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get weather forcast for a location.

    Args:
        latitude
        Longitude
    """

    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to get forecast data for this location."

    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(url=forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    periods = forecast_data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:
        forecast = f"""
{period["name"]}: 
Temperature: {period["temperature"]} deg {period["temperatureUnit"]}
Wind: {period["windSpeed"]} {period["windDirection"]}
Forecast: {period["detailedForecast"]}
"""
    
        forecasts.append(forecast)
    
    return "\n----\n".join(forecasts)

#running the server code
def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()