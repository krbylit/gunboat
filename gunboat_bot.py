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
	await ctx.channel.send(rf"""```
              |    |    |
             )_)  )_)  )_)
            )___))___))___)\
           )____)____)_____)\\
         _____|____|____|____\\\__
---------\                   /---------
  ^^^^^ ^^^^^^^^^^^^^^^^^^^^^
    ^^^^      ^^^^     ^^^    ^^
         ^^^^      ^^^
        {user_name} boards a frigate!
	```"""  # MOST OF THESE MUST BE MOVED TO END UP TURN CLEANUP


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
	await ctx.channel.send(rf"""```
              |    |    |
             )_)  )_)  )_)
            )___))___))___)\
           )____)____)_____)\\
         _____|____|____|____\\\__
---------\                   /---------
  ^^^^^ ^^^^^^^^^^^^^^^^^^^^^
    ^^^^      ^^^^     ^^^    ^^
         ^^^^      ^^^
        {user_name} boards a frigate!
	```"""


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
	await ctx.channel.send(rf"
                  __
                 /  \
           .-.  |    |
   *    _.-'  \  \__/
    \.-'       \
   /          _/
  |      _  /"
  |     /_\'
   \    \_/
    -----
 {user_name} fires their cannon!
 
               `.
     .-._______*:--
  .=( . )..--""*:--
 [/"`._.'       ` '
 
              , .
      _-|---= *:--
   ._(O)/     ' `


                0N@@@@@ mmmmmmwwwwgWw,,,,,,,,,,,,,___,__,_____             ,   _,,,
          _.,_,/F'"""""'""""""""""T'^""""""""""""""""PN`NR"```````````""""TRR"`""""R
          W,[ NN@@pppp8@pppppppppp$@mppp@Pp^__"@Pppp@@@p@@pppppppppppppppp@pmpppppp@
          '^^`"0RRNNNNRRNNNNNNN BR       6p[E]K,2BDD0  NRRNNNNNNNNNNNNNNNNNNR      R
          ,_    RRRRRRRRRR 5]NNN%#00NBB@BB0    N 0  NH RNN 0RRRRRRRRRM^^^^^ R^MRNRR^
     _   [0B0R@m@5```],D,,@D@@D@@N@@@@@@@BTp@B NNNNNNNN
    'RRR@@BBB0  Bw0D@DB@D@@d]0DP]['BB@BB@@Kw3NNNNNNNNNN
       w#00w      L BBB@BBBBBBBb}R^6D@DRRBRB@@ NNNNNNHNH
       NNNNN BD@DMW DDD@@@BBB@DD@E@DBB@RB@N RDDD5NNNN NH
       NNN @RB0R   @0D@DB@BRRRRRRRRRDR@@ BD@BRN   WBNNNR
       RR0D6BD 0N[  HMM^              `RR0@@@@RRQ0  PRR%
         'N@BBU@ #BDR                    [008$@#DBBDH
          'DB@$AU@BR                      Y@PB]@PB@M
            `"^P^"                          `"PM^`
                                    `    `  "   `
                                    

       ,/MMPMPPMPP$nnn0$mn:::n+n=h
      _`[NNR  NDB0W@#0   RRRRRRRR
    ';P0 K0BBBhDDD@&NNN
     0 WK@0RRRRRR@NK@ N
      T59B        %60R
      

                0N@@@@@ mmmmmmwwwwgWw,,,,,,,,,,,,,___,__,_____             ,   _,,,
          _.,_,/F'"""""'""""""""""T'^""""""""""""""""PN`NR"```````````""""TRR"`""""R
          W,[ NN@@pppp8@pppppppppp$@mppp@Pp^__"@Pppp@@@p@@pppppppppppppppp@pmpppppp@
          '^^`"0RRNNNNRRNNNNNNN BR       6p[E]K,2BDD0  NRRNNNNNNNNNNNNNNNNNNR      R
          ,_    RRRRRRRRRR 5]NNN%#00NBB@BB0    N 0  NH RNN 0RRRRRRRRRM^^^^^ R^MRNRR^
     _   [0B0R@m@5```],D,,@D@@D@@N@@@@@@@BTp@B NNNNNNNN
    'RRR@@BBB0  Bw0D@DB@D@@d]0DP]['BB@BB@@Kw3NNNNNNNNNN
       w#00w      L BBB@BBBBBBBb}R^6D@DRRBRB@@ NNNNNNHNH
       NNNNN BD@DMW DDD@@@BBB@DD@E@DBB@RB@N RDDD5NNNN NH
       NNN @RB0R   @0D@DB@BRRRRRRRRRDR@@ BD@BRN   WBNNNR
       RR0D6BD 0N[  HMM^              `RR0@@@@RRQ0  PRR%
         'N@BBU@ #BDR                    [008$@#DBBDH
          'DB@$AU@BR                      Y@PB]@PB@M
            `"^P^"                          `"PM^`
                                    `    `  "   `
                                    

                ▓█▓▓▓▓▓█▓▓▓▄▄▄▄▄▄▄▄▓▄▄▄▄▄▄▄▄╓,,,,,,,,▄,_╓,_____            ,   _╓▄▄
          _,,_,▄╬╬╬╬╬╬╬╠╬╬╬╬╬╬╬╬╬╬╬╬╩╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬╬▓╬▓▓╬╬╬╬╩╬╩╩╩╩╩╩╩╩╩╩╣▓▓╬╬╬╬╬╬█
         ▐▌▄╣███▓▓╣╣╣╣▓▓╣╣╣╣╣╣╣╣╣╣▓▓▓╣╣╣╬╬▓╬╠▒╟╬╣▓╣╣╣▓▓╣▓▓╣╣╣╣╣╣╣╣╣╣╣╣╣╣╣╣╣▓▓╬╬╬╬╬╬▓
          ╙▀▀"╙▓████████████████▓█████████▓▓╬╬▓╬▓██████▓████████████████████████████
          ,,_   ███████████▓╬██▓▓╫▓▓▓▓▓▓▓▓▓██████▓███╣█▓███▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█▀▀▀▀███▀
     _   ║▓▓▓█▓▄▓▓╙"╠╬╬▓▄▄▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣█████████▒
    ╙▀╝▀▓▓▓▓▓▓██▓╬█▓╣▓▓▓▓▓▓▓▓▓▓▓╬╣╬▓▓▓▓▓▓▓▓▓▓▓█████████▒
       ▄▓▓▓▓██████▌█▓▓▓▓▓▓▓▓▓▓▓▓╬╫╬▓▓▓▓▓▓▓▓█▓▓▓██████▌█▌
       ████████▓▓▓▓█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓███▓▓▓███████▌
       ████▓▓▓█▓███▓▓▓▓▓▓▓▓▓▓▓▀▀▀▀▓▓▓█▓▓█▓▓▓▓██████▓███▌
       ▀▀▀▓▓▓▓███▓██▓▀▀▀`  ``         '▀▓▓▓▓▓▓▓█▓███▓▀▀▀
         '▓▓▓▓▓▓█▓▓▓▓                    ╟▓▓▓▓▓▓▓▓▓▓▌
          ╙▓▓▓▓▓▓▓▓▓                      ▀▓▓▓╬▓▓▓▓▀
            '╙▀▀▀^                          "╙▀▀▀"
                                    "`` `` `"  ``` `
                                    

                ▓█▓▓▓▓▓█▓▓æ▄▄▄▄▄▄╗▄▓▄▄▄╖╖╖╓╓,,,,,,,__╓,_,______            ,   _,╖,
          _,,__▄╬╙╩╩╩╩╬╠╩╩╩╩╩╩╩╩╩╩╠╠╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩▌╩▓▓╩╩╩╩╩╩╩╩╩╩╩╩╩╩╩Ñ╣╩▓╩╩╩╩╩╩▓
          ▒▄╣▓██▓▓╬▒▒▒▓▓╬▒▒▒▒▒▒▒▒▒▓▓▒╬▒╬╬R▒Ü]░║╬R▒╬╬╣▓▓▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒╣▒▌▒▒▒▒▒▒▓
          '▀▀"╙▓███████████████▓▓▓██▓████▓▓▓╬╬▌╬▓▓▓▓▓██▓█████████████████████▓▓▓▓▓▓█
          ,__   ███████████╬╠██╬▓╫╣▓╫▓▓▓▓▓▓▓▓████╫███╬█╣██▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█▀▀▀▀███▀
     _   [▓▓▓▓▓▄▓▓``╓╠▄▓▄▄╬▓╬╬╬╣╬╣▓▓▓▓▓▓▓▓╫▓╫╣█████████▒
    ╙╝╝▀@╣╬╣▓▓██▓▄▓▓╣▓▓▓╬╣╣▓╣╫╣▓╬▐╬▓╫╣▓▓▓▓▓╣╣╬▓████████▒
       ╗▓▓▓▓▓▓██▓▓▌█▓▓▓▓╬╬╬╬╬╬╬▓╬▀Ñ╣╣╣▓▓▓▓▓▓▓▓▓██████▌█▒
       ██████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╬╬▓▓╬▓▓▓▓▓▓█▓▓▓▓▓▓█████▌
       ████╣▓▓▓▓███▓▓▓▓▓▓▓▓╩╣▀▀▀▀▀▓▓▓▓▓▓▓▓╬▓▓▓▓▓▓█▓▓███▌
       ▀▀▀╬╬▓▓▓▓▓▓▓█╬▀▀╙   ``         `▀▓▓╬▓▓▓▓▓▓▓▓█▓▀▀▀
          ╬╬╬▓╬╣▓▓▓▓▓                    ║╬╣╣▓╬▓▓▓▓▓Γ
          ╙▓╬╬▓▓╬╬╬▀                      ╙╬╣╬╬╬▓╣▓▀
            `╙▀▀▀"                          '╙▀▀╙`
                                      `  `     ``
                                      
                                      
     
     
     
                                                                                             _╓,_
                                                                                          __╬▒Ü░╦▒_
                                                                          ___,╓,,,:÷@╦╔▒▒▒▒╠╠▒▒▒╠▒▒╗
                                                      __,,__,~:,,-=╔▒▒▒▒▒▒▒▒▒▒▒▒▒╠╠╠╠╠▒▒▒╠╠▒▒╠▒╩▓██╬▒
                                    ____,,:,-=╔▒R▒▒▒▒▒▒▒Ü▒▒╠▒▒▒▒▒▒▒▒▒▒╠▒╠╠╠╠╠╠╠╠╬╠╬╠╬╬╠╬╬╬╣▌╬╠╠╠╟╬╟╬╠
                      ,-╔D╠╩░░▒▒▒▒▒▒░░▒▒Ü░▒▒▒▒▒▒▒▒▒▒▒▒Ü╠▒▒Ü╠╬╠╠╠╠╠╠╠╬╬╠╬╬╬╬╬╬╬╬╬╬╬▓╬▓▓▓▓▓▓▓▓╬╬╬▒╩╠╣D╠
                    ,╠╠▒▒╠▒▒░▒▒▒▒▒▒▒▒╠▒╠╠╬╠╠╠╠╠╠╬╠╬╬╬╬╠╬╬╬▒╬╬╬╬╬╬╬╬╬╬╬╬╬╣╣╬▓╣▓▓▓▓▓▓▓╬▓▓▓▓▓▓▓█╣╬╣▒▒▒╠╩
                   j╠╠▒╠╠╬▒╠╠╬╬╠╬╬╬╬╠╬╬╬╢╬╫╬╠╠╬╬╬╬╬╬╬╬╬╬▓▓▒╣▓▓▓╣╬╬▓▓▓╬▓╣▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█████▓▓╬╣▓▓
                   ╠╬╬╠╠╠╬╬╬╬╬╬╬╬╬╬╬╬╣╬╬╬╬╬▒╠▓▓▓╬╬▓▓╣▓╬╣▓▓▓╬╣▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▀▀▀╙▀╙      ╙▀▀^
                ╗▒╣╬▒╬╬╬╬╬╣╬╬╬╫╬╬╬╬╬╬╬╬╣╬╬╬╬╫╬╬╬╬╬╬╬▓▓▓╬▓▓▓▓▓▓▓▓█▓▓▓▓▓▓▓▀▀▀^`
                ╬╬╬╬╬╬╬╬╬╣╬╣╣╬╬╬╬╬╬▓╬╬╬╬╬╣╣▓╣╣╣╣╣╣╣╣████▓▓▓████▓█▓
                 ` '╬╬╬╬╣╣╣▓▓▓╬╬╣▓╣╬╬▓╣╬╬▓▓╣╬╬╬╬╣▓╬╬╫██████████▓╣▓
                   φ╣╬╣╬╬╬╬╬╬╬╬╬╬╬╬▒╬▓▓█▓▓▓╣▓╣▓╣▓▓╣╬╬▓▓▓███████▓▓╫
            ▒   ,«φ╬╬╬▓▓▓╬▓╬╬╬╬╬╬╬╬╬▓███▓╬╬╬╬╬╣╬╬╬╬╬╬╣▓▓█▓█████▓▓╬▌
            ▓   ║▓╬╬▓▓▓█╟▓▓╣╬╣╬╣╬╬▓▓╬╣╬╣▓╬╬╬╬╬╬▓▓╬╬╬╬╣▓▓▓╬▓████▓╠╬▓
         φφ@╬▓▓▒╣╬╬╬╬▓╠▓╣▓▓╬╬╬╬╬╬╬╬╬╬╬╬▓╬╣╬╬╬╬╣╬▓╬▓╬╬╬╣╣╣▓╬███▓▓╬╬╝_
        ╘╬╣╬╬╬╬╬╬╬╬╬╬╬╬▓╬▓▓╬╬╬╬╬╬╬╬╬╣╣╣╬╬╬╬╬╣╣╣╣╣╣╫╬╬╬╬╠╬╬╬╬╬╬╣╬╬╢╠╬▒«
        ╒╩╩╬╬╠╬╟╬╣╣╣╬╬╬▓███████████╩║╬╟╬╬╬▓▓╣╣▓▓╣╣╬╣╬╬▓╬╬╬▓╬╬╬╬╬╬╬╬╬▒░░
       ╠▓▓╣▄╚▓▓▓▓▓▓▓██████████████Ñ▒▓▓█▓█▒╬╬╬╚╙╠▓╬╬╟╬╬╬╬╬╬╬╬╬╬╬╬╬╣╫▓▓▓▓▌
      ║██▓╣▓▓▐█████▓██████████████▐▓▓██▓╬▓▌▒╟▓▓▓▓▓▓██████████▓█╬╬╬╣█▓▓▓Γ
      ║███▓██░█████▓▓▓██████▀▀▀▀▀▀╟▓▓▓▓▓███╬╣▓▓▓▓╬╬╣╬▓╬╣▓▓▓╣╬▓▓▓▓▓▓▓▓▓▀
       ╣████Ñ╟███▀`               ╠╬▓▓████╬╬╫█▓█▀^``        ╙▀███▀▀▀"
        ╙▀╝╝▀▀▀^                   ╙╠╬▓╬╬░╬▓█▓▀
                                     `"╙╙╙""`
                                     
                                     
                                                                               __,,__
                                                                           ,╔░╔╦_  -_▒φ_
                                                                       _ ╓░   ,æ.__ `' _▒
                                                            _ _╔=╦╦▒▒  //_ ⁿB╔-▒._▄▄█▄` ░╬
                                               __,.. ,φ,__   {   __ _ |╔ ___ ║▒╔╚╫████▌@╓_L
                                        ,╔Γ= ╔_ _   ╦  _╔   # _:_Äφ_╔ ╠Ä╦|¼╦╓║▌:Ü▐███╬_.`╠R
                                    _∩╓:▄.╔▄ __|_ /[µ _ÖHjµ µ╔╔µ░▒▒▒▒▒_▒▒╬╬╬▒╢╫▌,.:`»╓_.╦Ü
                                   ╣▌,╚»▐╝╬^````"^▄║▒╦▐╬▒╬╠▌▐╬▒▓╬╣▓▓▓█▓╠▓▓╣▓▓╬╬╠██▄▄_▄▒▓▓`
                                   ╠▒ ╙_█  .     '██▓╣╣▓▓▓▓▓▓╬▓▓▓██████████████▓╬╠╬╬╬╠█╜
                                   '`            _████████████████▀▀^         `"""``
                                                  ███████████████; L `
                         ┌╦╦╦__       ─           ║████████████╬╣≡*╗╩`
                         '`    ²⌐ »#              ║██████████▓╬╬   ╓H
                                   ╙      ________║██████████▓╬▌`
                      ,,,╓_          `._|▒φ▄      ▐███████▀▀█╬╬╠░    ¼╗╦╔,
                       j╓;÷╣           ╔  _`½     ▐█████ __,_ ║▒░    ▐▒ `≈╬
                     - ▐░╠╬╬█▄▄▄▄⌐\-~  [._`  █╗╗╗φ╙""""j╦╔╦,_╦/╚╝╗╗╗╗▓▒r   ▒
                   _▄╓_ ▒╬╬╣████▌ _U_╔   _[▄,╚```    `  "``╙█╩- `╙`╙╠╬Ü|j⌂__
                   ╙▀▀ ▐▓╣▓▓▀▀▀▀▀╠▄█▓▌ ▐▒╠╠╠▒▒       ╔___ ,, ¼╦╓_,__╠░╙[▒▒╠▒
                    '  ████▌        `  ║▓╣▓▓▌  ║╚╠████▄▒▒φ▄▄▒█▓▒▒▒▄╬╩`╒▓▓▓▓Γ
                     `╙╙▀▀╙       ¬`  ╓█████_;;_`""   ╙█▀"```╙█▀   '╬▄████^
                                    `````````    [_;╦╦▒▌___ ,__▒▄_.╓
                                                 '╦▒▒▓▓█▒▄▒▄▄▒▓█▓▓▄▄▌
                                                   ╙╙▀▀ªª▀▀▀▀▀ⁿ╙▀▀╙
                                                   
                     _
                  /)  ( /=)===========..._____
                (\\)(\)()))()=))))))==(==+\==+>())))==========.=......=_
          _.===_ -(>\/(_=(//(\\........_.___                  )    \)=\+     .._
           )))))   )))))=))       <( ))) )  ===_     <<<<++<+<(<<<<<(\+)    ((_)/
           -===/))(  )            (+    =()())                      -==
            _./)===()() ))))()()))      ))))))).
            )))     === )  ))))))== =)===\))))) )
            )    )) ===)(+ ())))))))()()=   )\)
           ) )  ) ) )=        =)))      )(()====
            =() ()=            =()    (  =
              \-              )== )) ))=
                               \== )\ (=
                                 \= =-
                                 
                                                                    ,@  BRw
                                                                   [N B  0B
                                                                   'NN  NNR
                                       @BBBW                         ``"`
                               _,g@RNN NBNRR _
                 ' a,  _,wg@RB     0 N BBR0RRB
                 ,#N  N00BB   B   B 0B0 B@BRRNK
             .-'M"B0    BBBB@BR R 0    NNNN B0R
            _a@ N@w_'  00 BBBB N NNNNRRRN^`"`
          `|^.RR RNNy [NNNNNNNNNRRNM"`
         ,|P  'NHNU@RN [RRRRRRB^N]
          (n-_.  -N  NH 0RRM_```$[
         `'b  _`:` ``0L_N : '% ,,R
          :`_:` : `:   $H__  _]y^
           -`:_ :   `:#M7NN=P^`
            `<,$bb;,aM
                ````
                

                                 

                           ^~  _
                         ,RR [ |` __
                         _`R ` F    C  _
                        ___.%R/      L      -~
                         ^R0RR#,_,~'/-         ''"_
                                `^^R@g,.       ?     <_G _
                                     ,)RR@@S,__{ _,_'^--U|,S  ~
                                   y,335RD[BjiRM^ ^`m,m[Kr `'`\j
                                   ["^22`{[@B        _ "^ _ . -^-
                                   [[_           _          _     _ ` `
                               !D%7'[_'_`   _  j    _-         ;5,__ _ Y=j_
                 /      ,        Ru[|      |@K^   _),=".  _    _A _`[R^^`,Y_
                       __k      /_ |D__  ,^[0`">w==` _.3r_    |P_ _,   R _\Dr
                  _ __.>{/__       !|D A` ``[   - ,^  ,mR,\wU^`_ __R  !   ,`_
              . ` ``|=|`     \_ _'my%w`)   _[   _a   B `'=0[DRR9^` '_ '  U|,
                    ~[       `u '\'BwDB%Kg{{[w,|DH  ) ,| ^ `    _.  'R=%_.D
            [               !|^    ``   _  _     U Y| %@,w<         _. ``
           _  v.  `. |@_.,._R`'            _ -. _ !\ \  V`'   -
            _ ``-=-^ _ _ _ `  _                      ===^ -
                                 
                                                                                      _,,,_
                                                                                    aB  B  R,
                                                                                   [N  BN 0BB
                                                                                   [NN N    R
                                                _,gm,                               '0NNNNR^
                                            ,,,[  B N0,
                                     __,#   NNN 0BB0RR W
                    `' ,_    _,,w#@B       N    BBR RRR L
                      0  KR     BBBBN      BRB0 BB@BNRRR
                   a NN  BB0NBB BRBBRBNR 0B BRNBN B BNNNB
              _-'`  `"~B N   BBRRBBBBNBN    N  NNRNNNN NR
              _a0NRHN w_ R  N B  0 B  NNNNNNNRRRN ^ ``
           , |P $RR NRNNW   NNNNNNNNNNNRRRR M``
            |P   NR_ NC,NN   RRRRRRRRRNNB
            $    `M"BN RRR@ `NRRRR  Ww.&LH
            = `--   ], FT5   $N`]`._   @VH
            (\   ,`'`    T} ,N  @  T, :_
           ` $_,=` ,  `:  ` #R_ ]   _U,R
            ` -W   :`   `, jNN@@@@@@A^
             `(, :,,_  ,:, F    ````
                Yw___,,>^"
                                 

                                
                     _
                  /)  ( /=)===========..._____
                (\\)(\)()))()=))))))==(==+\==+>())))==========.=......=_
          _.===_ -(>\/(_=(//(\\........_.___                  )    \)=\+     .._
           )))))   )))))=))       <( ))) )  ===_     <<<<++<+<(<<<<<(\+)    ((_)/
           -===/))(  )            (+    =()())                      -==
            _./)===()() ))))()()))      ))))))).
            )))     === )  ))))))== =)===\))))) )
            )    )) ===)(+ ())))))))()()=   )\)
           ) )  ) ) )=        =)))      )(()====
            =() ()=            =()    (  =
              \-              )== )) ))=
                               \== )\ (=
                                 \= =-
                                                                                                                  _,,,,_
                                                            ,▒ ▒² _.._K_
                                                   ___,╔╔⌐╔▒ »╔[▒` ,_  ,╕
                                       _____╔╔#▒__░  ,╓_ [____[▌_²████╔╓_
                               _,╔ñ= ∩__  ╔  ╓ / ▒,!_Ö▒╔_╗µ;φ▄[█'╗╝██╩:_╠
                             ╖£╔ W▄▒,╦▄╦▒ ░_╔╠╔▓▄Ü▒▄▒╬▒▓▌[▓▒╬▒╬╝█▄'`)╔µ▓▌
                             ╫ ╠ █  _   ¢█║▓▓▓▓╣█╬╣╬▓▓▓██████▓██▒╬██▓██╜
                             ╙```       _████████████▀▀▀"`     "╙╙""`
                                         ████████████░  H
                     j.  __  _           ██████████╬╙╙▀Ñ
                     |       L           █████████╬╬  ╙`
                  ___]_   ` ``  _╔╦▄     ║█████▀▀█╬╬▒  ▒╔╓╓,
                   j╔»▒▄        ╠'  ¼    ║███▌,_╓_╙░▌   ▐░ ⁿ▒
                 `  ░╠╬▓███`▐`_ [  . ██▀▒    ╚▓╣▄▄R╚╚▀███▒__ H
                i▓▌ ╠╬╬████_╓▓▄ jµ╦╠φ░      __,_ ╙Ü╔__╠╠ÑH▒▒╔Ñ
                 │ ║███      `` ║▒▓▓Γ ╚j▓███▄▄▄╦▄▄█▒▒▄╬Ö`▐▓▓▓
                  """"       ` ▄███▀_╓╓```  ╠╬^   ╣Γ   ╚Φ██▀
                                        ╚▄╓╣▓▒╓▄_╔╓█▄_╔▄
                                         ╙███▄▓▓▓▓▌███▀`


")


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
	await ctx.channel.send(rf"""```
     ^  +~+~~
    ^   )`.).
      )``)``) .~~
      ).-'.-')|)
    |-).-).-'_'-/
 ~~~\ `o-o-o'  /~~~~~~~~~~~~~~~~~
  ~~~'---.____/~~~~~~~~~~~~~~
{user_name} performs an evasive maneuver!
```""")  # MAY NEED TO GET RID OF ``` CODE FORMATTING


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
	await turn_actions(ctx, player, 'aim')
	await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


async def turn_actions(ctx, player, action):
	"""Creates stack of actions taken by each player."""
	turn = game['turn']
	game['turn_log'][f'turn_{turn}'][player] = action
	await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


async def turn_end(ctx):  # need to add message feedback for game states
	"""Performs end of turn cleanup."""
	turn = game['turn']
	player_1 = list(game['turn_log'][f'turn_{turn}'].values())[0]  # listify values of current turn to index into
	# player
	player_2 = list(game['turn_log'][f'turn_{turn}'].values())[1]
	player_1_action = game['turn_log'][f'turn_{turn}'][player_1]
	player_2_action = game['turn_log'][f'turn_{turn}'][player_2]

	if player_1_action == 'fire':
		player_2.health -= player_1.fire(player_2)
		player_1.aimed = False

	if player_2_action == 'fire':
		player_1.health -= player_2.fire(player_1)
		player_2.aimed = False

	if player_1_action == 'aim':  # provide message feedback for missed aim
		if player_2.maneuvered:
			return
		player_1.aim()

	if player_2_action == 'aim':
		if player_1.maneuvered:
			return
		player_2.aim()

	# need to add handling/checking for 3 maneuvers in a row
	if player_1_action == 'maneuver':
		maneuvers = 0
		try:
			if game['turn_log'][f'turn_{turn-1}'][player_1] == 'maneuver':
				if game['turn_log'][f'turn_{turn-2}'][player_1] == 'maneuver':
					player_1.fouled = True
		except IndexError:
			pass

	if player_2_action == 'maneuver':
		maneuvers = 0
		try:
			if game['turn_log'][f'turn_{turn-1}'][player_2] == 'maneuver':
				if game['turn_log'][f'turn_{turn-2}'][player_2] == 'maneuver':
					player_2.fouled = True
		except IndexError:
			pass

	player_1.maneuvered = False
	player_2.maneuvered = False
	player_1.fouled = False
	player_2.fouled = False

	game['turn'] += 1
	await ctx.channel.send(f"{user_name} accepted {game['players']['challenger'].name}'s challenge!")


bot.run('')
