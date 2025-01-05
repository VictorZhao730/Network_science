import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Define the folder path containing the GraphML files
input_folder = r"garantex"  # Replace this with your folder path

# Define a list to store daily transaction data and average clustering coefficients
daily_transactions = []
clustering_time_series = []

# Iterate through all GraphML files in the folder
for file_name in os.listdir(input_folder):
    # Check if the file is a .graphml file
    if file_name.endswith(".graphml"):
        file_path = os.path.join(input_folder, file_name)
        
        # Extract the date from the file name
        try:
            date_str = file_name.split("_")[-1].split(".")[0]  # Extract date part
            timestamp = pd.to_datetime(date_str)  # Convert to pandas datetime format
        except Exception as e:
            print(f"Could not extract date from file name {file_name}: {e}")
            continue  # Skip files with invalid date format
        
        # Read the GraphML file
        try:
            G = nx.read_graphml(file_path)
        except Exception as e:
            print(f"Failed to read file {file_path}: {e}")
            continue  # Skip files that cannot be read
        
        # --- Calculate Clustering Coefficient ---
        clustering_coeffs = nx.clustering(G)  # Compute clustering coefficients for all nodes
        clustering_values = list(clustering_coeffs.values())  # Extract the coefficients as a list
        
        # Calculate the average clustering coefficient for the graph
        if len(clustering_values) > 0:
            avg_clustering = sum(clustering_values) / len(clustering_values)
        else:
            avg_clustering = 0  # If no nodes, set average clustering to 0
        
        # Append the average clustering coefficient to the time series
        clustering_time_series.append({
            "timestamp": timestamp,
            "avg_clustering": avg_clustering
        })
        
        # --- Process Transaction Data (Optional) ---
        # Initialize total amounts and unique edges for incoming and outgoing transactions
        total_in = 0
        total_out = 0
        
        unique_in_edges = set()  # To track unique incoming edges
        unique_out_edges = set()  # To track unique outgoing edges
        
        # Iterate through edges to classify incoming and outgoing transactions
        for u, v, data in G.edges(data=True):
            try:
                # Extract the transaction amount from the 'weight' attribute
                amount = float(data.get("weight", 0))  # Default to 0 if 'weight' is missing
                
                # Determine transaction direction
                if "garantex" in v.lower():  # If the target node is Garantex, it's an incoming transaction
                    if (u, v) not in unique_in_edges:  # Check if this edge is unique
                        unique_in_edges.add((u, v))  # Add to the set of unique incoming edges
                        total_in += amount  # Add the transaction amount
                elif "garantex" in u.lower():  # If the source node is Garantex, it's an outgoing transaction
                    if (u, v) not in unique_out_edges:  # Check if this edge is unique
                        unique_out_edges.add((u, v))  # Add to the set of unique outgoing edges
                        total_out += amount  # Add the transaction amount
            except Exception as e:
                print(f"Could not process edge {u} -> {v} with data {data}: {e}")
                continue  # Skip edges with invalid data
        
        # Calculate the average transaction amounts
        num_in_edges = len(unique_in_edges)  # Count unique incoming edges
        num_out_edges = len(unique_out_edges)  # Count unique outgoing edges
        
        average_in = total_in / num_in_edges if num_in_edges > 0 else 0
        average_out = total_out / num_out_edges if num_out_edges > 0 else 0
        
        # Append the daily data to the list
        daily_transactions.append({
            "timestamp": timestamp,
            "average_in": average_in,
            "average_out": average_out,
            "total_in": total_in,
            "total_out": total_out
        })

# Check if any clustering coefficients were extracted
if len(clustering_time_series) == 0:
    print("No clustering coefficient data found. Please check the folder path or file contents.")
else:
    # Convert the clustering time series to a Pandas DataFrame
    df_clustering = pd.DataFrame(clustering_time_series).sort_values(by="timestamp")

    # Print the first few rows of the clustering time series data
    print("Preview of clustering coefficient time series:")
    print(df_clustering.head())

    # Plot the average clustering coefficient over time
    plt.figure(figsize=(12, 6))
    plt.plot(df_clustering["timestamp"], df_clustering["avg_clustering"], marker="o", linestyle="-", color="b", label="Average Clustering Coefficient")
    plt.title("Average Clustering Coefficient Over Time", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Average Clustering Coefficient", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()
