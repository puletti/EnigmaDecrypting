class Rotor:
    def __init__(self, name, encoding, rotor_position, notch_position, ring_setting):
        self.name = name
        self.forward_wiring = self.decode_wiring(encoding)
        self.backward_wiring = self.inverse_wiring(self.forward_wiring)
        self.rotor_position = rotor_position
        self.notch_position = notch_position
        self.ring_setting = ring_setting

    @staticmethod
    def create(name, rotor_position, ring_setting):
        rotor_configs = {
            "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 16),
            "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", 4),
            "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", 21),
            "IV": ("ESOVPZJAYQUIRHXLNFTGKDCMWB", 9),
            "V": ("VZBRGITYUPSDNHLXAWMJQOFECK", 25),
            "VI": ("JPGVOUMFYQBENHZRDKASXLICTW", 0),
            "VII": ("NZJHGRCXMYSWBOUFAIVLPEKQDT", 0), 
            "VIII": ("FKQHTLXOCBJSPDZRAMEWNIUYGV", 0) 
        }

        encoding, notch_position = rotor_configs.get(name, ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 0))
        return Rotor(name, encoding, rotor_position, notch_position, ring_setting)

    def get_name(self):
        return self.name

    def get_position(self):
        return self.rotor_position

    @staticmethod
    def decode_wiring(encoding):
        return [ord(char) - 65 for char in encoding]

    @staticmethod
    def inverse_wiring(wiring):
        return [wiring.index(i) for i in range(len(wiring))]

    @staticmethod
    def encipher(k, pos, ring, mapping):
        shift = pos - ring
        return (mapping[(k + shift + 26) % 26] - shift + 26) % 26

    def forward(self, c):
        return self.encipher(c, self.rotor_position, self.ring_setting, self.forward_wiring)

    def backward(self, c):
        return self.encipher(c, self.rotor_position, self.ring_setting, self.backward_wiring)

    def is_at_notch(self) -> bool:
        if self.name == "VI" or self.name == "VII" or self.name == "VIII":
            return self.rotor_position == 12 or self.rotor_position == 25
        return self.rotor_position == self.notch_position

    def turnover(self):
        self.rotor_position = (self.rotor_position + 1) % 26
