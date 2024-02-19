import os
from dotenv import load_dotenv
import httpx
import json
import asyncio


import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
tree = bot.tree

load_dotenv()

bot_token: str = os.getenv("DISCORD_BOT_TOKEN")
api_base_url: str = os.getenv("API_BASE_URL")

if bot_token is None or api_base_url is None:
    raise ValueError(
        "One or more environment variables are missing. Make sure to add them to the .env file."
    )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")


@bot.hybrid_command()
async def ping(ctx: commands.Context) -> None:
    """
    Pong!
    """
    await ctx.defer()

    # Calculate latency in milliseconds
    latency_ms = bot.latency * 1000

    # Determine the color based on latency
    if latency_ms > 100:  # If latency is greater than 100 ms
        color = discord.Color.red()
    elif latency_ms > 50:  # If latency is greater than 50 ms
        color = discord.Color.orange()
    else:  # If latency is 50 ms or lower
        color = discord.Color.green()

    # Create the embed with the determined color
    embed = discord.Embed(
        title="Pong!",
        color=color,
        description=f"Latency: {latency_ms} ms",
    )

    await ctx.send(embed=embed)


@bot.hybrid_command()
async def list_operations(ctx: commands.Context) -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_base_url + "/openapi.json")
            response.raise_for_status()
            openapi_data = response.json()

        embed = discord.Embed(
            title="Available API Operations", color=discord.Color.blue()
        )

        for path, details in openapi_data["paths"].items():
            http_methods = ", ".join(details.keys())
            parameters = ", ".join(details.get("parameters", []))
            description = details.get(
                "description", "No description available."
            )

            embed.add_field(
                name=f"Path: {path}",
                value=f"**HTTP Methods:** {http_methods}\n**Parameters:** {parameters}\n**Description:** {description}",
                inline=False,
            )

        await ctx.send(embed=embed)

    except httpx.HTTPError as e:
        # Handle HTTP errors
        embed = discord.Embed(
            title="Error",
            description=f"Failed to fetch OpenAPI file: {str(e)}",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)

    except json.JSONDecodeError:
        # Handle JSON decode error
        embed = discord.Embed(
            title="Error",
            description="Failed to parse OpenAPI file. Check if it is a valid JSON.",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)

    except Exception as e:
        # Handle other exceptions
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred: {str(e)}",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


@bot.hybrid_command()
async def call_api(ctx: commands.Context, route: str) -> None:
    """
    Call an API route.

    Parameters:
      - route (str): The API route to call.

    Example:
      !call_api example
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_base_url + route)
            response.raise_for_status()
            result = response.text

        embed = discord.Embed(
            title="API Response", color=discord.Color.green()
        )
        embed.add_field(
            name="Route",
            value=f"`{route}`",
            inline=False,
        )
        embed.add_field(
            name="Response",
            value=f"```json\n{result}\n```",
            inline=False,
        )

        await ctx.send(embed=embed)

    except httpx.HTTPError as e:
        # Handle HTTP errors
        embed = discord.Embed(
            title="Error",
            description=f"Failed to call API route `{route}`: {str(e)}",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)

    except Exception as e:
        # Handle other exceptions
        embed = discord.Embed(
            title="Error",
            description=f"An error occurred while calling API route `{route}`: {str(e)}",
            color=discord.Color.red(),
        )
        await ctx.send(embed=embed)


@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context) -> None:
    """Sync commands"""
    synced = await ctx.bot.tree.sync()
    await ctx.send(f"Synced {len(synced)} commands globally")


# Run the bot with the loaded Discord bot token
bot.run(bot_token)
