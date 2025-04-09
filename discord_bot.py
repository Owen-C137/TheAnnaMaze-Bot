import discord
from discord.ext import commands
from discord.utils import get
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def purge_members(ctx):
    for member in ctx.guild.members:
        # Skip bots
        if member.bot:
            continue
        # Check if the member does NOT have the 'Confirmed' role
        if not get(member.roles, name='Confirmed'):
            try:
                await member.kick(reason="Removed due to missing 'Confirmed' role")
                await ctx.send(f'Removed {member.name}')
            except Exception as e:
                await ctx.send(f'Failed to remove {member.name}: {e}')

@bot.command()
async def sayhi(ctx):
    await ctx.send("Hello there!")

@bot.command()
async def react(ctx, message_id: int, *, emoji_list: str):
    """
    React to a message with a list of emojis.
    Usage: !react <message_id> <emoji1,emoji2,...>
    Example: !react 1100777582183579821 :tiktok:, :twitch:, :youtube:, :fb:, :spchat:, :discord:,🏞️
    """
    # Split the emoji list by commas and filter out empty entries
    emojis = [e.strip() for e in emoji_list.split(',') if e.strip()]
    
    try:
        # Fetch the target message from the current channel
        message = await ctx.channel.fetch_message(message_id)
        for e in emojis:
            # If the emoji is in the format :name:, try to find the custom emoji in the guild
            if e.startswith(':') and e.endswith(':'):
                emoji_name = e.strip(':')
                custom_emoji = discord.utils.get(ctx.guild.emojis, name=emoji_name)
                if custom_emoji:
                    e = str(custom_emoji)
                else:
                    # If not found, assume it's a Unicode emoji and remove colons
                    e = emoji_name
            await message.add_reaction(e)
        await ctx.send("Reactions added successfully!")
    except Exception as error:
        await ctx.send(f"Error adding reactions: {error}")

@bot.event
async def on_member_join(member):
    try:
        welcome_message = (
                        f":wave: Welcome to {member.guild.name}!\n\n"    
                        "To gain access to the public channels in the server you will need to first agree to the server rules to get the confirmed role \n\n"
                        "https://discordapp.com/channels/1029289829541871626/1349686985543127052 \n"
                        "There are also personalized channels, accessible by choosing the role specific to them\n"
                        "https://discordapp.com/channels/1029289829541871626/1100760647702171729 \n\n"
                        "Once you have done this, feel free to introduce yourself and get chatting!"
        )
        await member.send(welcome_message)
    except Exception as e:
        # This will silently fail if the user has DMs turned off
        print(f"Could not send DM to {member.name}: {e}")


bot.run(os.getenv('DISCORD_TOKEN'))
