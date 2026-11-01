from music21 import converter, chord, note, stream
import numpy as np

# Define consonance scores for intervals
consonance_scores = {
    0: 1.0,  # Octave
    7: 0.9,  # Perfect fifth
    5: 0.9,  # Perfect fourth
    4: 0.8,  # Major third
    3: 0.8,  # Minor third
    9: 0.5,  # Major sixth
    8: 0.5,  # Minor sixth
    2: 0.15,  # Major second
    10: 0.15,  # Minor seventh
    6: 0.1,  # Tritone (augmented fourth / diminished fifth)
    1: 0.0,  # Minor second
    11: 0.0  # Major seventh
}


# Function to calculate consonance score for a chord
def calculate_consonance(chord_obj):
    if len(chord_obj) < 2:
        return 0  # Single notes have no interval

    pitches = np.array([p.midi for p in chord_obj.pitches])  # Convert pitches to MIDI
    intervals = np.abs(np.subtract.outer(pitches, pitches)) % 12  # Get interval matrix
    unique_intervals = intervals[np.triu_indices(len(pitches), k=1)]  # Extract unique pairs

    # Compute consonance score
    consonance_values = np.array([consonance_scores.get(i, 0) for i in unique_intervals])

    # Use harmonic mean to balance large chords
    if len(unique_intervals) > 0:
        avg_consonance = len(consonance_values) / np.sum(1 / (consonance_values + 1e-6))  # Avoid division by zero
    else:
        avg_consonance = 0

    return avg_consonance


# Load and analyze a music score
def analyze_score(file_path):
    score = converter.parse(file_path)
    total_score = 0
    chord_count = 0

    # Dictionary to group notes that start at the same time
    chords_by_offset = {}

    for part in score.parts:  # Ensure we go through all instruments/staves
        for element in part.flatten().notes:  # Use .flat to unfold from voices
            start_time = element.offset  # Use offset as time reference

            if start_time not in chords_by_offset:
                chords_by_offset[start_time] = []

            if isinstance(element, note.Note):
                chords_by_offset[start_time].append(element)
            elif isinstance(element, chord.Chord):
                chords_by_offset[start_time].extend(element.notes)

    # Analyze the consonance of chords (only simultaneous notes)
    for offset, notes in sorted(chords_by_offset.items()):
        if len(notes) > 1:
            chord_obj = chord.Chord(notes)
            consonance = calculate_consonance(chord_obj)
            total_score += consonance
            chord_count += 1
            print(f"Time {offset}: {chord_obj} → Consonance: {consonance:.3f}")  # Debugging output

    return total_score / chord_count if chord_count > 0 else 0  # Average score


# Example usage
file_path = "bach bwv1006.midi"  # Replace with actual file path
average_consonance = analyze_score(file_path)
print(f"Average consonance score for the piece: {average_consonance:.3f}")


