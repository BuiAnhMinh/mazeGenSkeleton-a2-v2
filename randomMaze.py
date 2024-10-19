import random
# create this to randomly change the weight pattern from checkered to random
def randomize_odd_numbers(data):
    """Randomizes odd numbers in odd lines of the given data."""
    lines = data.split('\n')
    for i, line in enumerate(lines):
        if i % 2 == 1:  # Odd line (1-based, so it's odd-indexed in 0-based)
            numbers = line.split()
            for j, num in enumerate(numbers):
                if int(num) % 2 != 0:  # Odd number
                    numbers[j] = str(random.randint(0, 3))
            lines[i] = ' '.join(numbers)
    return '\n'.join(lines)


input_data = """
0 0 1 0 2 0 3 0 0 0 1 0 2 0 3 1 0 0 1
0 1 0 0 1 0 0 0 1 0
1 1 2 0 3 1 0 0 1 0 2 1 3 0 0 1 1 0 2
0 1 0 0 1 1 1 0 1 0
2 0 3 0 0 0 1 1 2 0 3 0 0 0 1 0 2 0 3
0 0 1 0 1 0 1 0 0 0
3 0 0 0 1 0 2 0 3 0 0 0 1 0 2 0 3 0 0
0 0 1 1 1 1 0 1 0 0
0 1 1 0 2 0 3 0 1 0 1 0 2 0 3 0 1 0 1
0 1 0 1 1 0 1 1 0 0
1 1 2 0 3 1 0 0 1 0 2 1 3 0 0 1 1 0 2
0 0 1 0 1 0 1 0 1 0
2 1 3 1 0 1 1 0 2 0 3 1 0 0 1 0 2 0 3 
0 1 0 1 0 1 0 0 1 0
3 0 0 0 1 0 2 0 3 0 0 0 1 0 2 0 3 0 0
0 1 1 1 1 0 1 1 1 0
0 0 1 0 2 0 3 0 0 0 1 0 2 0 3 1 0 0 1
0 1 0 0 0 1 0 0 1 1
1 0 2 1 3 0 0 1 1 0 2 0 3 1 0 0 1 0 2
"""

result = randomize_odd_numbers(input_data)
print(result)
