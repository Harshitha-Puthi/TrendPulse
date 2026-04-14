# Note: Row counts differ from example because data is fetched live on April 14, 2026.
import pandas as pd
import os
import glob

def clean_data():
    # Find any trends json file in the current or data folder
    # This keeps it from breaking if the file name changes
    json_list = glob.glob("trends_*.json") + glob.glob("data/trends_*.json")
    
    if not json_list:
        print("Error: trends json file not found.")
        return
    
    # Load up the first match
    target = json_list[0]
    df = pd.read_json(target)
    print(f"Loaded {len(df)} stories from {target}")

    # Start the cleanup
    # Drop duplicates by id
    df = df.drop_duplicates(subset='post_id')
    print(f"After removing duplicates: {len(df)}")
    
    # Clear out rows with empty critical fields
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")
    
    # Make sure numbers are actually integers
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].astype(int)
    
    # Only keep the good stuff (score >= 5)
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")
    
    # Clean up whitespace in titles
    df['title'] = df['title'].str.strip()

    # Save output - make folder if it's missing
    if not os.path.exists("data"):
        os.makedirs("data")
        
    out = "data/trends_clean.csv"
    df.to_csv(out, index=False)
    
    print(f"Saved {len(df)} rows to {out}")
    
    # Category summary
    print("\nStories per category:")
    print(df['category'].value_counts())

if __name__ == "__main__":
    clean_data()
