import time
import pygame


def communism():
    pygame.mixer.init()
    pygame.mixer.music.load('The_Party_Troll.ogg')
    pygame.mixer.music.play()

    for i in range(17):
        print('☭' * (2**i))
        time.sleep(1)

    pygame.mixer.music.stop()


# print('*heavy soviet accent* The time is right..... *heavy soviet accent*')
# time.sleep(2)
# print("It's happening.....")
# for i in range(3):
#     time.sleep(0.5)
#     print('. ', end='')
# print()
# time.sleep(0.75)
# print('It is time....')
# time.sleep(1)
# print('.....The Revolution.....')
# time.sleep(1)
# print(".....has begun.....")
communism()
