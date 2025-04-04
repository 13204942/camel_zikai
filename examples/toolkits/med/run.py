
import json
import sys
from examples.toolkits.med.moudles import *

def execute_rationale_code(json_file):
    """执行JSON文件中的rationale代码并统计成功数"""
    success_count = 0
    total_count = 0
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        if "rationale" in item and isinstance(item["rationale"], list):
            total_count += 1
            try:
                # 执行每个rationale中的代码
                for code in item["rationale"]:
                    # 创建一个新的局部命名空间来执行代码
                    local_vars = {}
                    exec(code, globals(), local_vars)
                success_count += 1
            except Exception as e:
                print(f"执行失败: {str(e)}")
                print(f"问题: {item.get('usr_msg', '')[:100]}...")
                continue

    print(f"\n执行统计:")
    print(f"总计数: {total_count}")
    print(f"成功数: {success_count}")
    print(f"成功率: {success_count/total_count*100:.2f}%")

def main():
    if len(sys.argv) != 2:
        print("使用方法: python run.py <json_file>")
        return 1
        
    json_file = sys.argv[1]
    execute_rationale_code(json_file)
    return 0

if __name__ == "__main__":
    sys.exit(main())
