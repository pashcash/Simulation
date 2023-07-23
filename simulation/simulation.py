from dataclasses import dataclass, field
import simulation as sim
import datetime

from random import choice

@dataclass
class simulation:
    characters: dict[str, sim.character] = field(default_factory=dict)
    advertisements: dict[str, sim.advertisement] = field(default_factory=dict)
    _ticks: int = 0
    DATETIME_START = datetime.datetime(2023, 7, 15, hour=12, minute=00)

    @property
    def ticksPassed(self) -> int:
        return self._ticks

    @property
    def currentTime(self):
        t = self.ticksPassed
        current_time = self.DATETIME_START + datetime.timedelta(minutes=t)
        return current_time.strftime("%H:%M")
    
    def ticksAdd(self, ticks: int) -> None: 
        """Moves time forward, increasing tickes and decreasing all characters' motive fulfillment

        ticks : int
            specify time passed (measured in ticks)
        """
        self._ticks += ticks
        for char in self.characters.values():
            char.decayAllMotives(ticks)
            char.reorderMotives()

    def chooseAdvertismentToFulfillMotive(self, motive: str) -> sim.advertisement | None: 
        all_ads = self.advertisements.values()
        options = list(filter(lambda ad: ad.motive==motive, all_ads))
        action = choice(options) if options != [] else None
        return action
    
    def retrieveCharacterStatus(self, character_id: str) -> str: 
        character = self.characters[character_id]
        return character.status(self.ticksPassed)
    
    def retrieveCharacterMotives(self, character_id: str) -> dict[str, int]:
        character = self.characters[character_id]
        motives: dict[str, int] = {}
        for key, mot in character.motives.items(): 
            motives[key] = mot.percentage
        return motives
