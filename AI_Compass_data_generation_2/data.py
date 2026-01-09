import pandas as pd
import numpy as np
import random

# 2. Define Clusters and their Target Levels
clusters = {
    "1. The Traditionalist": {"count": 100, "base_lvl": 1},
    "2. The Curious Experimenter": {"count": 200, "base_lvl": 2},
    "3. The Structured Builder": {"count": 125, "base_lvl": 3},
    "4. The Value Scaler": {"count": 60, "base_lvl": 4},
    "5. The AI-Enabled Leader": {"count": 15, "base_lvl": 5}
}

# 3. Helper Data
industries = ["Manufacturing", "Retail", "Healthcare", "Logistics", "Finance", "Construction", "Hospitality"]
cities = ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt", "Stuttgart", "Düsseldorf"]
corp_suffixes = ["GmbH", "AG", "Solutions", "Logistics", "Digital", "Group", "SME"]
corp_roots = ["Nexus", "Zenith", "Quantum", "Vantage", "Alpha", "Blue Harbor", "Iron", "Skyline", "Peak"]

def generate_company_name():
    return f"{random.choice(corp_roots)} {random.choice(corp_suffixes)}"

# 4. Probabilistic Answer Selector
def get_weighted_level(base_lvl):
    levels = [1, 2, 3, 4, 5]
    # 70% chance for base level, 20% for +/- 1, 10% for others
    weights = []
    for l in levels:
        dist = abs(l - base_lvl)
        if dist == 0: weights.append(0.70)
        elif dist == 1: weights.append(0.20)
        else: weights.append(0.033)
    return np.random.choice(levels, p=[w/sum(weights) for w in weights])

def generate_data(questions_df, comp_id_pool=None):
    if comp_id_pool is None:
        comp_id_pool = list(range(1, 1501))
        random.shuffle(comp_id_pool)
    
    all_rows = []
    
    for profile, config in clusters.items():
        for _ in range(config['count']):
            base_lvl = config['base_lvl']
            c_name = generate_company_name()
            
            row = {
                "Company_ID": comp_id_pool.pop() if comp_id_pool else random.randint(1000, 9999),
                "Company_Name*": c_name,
                "Industry*": random.choice(industries),
                "Website": f"www.{c_name.lower().replace(' ', '-')}.de",
                "Employee_Count": random.choice(["1-50", "51-250", "251-500", "500+"]),
                "City": random.choice(cities),
                "Cluster_Profile": profile
            }
            
            # Fill Questions 1 to 34
            for idx, q_row in questions_df.iterrows():
                q_text = q_row['Question_Text']
                q_type = q_row['Question_Type']
                
                # Identify the Level columns (Level 1 to Level 9)
                lvl_options = [q_row[f'Level {i}'] for i in range(1, 10) if pd.notna(q_row[f'Level {i}'])]
                
                if q_type == "Checklist":
                    # For checklists, pick 1-3 random options from the available levels
                    # Higher clusters pick more options
                    num_to_pick = random.randint(1, min(3, len(lvl_options))) if base_lvl < 4 else random.randint(2, min(4, len(lvl_options)))
                    row[q_text] = ", ".join(random.sample(lvl_options, num_to_pick))
                
                elif idx < 28: # Weighted Assessment Questions (1-28)
                    selected_lvl = get_weighted_level(base_lvl)
                    # Ensure we don't index out of bounds if question has fewer than 5 levels
                    idx_to_use = min(selected_lvl, len(lvl_options)) - 1
                    row[q_text] = lvl_options[idx_to_use]
                    
                else: # Information Questions (29-34) - No Weighting
                    row[q_text] = random.choice(lvl_options)
    
            all_rows.append(row)
            
    return pd.DataFrame(all_rows)

if __name__ == "__main__":
    # 1. Load the files
    questions_df = pd.read_csv('Questions.csv', sep=';', skiprows=1)
    output_template = pd.read_csv('Questionnaire_Output.csv', sep=';', skiprows=1)
    output_template = output_template.loc[:, ~output_template.columns.str.contains('^Unnamed')]

    print("Generating dataset...")
    df_final = generate_data(questions_df)
    
    # Reorder columns to match output template
    # Only keep columns that are in df_final (some info questions might not be in template or vice versa)
    common_cols = [c for c in output_template.columns if c in df_final.columns]
    df_final = df_final[common_cols]
    
    df_final.to_csv('assessment_data.csv', index=False)
    print("Dataset generated successfully: 500 rows across 5 clusters.")