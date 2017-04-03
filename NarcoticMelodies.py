from midiutil import MIDIFile
import random
import argparse


class Melody:
    """Create melody with specified name, mood (sad/energetic/creepy) and tempo using chords progression. """
    def __init__(self, name, mood, tempo):
        self._name = name
        self._mood = mood
        self._tempo = tempo
        self._volume = 100
        self._duration = random.randint(5, 15)
        self._program = random.randint(0, 104)
        self.create_midi()

    def create_midi(self):
        """ Create melody and write it to file named self._name"""
        my_midi = MIDIFile(1)
        # adding random program (number from 0 to 127)
        my_midi.addProgramChange(0, 0, 0, self._program)
        # adding tempo to track
        my_midi.addTempo(0, 0, self._tempo)
        # function, which creates order of keys in an array
        degrees = self.create_melody()
        i = 0

        # adding notes to midi, 1/3 possibility note is going to be 0.5 beat later.
        for i, pitch in enumerate(degrees):
            if random.randrange(0, 3) != 1 or i == 0:
                my_midi.addNote(0, 0, pitch, i, 1, self._volume)
            else:
                my_midi.addNote(0, 0, pitch, i - 0.5, 1, self._volume)
                i -= + 0.5

        # adding longer note at the end, so the track doesn't 'cut off' suddenly
        my_midi.addNote(0, 0, 1, i, 2, 0)

        with open(self._name, "wb") as output_file:
            my_midi.writeFile(output_file)

    def create_melody(self):
        """ Create and return sequence of keys for a melody using theory of chords progression."""
        # key chords charts:

        # A B C D E F G C# F# Ab Bb Db Eb Gb
        major_map = [[9, 11, 1, 2, 4, 6, 8], [11, 1, 3, 4, 6, 8, 10], [0, 2, 4, 5, 7, 9, 11], [2, 4, 6, 7, 9, 11, 1],
                     [4, 6, 8, 9, 11, 1, 3], [5, 7, 9, 10, 0, 2, 4], [7, 9, 11, 0, 2, 4, 6],  [1, 3, 5, 6, 8, 10, 12],
                     [6, 8, 10, 11, 1, 3, 5], [8, 10, 0, 1, 3, 5, 7], [10, 0, 2, 3, 5, 7, 9], [-1, 1, 3, 4, 6, 8, 10],
                     [1, 3, 5, 6, 8, 10, 0], [3, 5, 7, 8, 10, 0, 2], [6, 8, 10, -1, 1, 3, 5]]
        # A B C D E F G C# F# Ab Bb D# Eb G#
        minor_map = [[9, 11, 0, 2, 4, 5, 7], [11, 1, 2, 4, 6, 7, 9], [0, 2, 3, 5, 7, 8, 10], [2, 4, 5, 7, 9, 10, 0],
                     [4, 6, 7, 9, 11, 0, 2], [5, 7, 8, 10, 0, 1, 3], [7, 9, 10, 0, 2, 3, 5], [1, 3, 4, 6, 8, 9, 11],
                     [6, 8, 9, 11, 1, 2, 4], [8, 10, -1, 1, 3, 4, 6], [10, 0, 2, 3, 5, 7, 8], [-1, 1, 3, 4, 6, 8, 10],
                     [3, 3, 6, 8, 10, 11, 1], [3, 5, 6, 8, 10, -1, 1], [8, 10, 11, 1, 3, 4, 6]]

        # circle of fifths: changing from the corresponding indexes from major to minor sounds good
        major_circle = [2, 6, 3, 0, 4, 1, 8, 12, 9, 13, 10, 5]
        minor_circle = [0, 4, 1, 8, 7, 14, 12, 10, 5, 2, 6, 3]

        # the order of keys from key chords charts
        # e.g for sad in A major: major_map[0][0], major_map[0][3], major_map[0][4], major_map[0][4]
        sad_mood = [[0, 3, 4, 4], [0, 5, 3, 4], [0, 4, 5, 3], [0, 0, 3, 5], [0, 5, 1, 4], [0, 5, 2, 3]]
        energetic_mood = [[0, 2, 3, 5], [0, 3, 4], [3, 4, 3], [0, 3, 0, 4], [3, 4, 3],  [0, 2, 5, 3], [0, 1, 2, 3, 4]]
        creepy_mood = [[0, 5, 3, 5], [3, 2, 3], [5, 4, 6]]

        # drawing octave
        octave = random.randint(4, 7)

        # key to start, corresponding to the index from the maps (minor_map, major_map,
        # e.g. if key = 1 and we're in minor we start from [11, 1, 2, 4, 6, 7, 9] -> chart for B
        key = random.randint(0, 14)
        # for sequence of keys
        degrees = []

        # drawing sequence scheme
        if self._mood == 'creepy':
            mood_map = creepy_mood[random.randrange(len(creepy_mood))]
            scale = 'minor'
        elif self._mood == 'energetic':
            mood_map = energetic_mood[random.randrange(len(energetic_mood))]
            scale = 'major'
        else:
            mood_map = sad_mood[random.randrange(len(sad_mood))]
            scale = 'minor'

        for time in range(self._duration + 1):
            for i, note in enumerate(mood_map):
                if scale == 'minor':
                    degrees.append(minor_map[key][note] + 12 * octave)
                    time += 1
                else:
                    degrees.append(major_map[key][note] + 12 * octave)
                    time += 1

            # shift according to circle of fifths
            if scale == 'minor':
                if minor_circle.__contains__(key):
                        key = major_circle[minor_circle.index(key)]
                else:
                    key = (key + 1) % 12
                scale = 'major'
            else:
                if major_circle.__contains__(key):
                    key = minor_circle[major_circle.index(key)]
                else:
                    key = (key + 1) % 12
                scale = 'minor'

        return degrees


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Welcome to narcotic melodies generator,"
                    " simple program generating music based on chords progression.")
    parser.add_argument('-n', '--name', type=str, required=True, help="Output file name or path if to "
                                                                      "save file in another location.")
    parser.add_argument('-m', '--mood', type=str, required=False, help="Mood for music: sad/energetic/creepy",
                        default='sad')
    parser.add_argument('-t', '--tempo', type=int, required=False, help="Tempo of created melody in beats per minute "
                                                                        "(best when between 90 and 300)",
                        default=90)
    args = vars(parser.parse_args())

    melody = Melody(args['name'], args['mood'], args['tempo'])
