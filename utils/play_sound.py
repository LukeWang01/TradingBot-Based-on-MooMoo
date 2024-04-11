import simpleaudio as sa

# Note: there will be no sound when the code exit immediately


def order_placed():
    # Load the sound file
    wave_obj = sa.WaveObject.from_wave_file('audio/order_placed.wav')

    # Play the sound file
    play_obj = wave_obj.play()

    # Wait for the sound to finish playing
    # play_obj.wait_done()


def strategy_notified():
    # Load the sound file
    wave_obj = sa.WaveObject.from_wave_file('audio/strategy_notified.wav')

    # Play the sound file
    play_obj = wave_obj.play()

    # Wait for the sound to finish playing
    # play_obj.wait_done()
