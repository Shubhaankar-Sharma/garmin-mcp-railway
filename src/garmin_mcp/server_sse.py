"""
SSE-enabled MCP Server for Garmin Connect Data - for remote hosting
"""

import os
import sys

import requests
from mcp.server.fastmcp import FastMCP

from garth.exc import GarthHTTPError
from garminconnect import Garmin, GarminConnectAuthenticationError

# Import all modules
from garmin_mcp import activity_management
from garmin_mcp import health_wellness
from garmin_mcp import user_profile
from garmin_mcp import devices
from garmin_mcp import gear_management
from garmin_mcp import weight_management
from garmin_mcp import challenges
from garmin_mcp import training
from garmin_mcp import workouts
from garmin_mcp import data_management
from garmin_mcp import womens_health


def get_mfa() -> str:
    """Get MFA code from user input"""
    # In SSE mode, MFA cannot be interactive
    # Users must pre-configure OAuth tokens
    raise RuntimeError(
        "MFA not supported in SSE mode. Please pre-configure OAuth tokens by running the server locally first."
    )


# Get credentials from environment
email = os.environ.get("GARMIN_EMAIL")
email_file = os.environ.get("GARMIN_EMAIL_FILE")
if email and email_file:
    raise ValueError(
        "Must only provide one of GARMIN_EMAIL and GARMIN_EMAIL_FILE, got both"
    )
elif email_file:
    with open(email_file, "r") as f:
        email = f.read().rstrip()

password = os.environ.get("GARMIN_PASSWORD")
password_file = os.environ.get("GARMIN_PASSWORD_FILE")
if password and password_file:
    raise ValueError(
        "Must only provide one of GARMIN_PASSWORD and GARMIN_PASSWORD_FILE, got both"
    )
elif password_file:
    with open(password_file, "r") as f:
        password = f.read().rstrip()

# For Railway deployment, we'll use environment variable for tokens
tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
tokenstore_base64 = os.getenv("GARMINTOKENS_BASE64") or "~/.garminconnect_base64"


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    try:
        # Using Oauth1 and OAuth2 token files from directory
        print(
            f"Trying to login to Garmin Connect using token data from directory '{tokenstore}'...\n"
        , file=sys.stderr)

        garmin = Garmin()
        garmin.login(tokenstore)

    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        print(
            "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        , file=sys.stderr)
        try:
            garmin = Garmin(
                email=email, password=password, is_cn=False, prompt_mfa=get_mfa
            )
            garmin.login()
            # Save Oauth1 and Oauth2 token files to directory for next login
            garmin.garth.dump(tokenstore)
            print(
                f"Oauth tokens stored in '{tokenstore}' directory for future use. (first method)\n"
            , file=sys.stderr)
            # Encode Oauth1 and Oauth2 tokens to base64 string and safe to file for next login (alternative way)
            token_base64 = garmin.garth.dumps()
            dir_path = os.path.expanduser(tokenstore_base64)
            with open(dir_path, "w") as token_file:
                token_file.write(token_base64)
            print(
                f"Oauth tokens encoded as base64 string and saved to '{dir_path}' file for future use. (second method)\n"
            , file=sys.stderr)
        except (
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectAuthenticationError,
            requests.exceptions.HTTPError,
        ) as err:
            print(err, file=sys.stderr)
            return None

    return garmin


def create_mcp_server():
    """Initialize and configure the MCP server"""
    # Initialize Garmin client
    garmin_client = init_api(email, password)
    if not garmin_client:
        raise RuntimeError("Failed to initialize Garmin Connect client")

    print("Garmin Connect client initialized successfully.", file=sys.stderr)

    # Configure all modules with the Garmin client
    activity_management.configure(garmin_client)
    health_wellness.configure(garmin_client)
    user_profile.configure(garmin_client)
    devices.configure(garmin_client)
    gear_management.configure(garmin_client)
    weight_management.configure(garmin_client)
    challenges.configure(garmin_client)
    training.configure(garmin_client)
    workouts.configure(garmin_client)
    data_management.configure(garmin_client)
    womens_health.configure(garmin_client)

    # Create the MCP app
    mcp = FastMCP("Garmin Connect v1.0")

    # Register tools from all modules
    mcp = activity_management.register_tools(mcp)
    mcp = health_wellness.register_tools(mcp)
    mcp = user_profile.register_tools(mcp)
    mcp = devices.register_tools(mcp)
    mcp = gear_management.register_tools(mcp)
    mcp = weight_management.register_tools(mcp)
    mcp = challenges.register_tools(mcp)
    mcp = training.register_tools(mcp)
    mcp = workouts.register_tools(mcp)
    mcp = data_management.register_tools(mcp)
    mcp = womens_health.register_tools(mcp)

    # Add activity listing tool directly to the app
    @mcp.tool()
    async def list_activities(limit: int = 5) -> str:
        """List recent Garmin activities"""
        try:
            activities = garmin_client.get_activities(0, limit)

            if not activities:
                return "No activities found."

            result = f"Last {len(activities)} activities:\n\n"
            for idx, activity in enumerate(activities, 1):
                result += f"--- Activity {idx} ---\n"
                result += f"Activity: {activity.get('activityName', 'Unknown')}\n"
                result += (
                    f"Type: {activity.get('activityType', {}).get('typeKey', 'Unknown')}\n"
                )
                result += f"Date: {activity.get('startTimeLocal', 'Unknown')}\n"
                result += f"ID: {activity.get('activityId', 'Unknown')}\n\n"

            return result
        except Exception as e:
            return f"Error retrieving activities: {str(e)}"

    return mcp


# Create the MCP server
mcp_server = create_mcp_server()

# Create ASGI app using FastMCP's sse_app() method
# This returns a Starlette application that can be run with uvicorn
app = mcp_server.sse_app()


def main():
    """Entry point for the SSE server"""
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Garmin MCP Server on port {port}", file=sys.stderr)
    print(f"SSE endpoint will be available at: http://0.0.0.0:{port}/sse", file=sys.stderr)

    # Run the ASGI app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
