import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

bot = commands.Bot(command_prefix="anon-")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=bot.command_prefix+"help"))


@bot.event
async def on_raw_reaction_add(payload):
    if(payload.user_id == bot.user.id):
        return
    if(not payload.guild_id and str(payload.emoji) == "\U0001F5D1"):
        msgChannel = await bot.fetch_channel(
            payload.channel_id)
        deletedMsg = await msgChannel.fetch_message(payload.message_id)
        await deletedMsg.delete()


@bot.event
async def on_command_error(ctx, error):
    if(ctx.guild):
        await ctx.message.delete()
        if(isinstance(error, discord.ext.commands.errors.MissingRequiredArgument)):
            await ctx.message.author.send("Enter a user!")
    else:
        await ctx.send("Type your command into a valid text channel!")


@bot.command(name="dm", brief="Anonymously dms user (anon-dm @recipient your sentence)")
async def dm(ctx, user: discord.User, *, message=None):
    if(ctx.guild):
        await ctx.message.delete()
        if(message is None):
            await ctx.message.author.send("Enter a message to send to " + user.display_name)
            return
        successMsg = await ctx.message.author.send("Successfully sent **" + user.display_name + ":** \"" + message + "\"")
        await successMsg.add_reaction("\U0001F5D1")
        msg = await user.send("**An anonymous user sent you this:** "+message)
        await msg.add_reaction("\U0001F5D1")
    else:
        await ctx.send("Type your command into a valid text channel!")

load_dotenv()
bot.run(getenv('TOKEN'))
