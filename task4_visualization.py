import pandas as pd
import matplotlib.pyplot as plt
import os

def create_visualizations():
    # --- 1. Setup  ---
    path = "data/trends_analysed.csv"
    if not os.path.exists(path):
        print("Error: trends_analysed.csv not found!")
        return
    
    df = pd.read_csv(path)
    
    # Create the outputs folder if it is missing
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        print("Created 'outputs/' folder.")

    # Setting a clean style for all charts
    plt.style.use('ggplot')

    # --- 2. Chart 1: Top 10 Stories by Score (6 marks) ---
    # Sort and grab the top 10
    top_10 = df.sort_values(by='score', ascending=False).head(10)
    
    # Shorten titles longer than 50 chars so they don't mess up the layout
    titles = [t[:47] + "..." if len(t) > 50 else t for t in top_10['title']]
    
    plt.figure(figsize=(10, 6))
    plt.barh(titles, top_10['score'], color='skyblue')
    plt.gca().invert_yaxis() # Highest score at the top
    plt.title("Top 10 Most Upvoted Stories")
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.tight_layout()
    plt.savefig("outputs/chart1_top_stories.png")
    plt.close() # Close to free up memory

    # --- 3. Chart 2: Stories per Category  ---
    plt.figure(figsize=(8, 6))
    counts = df['category'].value_counts()
    # Use a list of colors to satisfy the "different color for each bar" rule
    colors = ['tomato', 'cornflowerblue', 'gold', 'mediumseagreen', 'orchid']
    
    counts.plot(kind='bar', color=colors[:len(counts)])
    plt.title("Stories per Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/chart2_categories.png")
    plt.close()

    # --- 4. Chart 3: Score vs Comments  ---
    plt.figure(figsize=(8, 6))
    
    # Separate the data to color them differently
    popular = df[df['is_popular'] == True]
    normal = df[df['is_popular'] == False]
    
    plt.scatter(normal['score'], normal['num_comments'], alpha=0.6, label='Normal', color='gray')
    plt.scatter(popular['score'], popular['num_comments'], alpha=0.8, label='Popular', color='orange')
    
    plt.title("Score vs. Number of Comments")
    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig("outputs/chart3_scatter.png")
    plt.close()

    # --- Bonus: Dashboard  ---
    # Combining all three into a 2x2 grid (leaving one corner empty or stretching)
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle("TrendPulse Dashboard", fontsize=20, fontweight='bold')

    # Re-plot 1: Top Stories
    axes[0, 0].barh(titles, top_10['score'], color='skyblue')
    axes[0, 0].invert_yaxis()
    axes[0, 0].set_title("Top 10 Stories")

    # Re-plot 2: Categories
    counts.plot(kind='bar', color=colors[:len(counts)], ax=axes[0, 1])
    axes[0, 1].set_title("Category Breakdown")
    axes[0, 1].tick_params(axis='x', rotation=45)

    # Re-plot 3: Scatter (spanning the bottom row)
    # Removing the empty 4th subplot to make it look cleaner
    fig.delaxes(axes[1, 1])
    ax_bottom = plt.subplot(2, 1, 2) # Use the bottom space for a wide scatter
    ax_bottom.scatter(normal['score'], normal['num_comments'], color='gray', label='Normal')
    ax_bottom.scatter(popular['score'], popular['num_comments'], color='orange', label='Popular')
    ax_bottom.set_title("Engagement Analysis (Score vs Comments)")
    ax_bottom.legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("outputs/dashboard.png")
    print("All charts and dashboard saved to 'outputs/' folder!")

if __name__ == "__main__":
    create_visualizations()
