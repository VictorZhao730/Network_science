import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Define the folder path containing the GraphML files
input_folder = r"garantex"  # Replace this with your folder path

# Define a list to store daily transaction data
daily_transactions = []

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
        
        # Initialize total amounts and edge counts for incoming and outgoing transactions
        total_in = 0
        num_in_edges = 0
        total_out = 0
        num_out_edges = 0
        
        # Iterate through edges to classify incoming and outgoing transactions
        for u, v, data in G.edges(data=True):
            try:
                # Extract the transaction amount from the 'weight' attribute
                amount = float(data.get("weight", 0))  # Default to 0 if 'weight' is missing
                
                # Determine transaction direction
                if "garantex" in v.lower():  # If the target node is Garantex, it's an incoming transaction
                    total_in += amount
                    num_in_edges += 1
                elif "garantex" in u.lower():  # If the source node is Garantex, it's an outgoing transaction
                    total_out += amount
                    num_out_edges += 1
            except Exception as e:
                print(f"Could not process edge {u} -> {v} with data {data}: {e}")
                continue  # Skip edges with invalid data
        
        # Calculate the average transaction amounts
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

# Check if any transaction records were extracted
if len(daily_transactions) == 0:
    print("No transaction records found. Please check the folder path or file contents.")
else:
    # Convert the daily transaction list to a Pandas DataFrame
    df = pd.DataFrame(daily_transactions)

    # Print the first few rows of the data
    print("Preview of daily transaction data:")
    print(df.head())

    # Aggregate data by day (in case there are duplicate timestamps)
    df_daily = df.groupby("timestamp").mean()

    # Print the aggregated data
    print("Aggregated daily transaction data:")
    print(df_daily.head())

    # Plot the average transaction amounts for incoming and outgoing transactions
    plt.figure(figsize=(12, 6))
    plt.plot(df_daily.index, df_daily["average_in"], marker="o", linestyle="-", color="g", label="Average In (to Garantex)")
    plt.plot(df_daily.index, df_daily["average_out"], marker="o", linestyle="-", color="r", label="Average Out (from Garantex)")
    plt.title("Average Transaction Amount In and Out of Garantex Over Time", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Average Transaction Amount", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()

    # Plot the total transaction amounts for incoming and outgoing transactions
    plt.figure(figsize=(12, 6))
    plt.plot(df_daily.index, df_daily["total_in"], marker="o", linestyle="-", color="b", label="Total In (to Garantex)")
    plt.plot(df_daily.index, df_daily["total_out"], marker="o", linestyle="-", color="orange", label="Total Out (from Garantex)")
    plt.title("Total Transaction Amount In and Out of Garantex Over Time", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Total Transaction Amount", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()
