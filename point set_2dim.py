from music21 import converter, note, chord
import datetime

# Convert pitch to piano key number (A0=1, C8=88)
def pitch_to_piano_key(p):
    midi = p.midi
    return midi - 20  # A0 is MIDI 21 → piano key 1

# Load the score
score = converter.parse('mozart requiem k.626.midi')  # Replace with your file path

# Extract all individual pitches (expanding chords)
pitches = []

for element in score.recurse().notes:
    if isinstance(element, chord.Chord):
        pitches.extend([pitch_to_piano_key(p) for p in element.pitches])
    elif isinstance(element, note.Note):
        pitches.append(pitch_to_piano_key(element.pitch))

# Record 3-note transitions
triplets = []
for i in range(len(pitches) - 2):
    triplet = (pitches[i], pitches[i + 1], pitches[i + 2])
    triplets.append(triplet)

# Generate output file with timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"note_transitions_2.txt"

# Write to file
with open(output_file, "w") as f:
    for triplet in triplets:
        f.write(f"{triplet}\n")

print(f"Saved {len(triplets)} 3-note transitions to {output_file}")




