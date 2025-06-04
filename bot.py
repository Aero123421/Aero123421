import discord
import os
import logging
import google.generativeai as genai
from tavily import TavilyClient
from dotenv import load_dotenv

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    filename='bot.log',
    filemode='a'  # Append to log file
)
# Optional: More verbose logging from discord.py library
# logging.getLogger('discord').setLevel(logging.DEBUG)
# logging.getLogger('discord.http').setLevel(logging.DEBUG)
logger = logging.getLogger('DiscordBot')
# --- End Logging Setup ---

# Load environment variables
load_dotenv()
logger.info("Attempting to load environment variables from .env file.")

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API key loaded and configured.")
else:
    logger.error("CRITICAL: GEMINI_API_KEY not found in .env file. Gemini features will be disabled.")
    print("Error: GEMINI_API_KEY not found. Make sure you have set it in your .env file.")

# Get Tavily API Key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if TAVILY_API_KEY:
    logger.info("Tavily API key loaded.")
else:
    logger.error("CRITICAL: TAVILY_API_KEY not found in .env file. Tavily search features will be disabled.")
    print("Error: TAVILY_API_KEY not found. Make sure you have set it in your .env file.")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize Discord client
client = discord.Client(intents=intents)

async def generate_gemini_response(prompt):
    """Generates a response from the Gemini API."""
    if not GEMINI_API_KEY:
        logger.warning("Gemini API call attempted but API key is not configured.")
        return "Gemini API key not configured. Please set GEMINI_API_KEY in .env"
    try:
        logger.info(f"Generating Gemini response for prompt: '{prompt[:50]}...'")
        model = genai.GenerativeModel('gemini-pro')
        response = await model.generate_content_async(prompt)
        logger.info("Gemini response generated successfully.")
        return response.text
    except Exception as e:
        logger.error(f"Error generating Gemini response for prompt '{prompt[:50]}...': {e}", exc_info=True)
        return "Sorry, an error occurred while trying to get a response from Gemini."

async def search_tavily(query):
    """Performs a search using the Tavily API."""
    if not TAVILY_API_KEY:
        logger.warning("Tavily search attempted but API key is not configured.")
        return "Tavily API key not configured. Please set TAVILY_API_KEY in .env"
    try:
        logger.info(f"Performing Tavily search for query: '{query[:50]}...'")
        tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
        response = await tavily_client.search(query=query, search_depth="basic", max_results=5)
        results = response.get('results', [])
        logger.info(f"Tavily search completed. Found {len(results)} results for query '{query[:50]}...'.")

        if not results:
            return "No search results found."

        formatted_results = []
        for result in results:
            formatted_results.append(f"Title: {result.get('title', 'N/A')}\nURL: <{result.get('url', 'N/A')}>")

        return "\n\n".join(formatted_results)
    except Exception as e:
        logger.error(f"Error during Tavily search for query '{query[:50]}...': {e}", exc_info=True)
        return "Sorry, an error occurred while performing the search."

@client.event
async def on_ready():
    """Event handler for when the bot has successfully connected to Discord."""
    logger.info(f'{client.user} has connected to Discord! User ID: {client.user.id}')
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set. Gemini functionality will be disabled for this session.")
    if not TAVILY_API_KEY:
        logger.warning("TAVILY_API_KEY is not set. Tavily search functionality will be disabled for this session.")

@client.event
async def on_message(message):
    """Event handler for when a message is received."""
    if message.author == client.user:
        return

    if not message.content.startswith('!'):
        return

    logger.info(f"Received command '{message.content}' from {message.author} (ID: {message.author.id}) in channel {message.channel.id} (Guild: {message.guild.id if message.guild else 'DM'})")

    command_text = message.content.lower()
    command_parts = message.content.split()
    command_name = command_parts[0].lower()


    if command_name == '!hello':
        logger.info(f"Processing !hello command for {message.author.name}")
        await message.channel.send('Hello!')
        logger.info(f"!hello command processed successfully for {message.author.name}")

    elif command_name == '!ask':
        prompt = message.content[len('!ask '):].strip()
        logger.info(f"Processing !ask command for {message.author.name} with prompt: '{prompt[:30]}...'")
        if not prompt:
            logger.warning(f"!ask command from {message.author.name} had no prompt.")
            await message.channel.send("Please provide a prompt after `!ask ` (e.g., `!ask What is AI?`).")
            return

        async with message.channel.typing():
            response_text = await generate_gemini_response(prompt)
            await message.channel.send(response_text)
        logger.info(f"!ask command processed successfully for {message.author.name}. Prompt: '{prompt[:30]}...'")

    elif command_name == '!search':
        query = message.content[len('!search '):].strip()
        logger.info(f"Processing !search command for {message.author.name} with query: '{query[:30]}...'")
        if not query:
            logger.warning(f"!search command from {message.author.name} had no query.")
            await message.channel.send("Please provide a query after `!search ` (e.g., `!search Python tutorials`).")
            return

        async with message.channel.typing():
            search_results = await search_tavily(query)
            if len(search_results) > 2000:
                logger.info(f"Search results for '{query[:30]}...' too long, truncating for {message.author.name}.")
                await message.channel.send("Search results are too long. Here's a part of it:\n" + search_results[:1900] + "...")
            else:
                await message.channel.send(search_results)
        logger.info(f"!search command processed successfully for {message.author.name}. Query: '{query[:30]}...'")

    elif command_name == '!help':
        logger.info(f"Processing !help command for {message.author.name}")
        help_message = """
Available commands:
`!hello` - Greets the user.
`!ask <question>` - Ask a question to the Gemini AI.
`!search <query>` - Search the web using Tavily.
`!help` - Shows this help message.
        """
        await message.channel.send(help_message)
        logger.info(f"!help command processed successfully for {message.author.name}")
    else:
        logger.warning(f"Unknown command '{command_name}' received from {message.author.name}: {message.content}")
        await message.channel.send(f"Unknown command: `{command_name}`. Type `!help` to see available commands.")

# Load the token from environment variables and run the bot
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if TOKEN is None:
    logger.critical("CRITICAL: DISCORD_BOT_TOKEN not found. The bot cannot start.")
    print("Error: DISCORD_BOT_TOKEN not found. Make sure you have set it in your .env file.")
else:
    logger.info("DISCORD_BOT_TOKEN loaded. Attempting to start the bot.")
    # client.run(TOKEN) # This line will be uncommented in the final step to run the bot.
    pass # Keep client.run commented out for now

# Placeholder for running the bot (actual execution will be handled in a later step)
if TOKEN:
    logger.info("Bot script setup complete. Bot is ready to run (client.run() is currently commented out).")
else:
    logger.error("Bot script setup encountered an error: DISCORD_BOT_TOKEN is missing.")

print("Bot script loaded with enhanced logging and error handling. Waiting for token to run.")
