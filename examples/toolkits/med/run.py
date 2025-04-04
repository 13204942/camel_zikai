import json
import sys
import os
from datetime import datetime
from examples.toolkits.med.moudles import *

def execute_rationale_code(json_file, log_file=None):
    """执行JSON文件中的rationale代码并统计成功数"""
    success_count = 0
    total_count = 0
    failed_items = []
    
    # 准备日志文件
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"execution_log_{timestamp}.txt"
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 打开日志文件
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write(f"执行日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"输入文件: {json_file}\n\n")
        
        for idx, item in enumerate(data):
            if "rationale" in item and isinstance(item["rationale"], list):
                total_count += 1
                try:
                    # 执行每个rationale中的代码
                    for code in item["rationale"]:
                        # 创建一个新的局部命名空间来执行代码
                        local_vars = {}
                        exec(code, globals(), local_vars)
                    success_count += 1
                    log.write(f"成功: {item.get('usr_msg', '')[:100]}...\n")
                except Exception as e:
                    error_msg = f"执行失败: {str(e)}"
                    print(error_msg)
                    print(f"问题: {item.get('usr_msg', '')[:100]}...")
                    log.write(f"{error_msg}\n")
                    log.write(f"问题: {item.get('usr_msg', '')[:100]}...\n")
                    
                    # 记录失败的条目
                    failed_items.append({
                        "index": idx,
                        "error": str(e),
                        "question": item.get('usr_msg', ''),
                        "rationale": item.get("rationale", [])
                    })
                    continue

        # 写入统计信息
        stats = f"\n执行统计:\n"
        stats += f"总计数: {total_count}\n"
        stats += f"成功数: {success_count}\n"
        stats += f"失败数: {total_count - success_count}\n"
        stats += f"成功率: {success_count/total_count*100:.2f}%\n"
        
        log.write(stats)
        print(stats)
        
    print(f"执行日志已保存到: {os.path.abspath(log_file)}")
    return log_file, failed_items

def get_error_log(failed_items, output_file=None):
    """生成执行错误日志文件"""
    if not failed_items:
        print("没有执行错误")
        return None
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"error_log_{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(failed_items, f, ensure_ascii=False, indent=2)
    
    print(f"错误日志已保存到: {os.path.abspath(output_file)}")
    return output_file

def main():
    if len(sys.argv) < 2:
        print("使用方法: python run.py <json_file> [log_file] [--error-log [error_log_file]]")
        return 1
    
    json_file = sys.argv[1]
    log_file = None
    error_log_file = None
    get_error = False
    
    # 解析命令行参数
    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "--error-log":
            get_error = True
            if i+1 < len(sys.argv) and not sys.argv[i+1].startswith("--"):
                error_log_file = sys.argv[i+1]
        elif i == 2 and not sys.argv[i].startswith("--"):
            log_file = sys.argv[i]
    
    # 执行代码并获取失败项
    log_file, failed_items = execute_rationale_code(json_file, log_file)
    
    # 如果需要生成错误日志
    if get_error:
        get_error_log(failed_items, error_log_file)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
