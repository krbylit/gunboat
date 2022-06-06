# $challenge starts game and creates player1 Frigate obj
# $accept creates player2 Frigate and DMs players for input
#   need to figure out way to wait on both player commands, maybe while loop with list of commands, checking on length
#       maybe implement dictionary for complete turn history, may make 3x maneuver tracking easiest

import discord
from discord.ext import commands
import random
from RealEstateGame import *

client = discord.Client()
bot = commands.Bot(command_prefix="$")
game = RealEstateGame()
rents = [
    50,
    50,
    50,
    75,
    75,
    75,
    100,
    100,
    100,
    150,
    150,
    150,
    200,
    200,
    200,
    250,
    250,
    250,
    300,
    300,
    300,
    350,
    350,
    350,
]


@bot.command(
    help="Starts a game of Minipoly with 24 spaces and a starting GO space. Rent "
    "prices for spaces range from $50-$350.",
    brief="Starts a game of Minipoly",
    name="start",  # optional shorter command call, prefix w/ $ in chat to execute
)
async def play_minipoly(ctx):
    """Creates a Minipoly game."""
    author = ctx.message.author
    user_name = author.name
    game.create_spaces(50, rents)
    await ctx.channel.send(f"{user_name} started a game of Minipoly!")


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
