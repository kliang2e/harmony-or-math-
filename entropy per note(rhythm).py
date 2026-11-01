from music21 import converter, note, chord
from collections import defaultdict
import math

# Load the score (adjust path to your file)
score = converter.parse('mozart k626_merged.mid')  # Replace with your file's path

# Extract rhythmic durations from the score
rhythms = []  # Stores rhythmic values (durations)
total_notes = 0  # Counts each note or chord as one rhythmic event

for element in score.recurse().notes:
    if isinstance(element, chord.Chord):
        rhythms.append(element.quarterLength)  # Store only one duration for the whole chord
    elif isinstance(element, note.Note):
        rhythms.append(element.quarterLength)  # Store duration of the note

    total_notes += 1  # Count each note or chord as one rhythmic event

# Function to calculate entropy for a given order
def calculate_entropy(order, sequence):
    counts = defaultdict(int)
    total_context_counts = defaultdict(int)

    # Slide through the sequence to count occurrences
    for i in range(len(sequence) - order):
        context = tuple(sequence[i:i + order])  # Previous durations as context
        next_duration = sequence[i + order]  # Next rhythmic value to be predicted
        counts[(context, next_duration)] += 1
        total_context_counts[context] += 1

    # Compute entropy for this order
    entropy = 0
    for (context, next_duration), count in counts.items():
        p = count / total_context_counts[context]  # Probability of next rhythm given context
        entropy -= p * math.log2(p)
    return entropy

# Main loop to calculate total entropy
total_entropy = 0
max_order = len(rhythms) - 1  # Limit based on sequence length
additional_orders_after_zero = 3  # Number of extra orders to calculate after entropy hits 0
stop_after_zero = False  # Flag to track when we've reached additional orders

for order in range(max_order + 1):
    entropy = calculate_entropy(order, rhythms)

    if stop_after_zero:  # Reduce the counter for extra orders
        additional_orders_after_zero -= 1
        if additional_orders_after_zero < 0:  # Stop after additional orders
            break

    if entropy == 0 and not stop_after_zero:
        stop_after_zero = True  # Trigger the extra order loop

    total_entropy += entropy
    print(f"Order {order} rhythmic entropy: {entropy:.6f}")

# Compute average rhythmic entropy per note
average_rhythmic_entropy = total_entropy / total_notes
print(f"Total rhythmic entropy (all orders): {total_entropy:.6f}")
print(f"Average rhythmic entropy per note: {average_rhythmic_entropy:.6f}")