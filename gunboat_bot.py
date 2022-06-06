# $challenge starts game and creates player1 Frigate obj
# $accept creates player2 Frigate and DMs players for input
#   need to figure out way to wait on both player commands, maybe while loop with list of commands, checking on length
#       maybe implement dictionary for complete turn history, may make 3x maneuver tracking easiest

import discord
from discord.ext import commands
from gunboat import *

client = discord.Client()
bot = commands.Bot(command_prefix="$")

game = {
    'players': {},
    'turn': 1,
    'turn_log': {
        'turn_1': {},
        },
    }


@bot.command(
    help="Challenge the channel members to a game of Gunboat. The first to accept with '$accept' will become your "
         "opponent",
    brief="Challenge the channel to a game of Gunboat.",
    name="challenge",  # optional shorter command call, prefix w/ $ in chat to execute
)
async def challenge(ctx):
    """Challenges the channel to a game of Gunboat."""
    author = ctx.message.author
    user_name = author.name
    game['players'][f'{user_name}'] = Frigate(user_name)
    await ctx.channel.send(f"{user_name} boarded a frigate and challenged you!")

@bot.command(
    help="Accepts the challenge to a game of Gunboat.",
    brief="Accept the challenge!",
    name="accept",  # optional shorter command call, prefix w/ $ in chat to execute
    )
async def accept(ctx):
    """Accepts the challenge to a game of Gunboat."""
    author = ctx.message.author
    user_name = author.name
    for player in game['players']:  # for getting opposing player's name, look into better implementation
        if player != user_name:
            opponent = player
    game['players'][f'{user_name}'] = Frigate(user_name)
    await ctx.channel.send(f"{user_name} accepted {opponent}'s challenge!")


@bot.command(
    help="Command your crew to fire cannons. Deals 1 damage normally, takes 1 ammo. Can be dodged if the opponent "
         "maneuvers during "
         "the same turn.",
    brief="Fire cannons!",
    name="fire",  # optional shorter command call, prefix w/ $ in chat to execute
    )
async def fire(ctx):
    """Accepts the challenge to a game of Gunboat."""
    author = ctx.message.author
    user_name = author.name
    await turn_actions(user_name, 'fire')
    await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


@bot.command(
    help="Command your crew to perform evasive maneuvers. Dodges cannon fire if fired upon during the same turn. "
         "Maneuvering 3 turns in a row puts you on their broadside, though, and you're susceptible to a critical hit.",
    brief="Evade!",
    name="man",  # optional shorter command call, prefix w/ $ in chat to execute
    )
async def maneuver(ctx):
    """Accepts the challenge to a game of Gunboat."""
    author = ctx.message.author
    user_name = author.name
    player = game['players'][user_name]
    player.maneuvered = True
    await turn_actions(ctx, user_name, 'maneuver')
    await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


@bot.command(
    help="Command your crew to reload, replenishing all 3 of your cannon shots.",
    brief="Reload!",
    name="rel",  # optional shorter command call, prefix w/ $ in chat to execute
    )
async def reload(ctx):
    """Accepts the challenge to a game of Gunboat."""
    author = ctx.message.author
    user_name = author.name
    player = game['players'][user_name]
    player.maneuvered = True
    await turn_actions(ctx, user_name, 'maneuver')
    await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


async def turn_actions(ctx, player, action):
    """Creates stack of actions taken by each player."""
    turn = game['turn']
    game['turn_log'][f'turn_{turn}'][player] = action
    await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


async def turn_end(ctx, player, action):
    """Performs end of turn cleanup."""
    game['turn'] += 1

    await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


@bot.command(
    help="Adds you as a player. You start at GO with $1000.",
    brief="Adds you as a player. You start at GO with $1000.",
    name="play",  # optional shorter command call, prefix w/ $ in chat to execute
)
async def add_player(ctx):
    """Adds the command author as a player."""
    author = ctx.message.author
    user_name = author.name
    game.create_player(f"{user_name}", 1000)
    await ctx.channel.send(f"Welcome to the game, {user_name}")


