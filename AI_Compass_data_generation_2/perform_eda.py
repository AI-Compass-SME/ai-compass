
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda(input_file='assessment_data.csv', output_dir='eda_outputs'):
    # Set style
    sns.set_theme(style="whitegrid")
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        df = pd.read_csv(input_file)
        print("Dataset loaded successfully.")
        print(f"Shape: {df.shape}")
        print("Columns:", df.columns.tolist())
        
        # 1. Univariate Analysis
        
        # Cluster Profile Distribution
        plt.figure(figsize=(10, 6))
        cluster_counts = df['Cluster_Profile'].value_counts()
        sns.barplot(x=cluster_counts.values, y=cluster_counts.index, palette='viridis')
        plt.title('Distribution of Cluster Profiles')
        plt.xlabel('Count')
        plt.ylabel('Cluster Profile')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/cluster_distribution.png")
        print(f"Saved cluster_distribution.png. Counts:\n{cluster_counts}")
    
        # Industry Distribution
        plt.figure(figsize=(10, 6))
        industry_counts = df['Industry*'].value_counts()
        sns.barplot(x=industry_counts.values, y=industry_counts.index, palette='magma')
        plt.title('Distribution by Industry')
        plt.xlabel('Count')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/industry_distribution.png")
        print(f"Saved industry_distribution.png. Counts:\n{industry_counts}")
    
        # Employee Count Distribution
        plt.figure(figsize=(8, 5))
        emp_order = ["1-50", "51-250", "251-500", "500+"]
        sns.countplot(data=df, x='Employee_Count', order=emp_order, palette='Blues_d')
        plt.title('Employee Count Distribution')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/employee_distribution.png")
        print("Saved employee_distribution.png")
    
        # 2. Specific Question Analysis (Example)
        # "How is AI prioritized in management meetings?"
        q_col = "How is AI prioritized in management meetings?"
        if q_col in df.columns:
            plt.figure(figsize=(12, 6))
            sns.countplot(data=df, y=q_col, hue='Cluster_Profile', palette='viridis')
            plt.title('Management Priority of AI by Cluster')
            plt.tight_layout()
            plt.savefig(f"{output_dir}/management_priority_by_cluster.png")
            print("Saved management_priority_by_cluster.png")
        
        print("\nEDA Script Completed Successfully.")
        return True
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    run_eda()
