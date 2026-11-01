from music21 import converter, note, chord, pitch
import os

# Function to convert pitch to piano key number (A0 = 1, C8 = 88)
def pitch_to_key_number(p):
    return p.midi - 20  # MIDI 21 (A0) → key 1

# Load the score (adjust the path to your file)
score = converter.parse('mozart requiem k.626.midi')  # Replace with your MIDI file path

# Extract all pitches (including from chords)
all_keys = []

for element in score.recurse().notes:
    if isinstance(element, chord.Chord):
        for p in element.pitches:
            key_num = pitch_to_key_number(p)
            if 1 <= key_num <= 88:
                all_keys.append(key_num)
    elif isinstance(element, note.Note):
        key_num = pitch_to_key_number(element.pitch)
        if 1 <= key_num <= 88:
            all_keys.append(key_num)

# Generate transitions: (note1, note2)
transitions = []
for i in range(len(all_keys) - 1):
    transitions.append((all_keys[i], all_keys[i + 1]))

# Write transitions to a file
output_file = "note_transitions_1.txt"
with open(output_file, "w") as f:
    for a, b in transitions:
        f.write(f"({a},{b})\n")

print(f"Saved {len(transitions)} transitions to '{os.path.abspath(output_file)}'")



