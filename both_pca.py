import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = "flipped_master_table.csv"  # Replace with your actual file path
data = pd.read_csv(file_path)

# Check for missing values in 'Reference' and 'Status'
data['Reference'].fillna('Missing_Reference', inplace=True)
data['Status'].fillna('Missing_Status', inplace=True)

def plot_combined_pca(data):
    # Filter the data for 'neg' and 'pos' samples
    neg_data = data[data['Status'] == 'neg']
    pos_data = data[data['Status'] == 'pos']
    
    # Combine both datasets for PCA
    combined_data = pd.concat([neg_data, pos_data])
    
    # Extract the numeric columns for PCA
    features = combined_data.columns[2:]  # Assuming the first two columns are 'Reference' and 'Status'
    x = combined_data.loc[:, features].values
    
    # Check for non-finite values and handle them
    x = np.nan_to_num(x)  # Replace NaN, inf, -inf with zero
    
    # Standardize the data
    x = StandardScaler().fit_transform(x)
    
    # Perform PCA
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(x)
    pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
    
    # Add the 'Reference' and 'Status' columns back to the PCA results
    final_df = pd.concat([combined_data[['Reference', 'Status']], pca_df], axis=1)
    
    # Visualize the results
    plt.figure(figsize=(10,8))
    
    # Plot 'neg' samples (Red)
    neg_points = final_df[final_df['Status'] == 'neg']
    plt.scatter(neg_points['PC1'], neg_points['PC2'], c='red', label='neg')
    
    # Plot 'pos' samples (Green)
    pos_points = final_df[final_df['Status'] == 'pos']
    plt.scatter(pos_points['PC1'], pos_points['PC2'], c='green', label='pos')
    
    # Label points with their 'Reference' values
    for i in range(final_df.shape[0]):
        label = final_df['Reference'][i] if pd.notna(final_df['Reference'][i]) else 'NaN'
        plt.text(final_df['PC1'][i], final_df['PC2'][i], label, fontsize=8)
    
    plt.title('PCA of Gut Microbiome Data - Combined Neg (Red) and Pos (Green) Samples')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend()
    plt.grid()
    plt.show()

# Generate the combined PCA plot
plot_combined_pca(data)
