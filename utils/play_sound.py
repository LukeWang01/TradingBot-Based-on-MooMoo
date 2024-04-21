# import simpleaudio as sa
# from pydub import AudioSegment
# from pydub.playback import play
import sounddevice as sd
import soundfile as sf
# using pydub to play audio files instead of simpleaudio
# simpleaudio is not working on some systems
# Note: there will be no sound when the code exit immediately


def order_placed():
    # # Load the sound file
    # wave_obj = sa.WaveObject.from_wave_file('audio/order_placed.wav')
    #
    # # Play the sound file
    # play_obj = wave_obj.play()
    #
    # # Wait for the sound to finish playing
    # # play_obj.wait_done()
    # Load audio file
    # audio = AudioSegment.from_file("audio/order_placed.wav")
    #
    #
    # # Play audio
    # play(audio)

    # Load audio file
    data, samplerate = sf.read("audio/order_placed.wav")
    # Play audio
    sd.play(data, samplerate)
    sd.wait()


def strategy_notified():
    # Load the sound file
    # wave_obj = sa.WaveObject.from_wave_file('audio/strategy_notified.wav')
    # Play the sound file
    # play_obj = wave_obj.play()
    # Wait for the sound to finish playing
    # play_obj.wait_done()
    #
    # audio = AudioSegment.from_file("audio/strategy_notified.wav")
    # play(audio)

    # Load audio file
    data, samplerate = sf.read("audio/strategy_notified.wav")
    # Play audio
    sd.play(data, samplerate)
    sd.wait()
