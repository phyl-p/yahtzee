import pandas as pd # for data analysis
import matplotlib.pyplot as plt # for simulation analysis visualization
import random # for dice rolling simulation

# aggressive strategy focuses on maximizing the score
def aggressive_strategy(dice):
    counts = [dice.count(i) for i in range(1, 7)]
    max_count = max(counts)
    chosen_number = counts.index(max_count) + 1
    indices_to_reroll = [i for i, x in enumerate(dice) if x != chosen_number]

    # Focus on Yahtzee or largest available multiple
    if max_count == 5:
        return 'yahtzee', []
    elif max_count >= 3:
        if max_count == 4:
            return 'four_of_a_kind', indices_to_reroll
        else:
            return 'three_of_a_kind', indices_to_reroll
    else:
        # Check for potential straights
        sorted_dice = sorted(dice)
        if all(x in sorted_dice for x in [2, 3, 4, 5]):  # Check for middle straight
            return 'large_straight', [i for i, x in enumerate(dice) if x not in [2, 3, 4, 5]]
        elif all(x in sorted_dice for x in [1, 2, 3, 4, 5]):
            return 'large_straight', []
        elif all(x in sorted_dice for x in [2, 3, 4, 5, 6]):
            return 'large_straight', []
        else:
            # Default to rerolling all except the highest number for a possible better combination
            return 'chance', indices_to_reroll
        
# conservative strategy focuses on minimizing the risk while getting points
def conservative_strategy(dice):
    counts = [dice.count(i) for i in range(1, 7)]
    preferred_score = max(counts) * (counts.index(max(counts)) + 1)
    # Aim for the highest count number
    chosen_number = counts.index(max(counts)) + 1
    indices_to_reroll = [i for i, x in enumerate(dice) if x != chosen_number]

    # Choose the safest category based on the highest count
    if counts[chosen_number - 1] >= 3:
        if counts[chosen_number - 1] == 3:
            return 'three_of_a_kind', indices_to_reroll
        elif counts[chosen_number - 1] == 4:
            return 'four_of_a_kind', indices_to_reroll
        else:
            return 'yahtzee', []
    else:
        return ['ones', 'twos', 'threes', 'fours', 'fives', 'sixes'][chosen_number - 1], indices_to_reroll

def random_strategy(dice, roll_number):
    categories = [
        "chance", "yahtzee", "ones", "twos", "threes", "fours",
        "fives", "sixes", "three_of_a_kind", "four_of_a_kind",
        "full_house", "small_straight", "large_straight"
    ]
    category = random.choice(categories)
    if roll_number < 3:
        indices_to_reroll = random.sample(range(5), random.randint(0, 5))  # More likely to reroll more dice
    else:
        indices_to_reroll = random.sample(range(5), random.randint(0, 2))  # Fewer rerolls on the last roll
    return category, indices_to_reroll

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