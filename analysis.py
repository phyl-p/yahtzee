import matplotlib.pyplot as plt # for simulation analysis visualization

def analyze_and_visualize(df):
    # Calculate total scores by player
    total_scores = df.groupby('player')['score'].sum()
    print("Total Scores by Player:")
    print(total_scores)

    # Visualization of scores by category
    category_scores = df.groupby('chosen_category')['score'].mean()
    category_scores.plot(kind='bar', title='Average Score per Category')
    plt.xlabel('Category')
    plt.ylabel('Average Score')
    plt.show()