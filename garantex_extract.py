from tqdm import tqdm
import os
import networkx as nx
# 定义路径
input_folder = r"G:\UZH\24f\ns\daily_networks_graphml"  # GraphML 文件所在文件夹
output_folder = r"G:\UZH\24f\ns\garantex"  # 提取的子图保存路径
os.makedirs(output_folder, exist_ok=True)  # 如果输出文件夹不存在，则创建

# 定义 Garantex 节点 ID
garantex_node = "Garantex"

# 遍历文件夹中的所有 GraphML 文件
for file_name in tqdm(os.listdir(input_folder), desc="Processing GraphML Files"):
    if file_name.endswith(".graphml"):  # 只处理 .graphml 文件
        file_path = os.path.join(input_folder, file_name)
        
        # 读取 GraphML 文件
        G = nx.read_graphml(file_path)
        
        # 检查 Garantex 是否在图中
        if garantex_node in G.nodes:
            # 提取与 Garantex 相关的边（包括出边和入边）
            related_edges = [
                (u, v) for u, v in G.edges()
                if u == garantex_node or v == garantex_node
            ]
            
            # 提取相关的节点
            related_nodes = set()
            for u, v in related_edges:
                related_nodes.add(u)
                related_nodes.add(v)
            
            # 创建子图
            subgraph = G.subgraph(related_nodes).copy()
            
            # 保存子图
            output_path = os.path.join(output_folder, f"garantex_subgraph_{file_name}")
            nx.write_graphml(subgraph, output_path)
        else:
            print(f"Warning: {file_name} does not contain the node '{garantex_node}'.")