@bot.command(
    help="First rolls a die for your movement. Then moves that many spaces for you. "
    "Movement automatically checks if your new space has an owner, and handles "
    "your payment of rent to them. Your new current space's info is then "
    "printed, as well as a notification of rent payment if that happens. Finally "
    "game status is checked, and a winner is decalred if there is one.",
    brief="Rolls a die and moves you, paying rent on new space if necessary.",
    name="roll",  # optional shorter command call, prefix w/ $ in chat to execute
)
async def roll(ctx):
    """Rolls a die for movement, moves the player and does rent payment handling,
    then prints info on the player's new space occupied."""
    author = ctx.message.author
    user_name = author.name
    die_roll = random.randint(1, 6)
    money_before_move = game.get_player_account_balance(user_name)
    game.move_player(user_name, die_roll)
    money_after_move = game.get_player_account_balance(user_name)
    info = game.space_info(user_name)
    position = info["position"]
    owner = info["owner"]
    rent_val = info["rent_value"]
    buy_val = info["buy_value"]
    await ctx.channel.send(f"{user_name} rolled a {die_roll}!")
    await ctx.channel.send(
        f"Position: {position}\n"
        f"Owner: {owner}\n"
        f"Rent Price: ${rent_val}\n"
        f"Buy Price: ${buy_val}"
    )
    player = game.get_players()[user_name]
    player_space = player.get_current_space()
    player_space_owner = player_space.get_owner()
    if player_space_owner is not None:
        await ctx.channel.send(
            f"{user_name} was charged ${rent_val} in rent by {owner}!"
        )
    if money_after_move == 0:
        await ctx.channel.send(
            f"Ope. {user_name} is out of money :(\nGGWP {user_name}"
        )
    winner = game.check_game_over()
    if winner != "":
        await ctx.channel.send(
            f"Wowowow! You finished a full game and {winner} is the winner :D"
        )


@bot.command(
    help="Looks at your current space and prints its information: board position, "
    "owner, rent price, and buy price.",
    brief="Print your current space's info.",
    name="spaceinfo",  # optional shorter command call, prefix w/ $ in chat to
    # execute
)
async def space_info(ctx):
    """Prints info for player's current space."""
    author = ctx.message.author
    user_name = author.name
    info = game.space_info(user_name)
    position = info["position"]
    owner = info["owner"]
    rent_val = info["rent_value"]
    buy_val = info["buy_value"]
    await ctx.channel.send(
        f"Position: {position}\n"
        f"Owner: {owner}\n"
        f"Rent Price: ${rent_val}\n"
        f"Buy Price: ${buy_val}"
    )


@bot.command(
    help="Prints your information: board position and current account balance.",
    brief="Prints your information: board position and current account balance.",
    name="myinfo",  # optional shorter command call, prefix w/ $ in chat to execute
)
async def my_info(ctx):
    """Prints player's position and money."""
    author = ctx.message.author
    user_name = author.name
    position = game.get_player_current_position(user_name)
    money = game.get_player_account_balance(user_name)
    await ctx.channel.send(f"{user_name}\nPosition: {position}\nMoney: ${money}")


@bot.command(
    help="Buys your current space and transfers ownership to you, if you have "
    "sufficient funds.",
    brief="Buy your current space.",
    name="buy",  # optional shorter command call, prefix w/ $ in chat to execute
)
async def buy_space(ctx):
    """Buys player's current space."""
    # NEED TO ADD handling for invalid purchases (not enough money, already owned, etc.)
    author = ctx.message.author
    user_name = author.name
    game.buy_space(user_name)
    money = game.get_player_account_balance(user_name)
    await ctx.channel.send(
        f"{user_name} bought a piece of property!\nNew balance: $" f"{money}"
    )


bot.run("OTgyMTM5NDMxMTQ0MjkyNDAz.G3mZpR.zO8M5bHKv6Yu1alq3v5DyoDf9ICDyn_BndHWj4")
