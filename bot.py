import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from dotenv import load_dotenv
from os import getenv

bot = commands.Bot(command_prefix="anon-")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="anon-help"))


try:
    @bot.command(name="dm", brief="Anonymously dms user\n (make sure you don't ping them but use their tag!)")
    async def dm(ctx, user, *, message=None):
        await ctx.message.delete()
        converter = MemberConverter()
        address = await converter.convert(ctx, user)
        if(message is None):
            await ctx.send("Enter a message to send to this user!")
            return
        msg = await address.send("**An anonymous user sent you this:** "+message)
        await msg.add_reaction("\U0001F5D1")
except discord.ext.commands.errors.UserNotFound:
    print("This doesn't even fucking work since it's a coroutine")

load_dotenv()
bot.run(getenv('TOKEN'))
