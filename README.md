# SimpleDiscordColorBot
Very simple hex code based color role assign bot for Discord

# Requirements
 * Python 3.7.4
 * discord.py
 * requests
 
Requirements can be installed with
```
pip install discord.py requests
```

# Before running
Make sure your Discord bot token is in a file called `token.txt` in the same directory as the python script.

# Commands
`!color #RRGGBB`  
Set your color to a specific hex code
 
`!color general description`  
Set your color to a general description (ex: desaturated cyan)  
*Uses the COLOURlovers API*

`!color remove`  
Removes all roles from a user that match the hex-code format

`!help`  
Display help. Also displayed with an argumentless `!color` invocation

`!purge`  
Goes through all the roles in the guild it was invoked from and removes any hex-code roles that aren't assigned to anyone. 
*Requires **manage_roles** permission*  
  
Note: The roles should be removed automatically when a user removes it via the `!color remove` command or when they assign a new color and it's not being used anymore, but it may be possible for one to slip through the cracks once in a blue moon. It also covers cases where colors are manually removed from someone but the role isn't deleted.

# Screenshots
### !color
![Invoking the !color command](https://i.imgur.com/NzQ6x48.png)
### !help
![Invoking the !help command](https://i.imgur.com/BMYFm4p.png)
### !purge
![Invoking the !purge command](https://i.imgur.com/5IgsXXJ.png)
