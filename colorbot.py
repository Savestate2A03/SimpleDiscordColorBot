import discord
import re
import requests
import asyncio

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

# disable default help
bot.remove_command('help')

# -------------------

# check if a role is not being used, and delete it
# this waits a bit before checking since discord
# likes to take some time before reporting changes
async def sleep_check_and_delete_role(role):
    await asyncio.sleep(10) # give time before checking
    return await check_and_delete_role(role)

# this is only called directly from the purge command
async def check_and_delete_role(role):
    if len(role.members) == 0:
        await role.delete()
        return True
    return False

# use requests to query the colourlovers API
async def color_lover_api(keywords):
    keywords = keywords.replace(" ", "+") # they use + instead of %20
    url = f"http://www.colourlovers.com/api/colors?keywords={keywords}&numResults=1&format=json"
    hexcode = "#" + requests.get(url).json()[0]["hex"] # fancy
    return hexcode

# remove colors, returns the number of 
# roles removed from the specified user
# (generally 1 but jic one gets stuck)
async def remove_colors(ctx, author):
    color_roles = []
    re_color = re.compile(r'^\#[0-9A-F]{6}$')
    for role in author.roles:
        # only remove color roles
        if re_color.match(role.name.upper()):
            color_roles.append(role)

    # once all the roles are collected,
    # remove them from the user
    for role in color_roles:
        await author.remove_roles(role)
        # if the role is no longer being used,
        # delete it. run it async as there's 
        # a 10 second (or so) wait in the check
        asyncio.create_task(sleep_check_and_delete_role(role))

    return len(color_roles)

# simple source command
@bot.command()
async def source(ctx):
    await ctx.send("blep <https://github.com/Savestate2A03/SimpleDiscordColorBot>")

# simple help command
@bot.command()
async def help(ctx):
    await ctx.send("Go here and pick out a color : "
        "<https://htmlcolorcodes.com/color-picker/>, then run the command "
        "`!color #RRGGBB` where '#RRGGBB' is the hex code you want !\n"
        "You can also use general descriptions of colors (ex: `!color dark purple`) "
        "thanks to the colourlovers API, so shoutouts to them !")

@bot.command(name="color", aliases=["colour"])
async def color(ctx, *color):
    # if the command is improperly
    # formatted, invoke help and exit
    if len(color) == 0:
        await help.invoke(ctx)
        return

    message = ctx.message
    author  = message.author 
    guild   = message.guild
    color_lover = False # flag if used the colourlovers API

    color = " ".join(color)
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
        # if not a hex code, use colourlovers API
        color_lover = True 
        color = await color_lover_api(color)

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

    await ctx.send(f"colorized !")

# remove colors that somehow dont get deleted
@bot.command()
async def purge(ctx):
    message = ctx.message
    author  = message.author 
    guild   = message.guild
    allowed = author.guild_permissions.manage_roles

    if not allowed:
        await ctx.send("you can't manage roles !")
        return

    # discord throttles a lot of stuff here
    # so going through all the roles takes a little while
    await ctx.send(f"purging unassigned colors ! ... this may take a sec ...")

    re_color = re.compile(r'^\#[0-9A-F]{6}$')
    num_deleted = 0

    roles = guild.roles
    progress = await ctx.send(f"progress: 0/{len(roles)}")
    iterations = 0

    for role in roles:
        if re_color.match(role.name): # if a color role
            deleted = await check_and_delete_role(role)
            if deleted:
                num_deleted += 1
        iterations += 1
        # edit our previous progress message (fancy)
        await progress.edit(content="progress: "
                f"{iterations}/{len(roles)}")

    # final report
    await ctx.send(f"removed {num_deleted} unassigned colors !")

# -------------------

# read token from token.txt
token = "womp"
with open('token.txt', 'r') as file:
    token = file.read().replace('\n', '')

bot.run(token)
