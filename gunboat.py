# 4 actions, one per turn: fire, dodge/maneuver, reload, aim
# 3 health
# non-dodged/connected shots deal 1 damage
# first player to 0 health loses
# FIRE: 3 ammo, one expended per shot
# RELOAD: reloads all 3 ammo
# MANEUVER: dodges a fire action on same turn
# 	3 maneuvers in a row opens you up to a critical hit (2x dmg)
# AIM: takes aim to prepare critical hit for next fire (2x dmg)
# 	aim broken if fired upon while taking aim or target ship maneuvers during
# 	aim (effectively only works if other
# 	ship is reloading or aiming)


class Frigate:
    """Player boat."""

    def __init__(self, name):
        """Initializes a player's frigate."""
        self.name = name
        self.health = 3
        self.ammo = 3
        self.attack = 1
        self.maneuvered = False  # status set by maneuver action, cleared
        # after 1 turn
        self.aimed = False  # aiming status, set if successful aim action
        # taken, dmg calc looks here for crit
        self.fouled = (
            False
            # status set with 3 maneuvers in a row, dmg calc looks here for
            # crit
        )
        # maybe using past action attribute will help tracking 3 maneuvers
        self.maneuvers = 0  # track maneuvers in a row
        self.last_action = None
        self.aimed_fouled_status = (False, False)

    def fire(self, opponent):
        """Fires cannons at opponent."""
        self.ammo -= 1
        if opponent.maneuvered:
            return 0
        if self.aimed or opponent.fouled:
            return self.attack * 2
        self.maneuvers = 0
        self.last_action = "fire"
        return self.attack

    def maneuver(self):
        """Maneuvers player ship to dodge attacks."""
        self.maneuvers += 1
        self.last_action = "maneuver"
        if self.maneuvers >= 3:
            self.fouled = True
        self.maneuvered = True

    def reload(self):
        """Reloads all three cannons."""
        self.maneuvers = 0
        self.last_action = "reload"
        self.ammo = 3

    def aim(self):
        """Aims at opponent to ready critical hit."""
        self.maneuvers = 0
        self.last_action = "aim"
        self.aimed = True
