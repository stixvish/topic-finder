import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_heatmap(data):
  # Convert to DataFrame
  df = pd.DataFrame(data).T  # Transpose so years are rows and categories are columns
  df.index = df.index.astype(int)  # Convert year strings to integers for better sorting
  df = df.sort_index()  # Sort by year

  # Create the heatmap
  plt.figure(figsize=(14, 10))

  # Create heatmap with custom styling
  ax = sns.heatmap(
    df.T,  # Transpose again so categories are rows and years are columns
    annot=True,
    fmt='.0f',
    cmap='YlOrRd',
    cbar_kws={'label': 'Value'},
    linewidths=0.5,
    linecolor='white'
  )

  # Customize the plot
  plt.title('Category Values Over Time (1986-2022)', fontsize=16, fontweight='bold', pad=20)
  plt.xlabel('Year', fontsize=12, fontweight='bold')
  plt.ylabel('Categories', fontsize=12, fontweight='bold')

  # Rotate x-axis labels for better readability
  plt.xticks(rotation=45, ha='right')
  plt.yticks(rotation=0)

  # Adjust layout to prevent label cutoff
  plt.tight_layout()

  # Show the plot
  plt.show()