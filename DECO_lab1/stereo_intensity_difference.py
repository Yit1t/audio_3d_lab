import soundfile as sf
import math
import numpy as np

def calculate_gains(degree):
    '''Calculate gains using the tangent law and coherent summation hypothesis.'''
    # Convert degree to radians for math.tan function
    degree_rad = math.radians(degree)
    
    # Tan of 30 degrees
    tan_30 = math.tan(math.radians(30))
    
    # Calculate gain_l and gain_r based on the formulas
    gain_l = 0.5 * (1 + math.tan(degree_rad) / tan_30)
    gain_r = 1 - gain_l
    
    # Get the final results by using the normalization equations
    gain_l_normalized = gain_l/(gain_l**2+gain_r**2)**0.5
    gain_r_normalized = gain_r/(gain_l**2+gain_r**2)**0.5


    return gain_l_normalized, gain_r_normalized


def generate_stereo_sound(gain_l, gain_r, soundfile):
    '''Generate stereo sound with gains calculated before.'''
    mono_sound, fs = sf.read(soundfile)
    left_sound = mono_sound * gain_l
    right_sound = mono_sound * gain_r
    # Combine two channels together
    stereo_sound = np.vstack((left_sound, right_sound)).T
    return stereo_sound

def amplitude_panning(degree, soundfile):
    '''Perform amplitude panning based on a given degree. '''
    gain_l, gain_r = calculate_gains(degree)
    sound = generate_stereo_sound(gain_l, gain_r, soundfile)
    print(f"At {degree}º: gLeft ={gain_l}, gRight = {gain_r}")
    return sound


soundfile = 'DECO_mono.wav'
# Amplitude panning
sound_0_front = amplitude_panning(0, soundfile)   # 0º
sound_10_right = amplitude_panning(-10, soundfile) # 10ºon the right
sound_20_right = amplitude_panning(-20, soundfile) # 20ºon the right
sound_30_right = amplitude_panning(-30, soundfile) # 30ºon the right (this is, the right speaker)

# Concatenate sounds and save the final sound file
final_sound = np.concatenate((sound_0_front, sound_10_right, sound_20_right, sound_30_right))
sf.write('DECO_stereo_intensity.wav',final_sound, 48000)
