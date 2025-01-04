import nextcord
from Pulldatachecks import stockpicker
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the token and channel ID from the environment variables
token = os.getenv("DISCORD_TOKEN")
channel_id = os.getenv("CHANNELID")

# Validate that the token and channel ID are retrieved
if not token:
    raise ValueError("No Discord bot token found in environment variables.")
if not channel_id:
    raise ValueError("No Discord channel ID found in environment variables.")

# Ensure channel ID is an integer, as required by nextcord
try:
    channel_id = int(channel_id)
except ValueError:
    raise ValueError("CHANNELID must be a valid integer.")

# Initialize the nextcord client
client = nextcord.Client()

# Flag to check if the stock has been sent
has_sent_stock = False

# Event when the bot is ready
@client.event
async def on_ready():
    global has_sent_stock

    print(f'We have logged in as {client.user}')

    # Only send the stock pick once
    if not has_sent_stock:
        # Pick a stock (replace with your stockpicker function as needed)
        stock = stockpicker()  # Example stock, replace with `stockpicker()` call if implemented

        # Get the channel and send the stock pick
        channel = client.get_channel(channel_id)
        if channel is None:
            print(f"Could not find channel with ID {channel_id}.")
        else:
            await channel.send(f"Today's stock pick is: {stock}")

        # Close the bot after sending the message
        await client.close()

        # Set flag to True to prevent re-sending stock pick
        has_sent_stock = True
    else:
        print("Stock pick has already been sent. Skipping logic.")

# Run the bot using your token
client.run(token)
