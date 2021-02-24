import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json

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
async def on_message(message):
    if(message.author == bot.user):
        await message.add_reaction("\U0001F5D1")
        return
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if(ctx.guild):
        if(isinstance(error, discord.ext.commands.errors.MissingRequiredArgument)):
            await ctx.message.author.send("Enter a user!")
            await ctx.message.delete()
        else:
            raise error
    else:
        await ctx.send("Type your command into a valid text channel!")


@bot.command(name="dm", brief="Anonymously dms user (anon-dm @recipient your sentence)")
async def dm(ctx, recipient: discord.User, *, message=None):
    if(recipient.id == ctx.message.author.id):
        await ctx.message.author.send("You can't anonymously dm yourself!")
    if(ctx.guild):
        await ctx.message.delete()
        if(os.path.exists("blacklist.json")):
            with open("blacklist.json") as outfile:
                if(recipient.id in json.load(outfile)):
                    await ctx.message.author.send("This person is blacklisted. ")
                    return
        if(message is None):
            await ctx.message.author.send("Enter a message to send to " + recipient.display_name)
            return
        await ctx.message.author.send("Successfully sent **" + recipient.display_name + ":** \"" + message + "\"")
        await recipient.send("**An anonymous user sent you this:** "+message)
    else:
        await ctx.send("Type your command into a valid text channel!")


@bot.command(name="blacklist", brief="Blacklists yourself from anonymous dms")
async def blacklist(ctx):
    if(os.path.isfile("blacklist.json")):
        with open("blacklist.json") as outfile:
            blacklist = json.load(outfile)
            if(ctx.message.author.id in blacklist):
                blacklist.remove(ctx.message.author.id)
                await ctx.message.author.send("Successfully removed you from the blacklist")
            else:
                blacklist.append(ctx.message.author.id)
                await ctx.message.author.send("Successfully added you to the blacklist")
    else:
        blacklist = [ctx.message.author.id]
    with open("blacklist.json", 'w') as outfile:
        json.dump(blacklist, outfile)

load_dotenv()
bot.run(os.getenv('TOKEN'))
