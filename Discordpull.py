import nextcord
from Pulldatachecks import stockpicker

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
        # Pick a stock
        stock = stockpicker()  # Call the stockpicker function
        
        # Send the stock pick to a channel (replace CHANNEL_ID with the actual channel ID)
        channel = client.get_channel(1324776055487336461)  # Replace with your channel ID
        await channel.send(f"Today's stock pick is: {stock}")

        # Set flag to True to prevent re-sending stock pick
        has_sent_stock = True
    else:
        print("Stock pick has already been sent. Skipping logic.")

# Run the bot using your token
client.run('REDACTED')  # Replace with your bot's token

client.close