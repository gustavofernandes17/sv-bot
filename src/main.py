
import os
from recorder import Recorder

from utils import get_token
from simov import SimovTelegram




def main():

    recorder = Recorder()

    simov_bot = SimovTelegram(get_token(os.getcwd() + '/token.json'), None, recorder, None)

    simov_bot.init()


if __name__ == '__main__':
    main() 


