import pandas as pd # for data analysis
import matplotlib.pyplot as plt # for simulation analysis visualization

def aggressive_strategy(dice):
    # Example implementation: focuses on Yahtzee or large straight
    counts = [dice.count(i) for i in range(1, 7)]
    if 5 in counts:
        return 'yahtzee'
    elif all(i in dice for i in [1, 2, 3, 4, 5]) or all(i in dice for i in [2, 3, 4, 5, 6]):
        return 'large_straight'
    else:
        return 'chance'  # Default to chance if high-score categories are not possible

def conservative_strategy(dice):
    # Example implementation: opts for guaranteed scores like ones, twos, etc.
    counts = [dice.count(i) for i in range(1, 7)]
    for i in range(6, 0, -1):  # Check from sixes to ones
        if counts[i-1] > 0:
            return ['sixes', 'fives', 'fours', 'threes', 'twos', 'ones'][i-1]
    return 'chance'

def random_strategy(dice):
    import random
    categories = [
        "chance", "yahtzee", "ones", "twos", "threes", "fours", 
        "fives", "sixes", "three_of_a_kind", "four_of_a_kind", 
        "full_house", "small_straight", "large_straight"
    ]
    return random.choice(categories)

def choose_strategy(player, strategies):
    if player in strategies:
        return strategies[player]
    else:
        return random_strategy  # Default strategy if none specified

def analyze_combinations(df):
    from collections import Counter
    # Calculate frequency of each dice combination
    dice_combinations = df['dice'].apply(lambda dice: tuple(sorted(dice)))
    frequency_counts = Counter(dice_combinations)

    # Visualizing the frequency of combinations
    pd.DataFrame.from_dict(frequency_counts, orient='index', columns=['Frequency']).sort_values(by='Frequency', ascending=False).plot(kind='bar')
    plt.title('Frequency of Dice Combinations')
    plt.xlabel('Combinations')
    plt.ylabel('Frequency')
    plt.show()