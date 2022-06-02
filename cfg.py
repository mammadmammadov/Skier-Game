import os

FPS = 50

WINDOWS_SIZE = (640, 600)

# getcwd= get current working directory - location of your module

# taking the resources

SKIER_IMAGE_PATHS = [
    os.path.join(os.getcwd(), 'resources/images/skier_forward.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_right1.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_right2.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_left2.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_left1.png'),
    os.path.join(os.getcwd(), 'resources/images/skier_fall.png')
    ]

OBSTACLE_PATHS = {
    'tree': os.path.join(os.getcwd(), 'resources/images/tree.png'),
    'flag': os.path.join(os.getcwd(), 'resources/images/flag.png')
    }

MUSIC_PATH = os.path.join(os.getcwd(), 'resources/music/music.mp3')
MUSIC_PATH_2 = os.path.join(os.getcwd(), 'resources/music/gameover.mp3')

FONT_PATH = os.path.join(os.getcwd(), 'resources/font/FZSTK.TTF')

