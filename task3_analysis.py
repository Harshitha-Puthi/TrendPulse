import pandas as pd
import numpy as np
import os

def run_trend_analysis():
    # --- 1. Load and Explore  ---
    file_path = "/content/data/trends_clean.csv"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Please run Task 2 first.")
        return

    df = pd.read_json(file_path) if file_path.endswith('.json') else pd.read_csv(file_path)
    
    print(f"Loaded data: {df.shape}")
    print("\nFirst 5 rows:")
    print(df.head())
    
    # Calculate simple averages using pandas
    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    
    print(f"\nAverage score   : {avg_score:.2f}")
    print(f"Average comments: {avg_comments:.2f}")

    # --- 2. Basic Analysis with NumPy  ---
    print("\n--- NumPy Stats ---")
    
    # Converting columns to numpy arrays for the math parts
    scores = df['score'].values
    comments = df['num_comments'].values
    
    print(f"Mean score   : {np.mean(scores):.2f}")
    print(f"Median score : {np.median(scores):.2f}")
    print(f"Std deviation: {np.std(scores):.2f}")
    print(f"Max score    : {np.max(scores)}")
    print(f"Min score    : {np.min(scores)}")
    
    # Finding the category with the most stories
    # value_counts is pandas, but we can display the top one easily
    top_cat = df['category'].value_counts().idxmax()
    cat_count = df['category'].value_counts().max()
    print(f"Most stories in: {top_cat} ({cat_count} stories)")
    
    # Finding the story with the most comments using numpy's argmax
    max_comm_index = np.argmax(comments)
    top_story_title = df.iloc[max_comm_index]['title']
    top_story_count = df.iloc[max_comm_index]['num_comments']
    print(f"Most commented story: \"{top_story_title}\" — {top_story_count} comments")

    # --- 3. Add New Columns ---
    # Engagement formula: comments / (score + 1)
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # is_popular: True if score is above the average
    df['is_popular'] = df['score'] > avg_score

    # --- 4. Save the Result  ---
    output_file = "data/trends_analysed.csv"
    df.to_csv(output_file, index=False)
    
    print(f"\nSaved to {output_file}")

if __name__ == "__main__":
    run_trend_analysis()
