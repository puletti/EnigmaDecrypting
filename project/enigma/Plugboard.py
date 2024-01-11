class Plugboard:
    def __init__(self, connections):
        self.wiring = self.decode_plugboard(connections)

    def forward(self, c):
        return self.wiring[c]

    @staticmethod
    def identity_plugboard():
        return list(range(26))

    @staticmethod
    def get_unplugged_characters(plugboard):
        unplugged_characters = set(range(26))

        if not plugboard:
            return unplugged_characters

        pairings = [char for char in plugboard if char.isalpha()]

        for pair in pairings:
            c1 = ord(pair[0]) - 65
            c2 = ord(pair[1]) - 65

            unplugged_characters.discard(c1)
            unplugged_characters.discard(c2)

        return unplugged_characters

    @staticmethod
    def decode_plugboard(plugboard):
        if not plugboard:
            return Plugboard.identity_plugboard()

        pairings = [pair for pair in plugboard.split() if len(pair) == 2 and pair.isalpha()]
        plugged_characters = set()
        mapping = Plugboard.identity_plugboard()

        for pair in pairings:
            c1 = ord(pair[0]) - 65
            c2 = ord(pair[1]) - 65

            if c1 in plugged_characters or c2 in plugged_characters:
                return Plugboard.identity_plugboard()

            plugged_characters.add(c1)
            plugged_characters.add(c2)

            mapping[c1] = c2
            mapping[c2] = c1

        return mapping
