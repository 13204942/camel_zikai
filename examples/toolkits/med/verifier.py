import json
import re
import argparse

def extract_boxed_number(content):
    """
    从content字段中提取\boxed{}包含的数字
    """
    if not content:
        return None
    
    # 匹配\boxed{数字}的正则表达式
    pattern = r'\\boxed\{([^}]*)\}'
    match = re.search(pattern, content)
    
    if match:
        boxed_content = match.group(1)
        # 进一步处理，有可能数字前后有空格或其他符号
        boxed_content = boxed_content.strip()
        return boxed_content
    
    return None

def verify_json_file(input_file, output_file):
    """
    验证JSON文件中的数据，比较boxed数字和final_answer，只保留匹配的数据
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        verified_data = []
        skipped_count = 0
        
        for item in data:
            content = item.get('content', '')
            final_answer = item.get('final_answer', '')
            
            boxed_number = extract_boxed_number(content)
            
            # 如果没有找到boxed数字或final_answer，跳过
            if not boxed_number or not final_answer:
                skipped_count += 1
                continue
            
            # 处理可能的浮点数比较
            # 尝试转换为浮点数进行比较
            try:
                boxed_number_float = float(boxed_number)
                final_answer_float = float(final_answer)
                
                # 允许小的浮点数误差
                if abs(boxed_number_float - final_answer_float) < 1e-6:
                    verified_data.append(item)
                else:
                    skipped_count += 1
            except ValueError:
                # 不是数字，直接比较字符串
                if boxed_number == final_answer:
                    verified_data.append(item)
                else:
                    skipped_count += 1
        
        # 将验证通过的数据写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(verified_data, f, ensure_ascii=False, indent=4)
        
        print(f"验证完成！")
        print(f"保留的数据项: {len(verified_data)}")
        print(f"跳过的数据项: {skipped_count}")
        print(f"结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"处理文件时出错: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='验证JSON文件中boxed数字和final_answer是否匹配')
    parser.add_argument('input_file', help='输入JSON文件路径')
    parser.add_argument('output_file', help='输出JSON文件路径')
    
    args = parser.parse_args()
    
    verify_json_file(args.input_file, args.output_file)
