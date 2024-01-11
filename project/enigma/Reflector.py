class Reflector:
    def __init__(self, encoding):
        self.forward_wiring = self.decode_wiring(encoding)

    @staticmethod
    def create(name):
        reflector_configs = {
            "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
            "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
        }
        encoding = reflector_configs.get(name, "ZYXWVUTSRQPONMLKJIHGFEDCBA")
        return Reflector(encoding)

    @staticmethod
    def decode_wiring(encoding):
        return [ord(char) - 65 for char in encoding]

    def forward(self, c):
        return self.forward_wiring[c]
