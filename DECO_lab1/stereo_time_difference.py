import soundfile as sf
import numpy as np

def set_time_difference(degree):
    '''Set time difference with figure 2b '''
    if degree == 0:
        time_difference = 0
        samples = 0
    elif degree == 10:
        time_difference = 0.1    
    elif degree == 20:
        time_difference = 0.3 
    elif degree == 30:
        time_difference = 1 
    samples = round(time_difference / 1000 * 48000)
    return time_difference, samples


def generate_stereo_sound(samples, soundfile):
    '''Generate stereo sound with samples calculated before.'''
    delay_sound = np.zeros(samples)
    mono_sound, fs = sf.read(soundfile)
    left_sound = np.concatenate((mono_sound, delay_sound)) 
    right_sound = np.concatenate((delay_sound,mono_sound)) 
    # Combine two channels together
    stereo_sound = np.vstack((left_sound, right_sound)).T
    return stereo_sound

def time_panning(degree, soundfile):
    '''Perform amplitude panning based on the setted time difference. '''
    time_difference, samples = set_time_difference(degree)
    sound = generate_stereo_sound(samples, soundfile)
    print(f"At {degree}º: tL − tR = {samples} samples, {time_difference} ms.")
    return sound


soundfile = 'DECO_mono.wav'
# Time panning
sound_0_front = time_panning(0, soundfile)   # 0º (this is, the front)
sound_10_right = time_panning(10, soundfile) # 10ºon the right
sound_20_right = time_panning(20, soundfile) # 20ºon the right
sound_30_right = time_panning(30, soundfile) # 30ºon the right (this is, the right speaker)

# Concatenate sounds and save the final sound file
final_sound = np.concatenate((sound_0_front, sound_10_right, sound_20_right, sound_30_right))
sf.write('DECO_stereo_time.wav',final_sound, 48000)
