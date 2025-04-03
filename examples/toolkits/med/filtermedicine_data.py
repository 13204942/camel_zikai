import json
import os

def filter_medicine_data(input_file, output_file):
    """
    读取医疗数据集JSON文件，移除所有条目中的'rationale'字段，
    然后将处理后的数据保存到新文件中。
    
    Args:
        input_file (str): 输入JSON文件的路径
        output_file (str): 输出JSON文件的路径
    """
    print(f"正在处理文件: {input_file}")
    
    try:
        # 读取JSON数据
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 记录原始数据条目数量
        original_count = len(data)
        print(f"原始数据条目数量: {original_count}")
        
        # 移除每个条目中的'rationale'字段
        filtered_data = []
        for item in data:
            if 'rationale' in item:
                del item['rationale']
            filtered_data.append(item)
        
        # 将处理后的数据写入新文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)
        
        print(f"处理完成！移除了{original_count}个条目中的'rationale'字段")
        print(f"已保存到: {output_file}")
        
    except Exception as e:
        print(f"处理过程中出错: {str(e)}")

if __name__ == "__main__":
    # 设置输入和输出文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, "seed_dataset.json")
    output_file = os.path.join(current_dir, "filtered_seed_dataset.json")
    
    # 执行过滤处理
    filter_medicine_data(input_file, output_file)
