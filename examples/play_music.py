from time import sleep
from robot_hat import Music

MUSIC_FILE = './musics/nhac-viet.mp3'
VOLUME = 50  # 0-100

def main():
    music = Music()
    music.music_set_volume(VOLUME)

    print(f"Playing {MUSIC_FILE} (Ctrl+C to stop)")
    music.music_play(MUSIC_FILE)

    try:
        while True:
            sleep(0.5)
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        music.music_stop()

if __name__ == "__main__":
    main()
