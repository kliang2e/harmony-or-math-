from music21 import converter, note, chord
from collections import defaultdict
import math

# Load the score (adjust path to your file)
score = converter.parse('mozart requiem k.626.midi')  # Replace with your file's path

# Extract all notes and chords from the score as strings (root notes if chords)
elements = []
total_notes = 0

for element in score.recurse().notes:
    if isinstance(element, chord.Chord):
        elements.append(element.root().name)  # Use root note for transitions
        total_notes += len(element.pitches)  # Add all notes in the chord to total count
    elif isinstance(element, note.Note):
        elements.append(element.name)
        total_notes += 1  # Single notes contribute one to total count

# Function to calculate entropy for a given order
def calculate_entropy(order, sequence):
    # Create a dictionary to count occurrences of sequences and their continuations
    counts = defaultdict(int)
    total_context_counts = defaultdict(int)

    # Slide through the sequence to count occurrences
    for i in range(len(sequence) - order):
        context = tuple(sequence[i:i + order])  # Previous notes as context
        next_note = sequence[i + order]  # Next note to be predicted
        counts[(context, next_note)] += 1
        total_context_counts[context] += 1

    # Compute entropy for this order
    entropy = 0
    for (context, next_note), count in counts.items():
        p = count / total_context_counts[context]  # Probability of next_note given context
        entropy -= p * math.log2(p)
    return entropy

# Main loop to calculate total entropy from zeroth order and stop when order entropy reaches 0
total_entropy = 0
max_order = len(elements) - 1  # Limit based on sequence length

for order in range(max_order + 1):
    entropy = calculate_entropy(order, elements)
    if entropy == 0:  # Stop if entropy contribution is 0
        break
    total_entropy += entropy
    print(f"Order {order} entropy: {entropy:.6f}")

# Compute average entropy per note
average_entropy = total_entropy / total_notes
print(f"Total entropy (all orders): {total_entropy:.6f}")
print(f"Average entropy per note: {average_entropy:.6f}")