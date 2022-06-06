import discord
from discord.ext import commands
from gunboat import *

# $challenge starts game and creates player1 Frigate obj
# $accept creates player2 Frigate and DMs players for input
#   (working?)need to figure out way to wait on both player commands, maybe while loop with list of commands,
#   checking on length
#       maybe implement dictionary for complete turn history, may make 3x maneuver tracking easiest
# need to figure out how to have bot send/receive DMs for private move commands, bot end of turn response should be
#   in public channel though

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
	player = game['players'][user_name]
	await turn_actions(ctx, player, 'fire')
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
	player.maneuver()
	await turn_actions(ctx, player, 'maneuver')
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
	player.reload()
	await turn_actions(ctx, player, 'reload')
	await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


@bot.command(
	help="Command your crew to reload, replenishing all 3 of your cannon shots.",
	brief="Reload!",
	name="aim",  # optional shorter command call, prefix w/ $ in chat to execute
	)
async def aim(ctx):
	"""Accepts the challenge to a game of Gunboat."""
	author = ctx.message.author
	user_name = author.name
	player = game['players'][user_name]
	player.aim()
	await turn_actions(ctx, player, 'aim')
	await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


async def turn_actions(ctx, player, action):
	"""Creates stack of actions taken by each player."""
	turn = game['turn']
	game['turn_log'][f'turn_{turn}'][player] = action
	await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


async def turn_end(ctx):
	"""Performs end of turn cleanup."""
	turn = game['turn']
	player_1 = list(game['turn_log'][f'turn_{turn}'].values())[0]  # listify values of current turn to index into
	# player
	player_2 = list(game['turn_log'][f'turn_{turn}'].values())[1]
	player_1_action = game['turn_log'][f'turn_{turn}'][player_1]
	player_2_action = game['turn_log'][f'turn_{turn}'][player_2]

	if player_1_action == 'fire':
		player_2.health -= player_1.fire(player_2)

	game['turn'] += 1
	await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


bot.run(SECRET_KEY)
