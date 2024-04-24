import pandas as pd # for data analysis
import matplotlib.pyplot as plt # for simulation analysis visualization
import random # for dice rolling simulation

# aggressive and conservative strategy takes into account the current dice and the current roll number

def aggressive_strategy(dice, roll_number):
    counts = [dice.count(i) for i in range(1, 7)]
    max_count = max(counts)
    chosen_number = counts.index(max_count) + 1
    indices_to_reroll = [i for i, x in enumerate(dice) if x != chosen_number]

    # Attempt to get Yahtzee or highest multiples
    if max_count == 5:
        return 'yahtzee', [], False  # Stop rolling, score Yahtzee
    elif roll_number < 3:
        if max_count == 4:
            return 'four_of_a_kind', indices_to_reroll, True  # Continue rolling for Yahtzee
        elif max_count == 3:
            return 'three_of_a_kind', indices_to_reroll, True  # Continue rolling for Four of a kind or Yahtzee
        else:
            return 'chance', indices_to_reroll, True  # Continue rolling
    else:
        # Last roll, choose the best available category
        return 'chance', [], False  # Stop rolling

def conservative_strategy(dice, roll_number):
    counts = [dice.count(i) for i in range(1, 7)]
    max_count = max(counts)
    chosen_number = counts.index(max(counts)) + 1
    indices_to_reroll = [i for i, x in enumerate(dice) if x != chosen_number]

    # Choose based on the safest outcome
    if max_count >= 3 and roll_number < 3:
        # If there's a high count, consider scoring immediately
        if max_count == 3:
            return 'three_of_a_kind', [], False  # Choose to score immediately if moderate
        elif max_count == 4:
            return 'four_of_a_kind', [], False
        else:
            return 'yahtzee', [], False
    elif roll_number == 3:
        # Last roll, must choose a category to score
        return 'chance', [], False  # No reroll, score in the best possible category
    else:
        return 'chance', indices_to_reroll, True  # Continue rolling

# simulates a novel player that randomly chooses a category and rerolls a random number of dice
def random_strategy(dice, roll_number):
    categories = [
        "chance", "yahtzee", "ones", "twos", "threes", "fours", 
        "fives", "sixes", "three_of_a_kind", "four_of_a_kind", 
        "full_house", "small_straight", "large_straight"
    ]
    category = random.choice(categories)
    continue_rolling = random.choice([True, False]) if roll_number < 3 else False
    indices_to_reroll = random.sample(range(5), random.randint(0, 5)) if continue_rolling else []

    return category, indices_to_reroll, continue_rolling

def choose_strategy(player, strategies):
    if player in strategies:
        if strategies[player] == 'aggressive':
            return aggressive_strategy
        elif strategies[player] == 'conservative':
            return conservative_strategy
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