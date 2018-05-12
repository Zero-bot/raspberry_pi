#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import random

BZRPin = 37

GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
GPIO.setup(BZRPin, GPIO.OUT)   # Set pin mode as output
GPIO.output(BZRPin, GPIO.LOW)

p = GPIO.PWM(BZRPin, 50) # init frequency: 50HZ
p.start(50)  # Duty cycle: 50%

c = [32, 65, 131, 262, 523]
db= [34, 69, 139, 277, 554]
d = [36, 73, 147, 294, 587]
eb= [37, 78, 156, 311, 622]
e = [41, 82, 165, 330, 659]
f = [43, 87, 175, 349, 698]
gb= [46, 92, 185, 370, 740]
g = [49, 98, 196, 392, 784]
ab= [52, 104, 208, 415, 831]
a = [55, 110, 220, 440, 880]
bb= [58, 117, 223, 466, 932]
b = [61, 123, 246, 492, 984]

cmajor = [c, d, e, f, g, a, b]
aminor = [a, b, c, d, e, f, g]

def playScale(scale, pause):
    '''
    scale: scale name to be played
    pause: pause between each notes played
    
    This function plays the given scale in every available octave
    I used this to test what was audible on the buzzer
    '''
    for i in range(0, 5):
        for note in scale:
            p.ChangeFrequency(note[i])
            time.sleep(pause)
    p.stop()
 
#call the playScale function   
#playScale(aminor, 0.5)

'''
How melodies are transposed into code that is played on buzzer:
Every song needs two lists, one to store the variables for the notes and octaves,
and one to store the corresponding lengths of the beats for each note.
The length of both lists MUST be the same. Numbers are used to indicate the note length.
In the case of most melodies:
0.5 = eighth 
1 = quarter note
2 = half note
3 = dotted half note
4 = whole note
This is a relative system, even if a piece is composed mainly in eighth notes or smaller
you should convert the time so that you're using mainly values of 1, 2, 3, and 4 for your notes list.
Actual numbers can be adjusted up or down slightly to account for any fermata or accents,
for example a quarter note with a fermata could be a value of 1.05 or 1.1.
The actual tempo is adjusted when the song is played. The note number system decribed above
is to classify the notes RELATIVE to each other in the song, not when the song is played.
Tempo can be experimentally tested when the function to play the song is called.
All songs should be composed in the key of C whenever possible as the lowest note available
is a C and doing so would simplify the octave referencing.
The easiest way to encode a song's info so it can be played is to do it by ear.
This method and the playSong function currently only support one buzzer, though in the 
future two buzzer support might be added. 
'''

#Star Wars Theme -- Key of C
starwars_notes = [c[1], g[1], f[1], e[1], d[1], c[2], g[1], f[1], e[1], d[1], c[2], g[1],f[1], e[1], f[1], d[1]]
starwars_beats = [4,4,1,1,1,4,4,1,1,1,4,4,1,1,1,4]

#London Bridges --Key of C
londonbridges_notes = [g[1], a[1], g[1], f[1], e[1], f[1], g[1], d[1], e[1], f[1], e[1], f[1], g[1], g[1], a[1], g[1], f[1], e[1], f[1], g[1],d[1], g[1], e[1], c[1]]
londonbridges_beats = [2, 0.5, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 0.5, 1, 1, 1, 1, 2, 2, 2, 1,1]

def playSong(songnotes, songbeats, tempo):
    '''
    songnotes: list of the melodies notes
    songbeats: list of melodies beat times
    tempo: speed of song, this is not traditional tempo in bpm like on a metronome, 
        but more like a multiplier for whatever the notes are so a tempo value of 2 
        make it play twice as fast. Adjust this by ear.
        
    This function plays the melody, simply by iterating through the list. 
    '''
    p.ChangeDutyCycle(50)
    for i in range(0, len(songnotes)):
        p.ChangeFrequency(songnotes[i])
        time.sleep(songbeats[i]*tempo)
    p.ChangeDutyCycle(0)

def random_notes():
	merged = a + b + c + d + e + f + g + ab + bb + db + eb + gb
	random_list = list(range(100, 2999, 2))
	rand_beats = [2, 1, .5]
	p.ChangeDutyCycle(50)
	while True:
		n = random.randint(0, len(random_list)-1)
		beats = random.randint(0, len(rand_beats)-1)
		print('Notes:' + str(n) + ' Beats:' + str(beats))
		
		p.ChangeFrequency(random_list[n])
		time.sleep(rand_beats[beats] * 0.2)
try:
	while True:
		# for f in [34, 69, 139, 277, 554]:
			# p.ChangeFrequency(f)
			# time.sleep(0.2)
		# for f in [58, 117, 223, 466, 932]:
			# p.ChangeFrequency(f)
			# time.sleep(0.2)
		# playSong(starwars_notes, starwars_beats, 0.2)
		# playSong(londonbridges_notes, londonbridges_beats, 0.3)
		random_notes()
except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
