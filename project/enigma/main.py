import Enigma

enigmamachine = Enigma.Enigma(["I", "II", "III"], "B", [0, 0, 0], [0, 0, 0], "AB CD EF GH IJ KL MN OP QR ST UV WX YZ")
plaintext = "HELLOWORLD"
ciphertext = enigmamachine.encrypt_string(plaintext)
print(ciphertext)
