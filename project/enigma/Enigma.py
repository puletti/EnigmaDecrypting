from Rotor import Rotor
from Reflector import Reflector
from Plugboard import Plugboard
class Enigma:
    # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
    # A B C D E F G H I J K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
    def __init__(self, rotors, reflector, rotor_positions, ring_settings, plugboard_connections):
        self.left_rotor = Rotor.create(rotors[0], rotor_positions[0], ring_settings[0])
        self.middle_rotor = Rotor.create(rotors[1], rotor_positions[1], ring_settings[1])
        self.right_rotor = Rotor.create(rotors[2], rotor_positions[2], ring_settings[2])
        self.reflector = Reflector.create(reflector)
        self.plugboard = Plugboard(plugboard_connections)

    def rotate(self):
        # If middle rotor notch - double-stepping
        if self.middle_rotor.is_at_notch():
            self.middle_rotor.turnover()
            self.left_rotor.turnover()
        # If left-rotor notch
        elif self.right_rotor.is_at_notch():
            self.middle_rotor.turnover()

        # Increment right-most rotor
        self.right_rotor.turnover()

    def encrypt(self, c):
        self.rotate()

        # Plugboard in
        c = self.plugboard.forward(c)

        # Right to left
        c1 = self.right_rotor.forward(c)
        c2 = self.middle_rotor.forward(c1)
        c3 = self.left_rotor.forward(c2)

        # Reflector
        c4 = self.reflector.forward(c3)

        # Left to right
        c5 = self.left_rotor.backward(c4)
        c6 = self.middle_rotor.backward(c5)
        c7 = self.right_rotor.backward(c6)

        # Plugboard out
        c7 = self.plugboard.forward(c7)

        return c7

    def encrypt_char(self, char):
        return chr(self.encrypt(ord(char) - 65) + 65)

    def encrypt_string(self, input_str):
        return ''.join(self.encrypt_char(char) for char in input_str)

# Example Usage:
# enigma = Enigma(["VII", "V", "IV"], "B", [10, 5, 12], [1, 2, 3], "AD FT WH JO PN")
# encrypted_text = enigma.encrypt_string("HELLOWORLD")
# print(encrypted_text)

# e2 = Enigma(["VII", "V", "IV"], "B", [10, 5, 12], [1, 2, 3], "AD FT WH JO PN")
# decrypted_text = e2.encrypt_string(encrypted_text)
# print(decrypted_text)

# left = Rotor.create("II", 7, 12)
#     middle = Rotor.create("V", 4, 2)
#     right = Rotor.create("III", 19, 20)

#     machine = Enigma([left, middle, right], "B", "AD FT WH JO PN")
