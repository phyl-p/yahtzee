import random # for dice rolling simulation
import pandas as pd # for data analysis
import matplotlib.pyplot as plt # for simulation analysis visualization
import simulation # for simulation analysis
import analysis # for data analysis

# returns a list of num_dice random integers between 1 and 6
def roll_dice(num_dice):
    return [random.randint(1, 6) for _ in range(num_dice)]

# from the dice and category, calculate the score
# category: chance, yahtzee, ones, twos, threes, fours, fives, sixes, three_of_a_kind, four_of_a_kind, full_house, small_straight, large_straight
# dice: list of 5 integers representing the dice values rolled from each round
# counts stores the frequency of each die value， is a list of 6 integers
def calculate_score(category, dice):
    # Count the frequency of each die value
    counts = [dice.count(i) for i in range(1, 7)]
    
    # Calculate the score based on the category
    # LOWER SECTION
    if category == "chance": # Score the total of any 5 dice in this box. 
        return sum(dice)
    elif category == "yahtzee":
        if 5 in counts:
            return 50
        return 0
    # UPPER SECTION
    elif category == "ones":
        return counts[0] * 1
    elif category == "twos":
        return counts[1] * 2
    elif category == "threes":
        return counts[2] * 3
    elif category == "fours":
        return counts[3] * 4
    elif category == "fives":
        return counts[4] * 5
    elif category == "sixes":
        return counts[5] * 6
    # LOWER SECTION
    elif category == "three_of_a_kind":
        for count in counts:
            if count >= 3:
                return sum(dice)
        return 0
    elif category == "four_of_a_kind":
        for count in counts:
            if count >= 4:
                return sum(dice)
        return 0
    elif category == "full_house":
        if 2 in counts and 3 in counts:
            return 25
        return 0
    elif category == "small_straight":
        # Stripes of four sequential dice (1-2-3-4, 2-3-4-5, 3-4-5-6)
        straights = [[1,2,3,4], [2,3,4,5], [3,4,5,6]]
        for straight in straights:
            if all(i in dice for i in straight):
                return 30
        return 0
    elif category == "large_straight":
        # Stripes of five sequential dice (1-2-3-4-5, 2-3-4-5-6)
        straights = [[1,2,3,4,5], [2,3,4,5,6]]
        for straight in straights:
            if all(i in dice for i in straight):
                return 40
        return 0
    else:
        return 0

# Get the category input from the user
def get_category_input():
    categories = [
        "chance", "yahtzee", "ones", "twos", "threes", "fours", 
        "fives", "sixes", "three_of_a_kind", "four_of_a_kind", 
        "full_house", "small_straight", "large_straight"
    ] #
    print("Available categories: " + ", ".join(categories)) # display the available categories
    category = input("Enter the category to score this roll: ").strip().lower() # get the category input from the user
    while category not in categories:
        print("Invalid category. Try again.")
        category = input("Enter the category to score this roll: ").strip().lower()
    return category

# Main function to play the game
def main():
    results = []  # List to store game data for analysis

    player_scores = {} # dictionary to store the scores for each player
    game_mode = int(input("Choose Game Mode: Simulation 1, Player 2): "))
    #check if the game mode is valid    
    while game_mode not in [1, 2]:
        print("Invalid game mode. Try again.")
        game_mode = int(input("Choose Game Mode: Simulation 1, Player 2): "))
        
    num_players = int(input("Enter number of players: ")) # allow multiple players

    if game_mode == 1:
        # assign a strategy to each player
        strategies = {}
        for player in range(1, num_players + 1):
            strategy = input(f"Enter strategy for player {player} (random, conservative, or aggressive): ").strip().lower()
            strategies[player] = strategy

    for i in range(1, num_players + 1): # initialize scores for each player
        player_scores[i] = {} # a dictionary within the player_scores dictionary

    num_rounds = 13  # Each player must fill all 13 categories
    for round_num in range(num_rounds): # each round
        print(f"\n~~~~~Round {round_num + 1}~~~~~")
        for player in range(1, num_players + 1): # each player takes a turn
            print(f"Player {player}'s turn:")
            dice = roll_dice(5) # roll 5 dice
            print("First roll: ", dice)
            # Allow the player to reroll the dice twice

            # Simulation Mode
            if game_mode == 1:
                strategy_func = simulation.choose_strategy(player, strategies) # choose the strategy function based on the player's strategy
                for roll in range(3):
                    category, reroll_indices = strategy_func(dice, roll + 1)
                    if reroll_indices:
                        new_dice = roll_dice(len(reroll_indices))
                        for index, new_die in zip(reroll_indices, new_dice):
                            dice[index] = new_die
                    if roll == 2 or not reroll_indices:  # No rerolls or last roll
                        break
            else:
                # Player Mode
                for roll in range(2):
                    reroll = input("Enter indices (1-5) of dice to reroll (comma separated, empty if none): ")
                    if reroll.strip():
                        indices = list(map(int, reroll.split(',')))
                        #check if the indices are valid
                        while any(i < 1 or i > 5 for i in indices):
                            print("Invalid index. Try again.")
                            reroll = input("Enter indices (1-6) of dice to reroll (comma separated, empty if none): ")
                            if reroll.strip():
                                indices = list(map(int, reroll.split(',')))
                            continue
                        new_dice = roll_dice(len(indices))
                        for index, new_die in zip(indices, new_dice):
                            dice[index-1] = new_die
                    print(f"Roll {roll + 2}: ", dice)
                
                # Ask the player to choose a category and calculate the score
                category = get_category_input()
            score = calculate_score(category, dice)
            player_scores[player][category] = score
           
           # Store each roll and its outcome in a dictionary
            results.append({
                'player': player,
                'round': round_num,
                'dice': dice.copy(),
                'chosen_category': category,
                'score': score
            })

           # Display the score for the current category and the current total scores
            print(f"Score for {category}: {score}")
            print(f"Current scores for player {player}:", player_scores[player])

    # Convert results to DataFrame for easier analysis
    results_df = pd.DataFrame(results)

    # After the game loop, output results and perform analysis
    analysis.analyze_and_visualize(results_df)

    # After all rounds are complete, display final scores and determine the winner
    print("\nFinal Scores:")
    max_score = 0
    winner = None
    for player, scores in player_scores.items():
        total_score = sum(scores.values())
        # give bonus points for a total score of 63 or more in the upper section
        if sum(scores.get(category, 0) for category in ["ones", "twos", "threes", "fours", "fives", "sixes"]) >= 63:
            total_score += 35
        print(f"Player {player}: {total_score}")
        if total_score > max_score:
            max_score = total_score
            winner = player

    # Announce the winner
    print(f"\n Player {winner} wins the game with a score of {max_score}! Congrats!")

if __name__ == "__main__":
    main()