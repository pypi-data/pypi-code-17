from customplayer import mPlayer

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
