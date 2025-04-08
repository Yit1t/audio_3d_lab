import soundfile as sf
import math
import numpy as np


def calculate_gains(degree):
    '''Calculate gains using the tangent law and coherent summation hypothesis.'''
    
    # Convert degree to radians for math.tan function
    degree_rad = math.radians(degree)

    # Set a set of gains, which represent the gains of six channels
    gains = [0, 0, 0, 0, 0, 0]

    # Tan of bisected angles
    tan_30 = math.tan(math.radians(30)) # Half of the angle of fronts
    tan_40 = math.tan(math.radians(40)) # Half of the angle of surround and front
    tan_70 = math.tan(math.radians(70)) # Half of the angle of surrounds

    if degree == 0: # When the sound come from the center front
        gains[2] = 1
    elif - 30 <= degree <= 30 and degree != 0: # When the sound is between the left front and the right front. In addition, the sound is not from the center
        gain_1 = 0.5 * (1 + math.tan(degree_rad) / tan_30)
        gain_2 = 1 - gain_1
        gains[0] = gain_1/(gain_1**2+gain_2**2)**0.5
        gains[1] = gain_2/(gain_1**2+gain_2**2)**0.5
    elif 30 < degree <= 110: # Between the left front and left surround
        degree = degree - (30 + 40) # Redefine the involved angles
        gain_1 = 0.5 * (1 + math.tan(degree_rad) / tan_40)
        gain_2 = 1 - gain_1
        gains[0] = gain_1/(gain_1**2+gain_2**2)**0.5
        gains[4] = gain_2/(gain_1**2+gain_2**2)**0.5
    elif -110 < degree <= -30: # Between the right front and the right surround
        degree = degree - (-30 - 40) # Redefine the involved angles
        gain_1 = 0.5 * (1 + math.tan(degree_rad) / tan_40)
        gain_2 = 1 - gain_1
        gains[1] = gain_1/(gain_1**2+gain_2**2)**0.5
        gains[5] = gain_2/(gain_1**2+gain_2**2)**0.5
    elif 110 < degree <= 180: # The left rear
        degree = degree - 180 # Redefine the involved angles
        gain_1 = 0.5 * (1 + math.tan(degree_rad) / tan_70)
        gain_2 = 1 - gain_1
        gains[4] = gain_1/(gain_1**2+gain_2**2)**0.5
        gains[5] = gain_2/(gain_1**2+gain_2**2)**0.5
    elif  -180 <= degree < -110: # The right rear
        degree = degree + 180 # Redefine the involved angles
        gain_1 = 0.5 * (1 + math.tan(degree_rad) / tan_70)
        gain_2 = 1 - gain_1
        gains[4] = gain_1/(gain_1**2+gain_2**2)**0.5
        gains[5] = gain_2/(gain_1**2+gain_2**2)**0.5

    return gains




def generate_stereo_sound(gains, soundfile):
    '''Generate stereo sound with gains calculated before.'''
    mono_sound, fs = sf.read(soundfile)
    # Combine channels together
    length = len(mono_sound)
    five_one = np.zeros((length, 6))
    five_one[:, 0] = mono_sound * gains[0]  # Front left
    five_one[:, 1] = mono_sound * gains[1]  # Front right
    five_one[:, 2] = mono_sound * gains[2] # Center
    five_one[:, 3] = 0 * gains[3] # LFE (I set it zero here, because I think we don't really need it in this panning lab)
    five_one[:, 4] = mono_sound * gains[4]    # Surround left
    five_one[:, 5] = mono_sound * gains[5]  # Surround right
    return five_one

def surround_panning(degree, soundfile):
    '''Perform amplitude panning based on a given degree. '''

    gains = calculate_gains(degree)
    sound = generate_stereo_sound(gains, soundfile)
    print(f"At {degree}º: gLf = {gains[0]}, gRf = {gains[1]}, gCen = {gains[2]}, gLFE = {gains[3]}, gLs = {gains[4]}, gRs = {gains[5]}")
    return sound


soundfile = 'DECO_mono.wav'
# Amplitude panning
sound_0_front = surround_panning(0, soundfile)   # 0º
sound_60_left = surround_panning(60, soundfile) # 60º on the right
sound_90_left = surround_panning(90, soundfile) # 90º on the right
sound_180_rear = surround_panning(180, soundfile) # 180º in the rear

# Concatenate sounds and save the final sound file
final_sound = np.concatenate((sound_0_front, sound_60_left, sound_90_left, sound_180_rear))
sf.write('DECO_51_intensity.wav',final_sound, 48000)
