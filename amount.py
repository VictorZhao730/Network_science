import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# 定义文件夹路径
input_folder = r"garantex"  # 替换为你的文件夹路径

# 定义存储每日交易总额的列表
daily_transactions = []

# 遍历文件夹中的所有 GraphML 文件
for file_name in os.listdir(input_folder):
    # 检查文件是否为 .graphml 格式
    if file_name.endswith(".graphml"):
        file_path = os.path.join(input_folder, file_name)
        
        # 从文件名中提取日期
        try:
            date_str = file_name.split("_")[-1].split(".")[0]  # 提取日期部分
            timestamp = pd.to_datetime(date_str)  # 转换为 pandas 的 datetime 格式
        except Exception as e:
            print(f"无法从文件名 {file_name} 提取日期: {e}")
            continue  # 跳过无法解析日期的文件
        
        # 读取 GraphML 文件
        try:
            G = nx.read_graphml(file_path)
        except Exception as e:
            print(f"无法读取文件 {file_path}: {e}")
            continue  # 跳过无法读取的文件
        
                # 累加当天所有边的交易金额
        daily_total = 0
        for u, v, data in G.edges(data=True):
            # 打印边的属性以调试
            # print(f"边: {u} -> {v}, 属性: {data}")
            
            try:
                # 提取交易金额字段 'weight'
                amount = float(data.get("weight", 0))  # 从字典中获取 'weight' 的值
                daily_total += amount  # 累加交易金额
            except Exception as e:
                print(f"无法处理边 {u} -> {v} 的数据 {data}: {e}")
                continue  # 跳过无法处理的边
                
        # 将当天的交易总额添加到列表
        daily_transactions.append({"timestamp": timestamp, "total_amount": daily_total})

# 检查是否有交易记录
if len(daily_transactions) == 0:
    print("未提取到任何交易记录，请检查文件夹路径或文件内容。")
else:
    # 将每日交易记录转换为 Pandas DataFrame
    df = pd.DataFrame(daily_transactions)

    # 打印前几行数据
    print("每日交易总额预览：")
    print(df.head())

    # 按天聚合交易金额（如果有重复日期）
    df_daily = df.groupby("timestamp").sum()

    # 打印前几天的聚合结果
    print("按天聚合的交易金额：")
    print(df_daily.head())

    # 绘制交易金额随时间的变化
    plt.figure(figsize=(12, 6))
    plt.plot(df_daily.index, df_daily["total_amount"], marker="o", linestyle="-", color="b")
    plt.title("Transaction Amount Over Time (Daily)", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Total Transaction Amount", fontsize=12)
    plt.grid(True)
    plt.show()
