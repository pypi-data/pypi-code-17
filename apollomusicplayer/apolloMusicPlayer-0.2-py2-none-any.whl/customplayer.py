import musicplayer, logging


class playableSong:
    def __init__(self, fn):
        self.url = fn
        self.f = open(fn)

    # `__eq__` is used for the peek stream management
    def __eq__(self, other):
        return self.url == other.url

    # this is used by the player as the data interface
    def readPacket(self, bufSize):
        return self.f.read(bufSize)

    def seekRaw(self, offset, whence):
        r = self.f.seek(offset, whence)
        return self.f.tell()


class mPlayer:
    def __init__(self):
        # needs at least 2 things to start for some reason
        self.queue = ["/Users/admin/Music/iTunes/iTunes Media/Music/Adrian Marcel/Unknown Album/2AM.mp3",
                      "/Users/admin/Music/iTunes/iTunes Media/Music/Penn Masala/Unknown Album/_Down.mp3"]
        self.player = musicplayer.createPlayer()
        self.player.outSamplerate = 96000  # support high quality :)
        self.player.queue = self.gen_song_queue()
        self.song_index = 1

    def print_queue(self):
        # print songs in the queueo
        print(self.queue)

    def gen_song_queue(self):
        # generates the song queue
        while True:
            if self.song_index < len(self.queue):
                yield playableSong(self.queue[self.song_index])
                if self.song_index > 1:
                    self.queue.remove(self.song_index)
                else:
                    self.song_index += 1
            else:
                print("stopped")
                self.player.playing = False
                yield self.queue[0]  # have a blank song here

    def add_song_to_queue(self, filename):
        # add song to queue
        self.queue.append(filename)

    def play(self):
        # play music
        self.player.playing = True

    def pause(self):
        # play music
        self.player.playing = False

    def skip(self):
        # skip a song
        self.player.nextSong()

    def play_song(self, filename):
        self.queue.insert(self.song_index, filename)
        self.song_index -= 1
        self.skip()

    def change_volume(self, new_volume):
        # change volume
        print(new_volume)
        assert (new_volume >= 0)
        assert(new_volume <= 100)
        #call(["amixer", "-D", "pulse", "sset", "Master", str(new_volume) + "%"])
        self.player.volume = new_volume;


if __name__ == "__main__":
    raw_input("press enter to begin tests")
    player = mPlayer()
    player.print_queue()
    raw_input("a list of mp3s should have been printed - enter to continue")
    player.play()
    raw_input("the first song should have played- enter to pause")
    player.pause()
    raw_input("the song should be paused - enter to resume")
    player.play()
    raw_input("song should resume not start over enter to pause and continue")
    file_name = raw_input("enter a song file such as songs/testSongs/Bed Of Roses.mp3 to play it")
    if file_name == "":
        file_name = 'test_resources/Bed Of Roses.mp3'
    player.play_song(file_name)
    test = raw_input("should play bed of roses - hit enter to continue and end the tests")
