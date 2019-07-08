import discord
import re

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

# disable default help
bot.remove_command('help')

# remove colors, returns the number of 
# roles removed from the specified user
# (generally 1 but jic one gets stuck)
async def remove_colors(ctx, author):
    color_roles = []
    for role in author.roles:
        # only remove color roles
        if role.name.startswith("#"):
            color_roles.append(role)

    # once all the roles are collected,
    # remove them from the user
    for role in color_roles:
        await author.remove_roles(role)

    # if the role is no longer being used,
    # delete it.
    if len(role.members) == 0:
        await role.delete()

    return len(color_roles)

# simple source command
@bot.command()
async def source(ctx):
    await ctx.send("blep <https://github.com/Savestate2A03/SimpleDiscordColorBot>")

# simple help command
@bot.command()
async def help(ctx):
    await ctx.send("Go here and pick out a color : <https://htmlcolorcodes.com/color-picker/>, then run the command `!color #RRGGBB` where '#RRGGBB' is the hex code you want !")

@bot.command()
async def color(ctx, *color):
    # if the command is improperly
    # formatted, invoke help and exit
    if len(color) != 1:
        await help.invoke(ctx)
        return

    message = ctx.message
    author  = message.author 
    guild   = message.guild

    color = color[0]
    color = color.upper() # makes things easier

    if color == "REMOVE":
        # see if any roles were removed
        # and let the user know how the removal
        # process went.
        removed = await remove_colors(ctx, author)
        if removed > 0:
            await ctx.send("color vaporized !")
        else:
            await ctx.send("no color role to remove !")
        return

    # look for hex code match
    re_color = re.compile(r'^\#[0-9A-F]{6}$')
    if not re_color.match(color):
        await ctx.send("not a hex code ):")
        return

    # remove all color roles in preperation
    # for a new color role
    await remove_colors(ctx, author)

    assigned_role = None

    # check if the role already exists. if 
    # it does, assign that instead of 
    # making a new role
    for role in guild.roles:
        if role.name.upper() == color:
            assigned_role = role

    # if we didn't find the role, make it
    if assigned_role == None:
        red   = int(color[1:3], 16) #.RR....
        green = int(color[3:5], 16) #...GG..
        blue  = int(color[5:7], 16) #.....BB
        assigned_role = await guild.create_role(
            name=color, 
            color=discord.Color.from_rgb(red, green, blue))

    # assign the role we found/created
    await author.add_roles(assigned_role)

    await ctx.send("colorized !")

# read token from token.txt
token = "womp"
with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')

bot.run(token)
