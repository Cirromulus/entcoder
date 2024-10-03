#!/usr/bin/python3

import wave
import sys
import pyaudio

CHUNKSIZE = 1024

q1_file = r"samples/quack1.wav"
q2_file = r"samples/quack2.wav"

q1 = wave.open(q1_file, 'rb')
q2 = wave.open(q2_file, 'rb')
# TODO: Check whether actually the same
sample_width = q1.getsampwidth()
rate = q1.getframerate()
channels = q1.getnchannels()

def chooseQuack(number : bool):
    if number:
        return q1
    else:
        return q2

def playQuack(stream : pyaudio.Stream, file : wave.Wave_read):
    while len(data := file.readframes(CHUNKSIZE)):  # Requires Python 3.8+ for :=
        stream.write(data)
    file.rewind()


# Instantiate PyAudio and initialize PortAudio system resources (1)
p = pyaudio.PyAudio()

# Open stream (2)
stream = p.open(format=p.get_format_from_width(sample_width),
                channels=channels,
                rate=rate,
                output=True)


for line in sys.stdin:
    if 'Exit' == line.rstrip():
        break
    for c in line.encode('ascii'):
        print (f"{chr(c)}: {c:b}")
        for bit_offs in range(7):    # MSB in ascii is redundant
            bit = bool((1 << bit_offs) & c)
            print (f"    {bit_offs}: {"quack" if bit else "also quack"}")
            playQuack(stream, chooseQuack(bit))

print ("OK Tenks by")

# Close stream (4)
stream.close()

# Release PortAudio system resources (5)
p.terminate()