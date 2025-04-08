import json
import sys
import os
import traceback
from datetime import datetime
from examples.toolkits.med.moudles import *

def execute_rationale_code(json_file, log_file=None):
    """执行JSON文件中的rationale代码并统计成功数"""
    success_count = 0
    total_count = 0
    failed_items = []
    error_stats = {}  # 用于统计不同类型的错误
    
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
            if "rationale" not in item or not isinstance(item["rationale"], list):
                continue
                
            total_count += 1
            calc_name = item.get('metadata', {}).get('calc_name', '未知计算')
            
            try:
                # 执行每个rationale中的代码
                for code_idx, code in enumerate(item["rationale"]):
                    # 创建一个新的局部命名空间来执行代码
                    local_vars = {}
                    try:
                        exec(code, globals(), local_vars)
                    except Exception as e:
                        # 记录代码执行错误
                        error_type = type(e).__name__
                        error_stats[error_type] = error_stats.get(error_type, 0) + 1
                        
                        # 获取完整的错误堆栈
                        error_trace = traceback.format_exc()
                        # 记录失败的条目
                        failed_items.append({
                            "index": idx,
                            "calc_name": calc_name,
                            "error_type": error_type,
                            "error_message": str(e),
                            "error_trace": error_trace,
                            "code_snippet": code.splitlines()[0][:100] + "...",  # 取第一行代码
                            "question": item.get('usr_msg', '')[:200] + "...",
                            "rationale_index": code_idx,
                            "expected_answer": item.get('final_answer', '无')
                        })
                        print(local_vars)
                        
                        log.write(f"\n--- 执行失败 (项目 {idx}) ---\n")
                        log.write(f"计算名称: {calc_name}\n")
                        log.write(f"问题摘要: {item.get('usr_msg', '')[:200]}...\n")
                        log.write(f"代码片段: {code.splitlines()[0][:100]}...\n")
                        log.write(f"错误类型: {error_type}\n")
                        log.write(f"错误信息: {str(e)}\n")
                        log.write(f"预期答案: {item.get('final_answer', '无')}\n")
                        log.write(f"错误堆栈:\n{error_trace}\n")
                        raise  # 重新抛出异常以中断当前item的执行
                
                # 如果所有代码都执行成功
                success_count += 1
                # log.write(f"成功: [{calc_name}] {item.get('usr_msg', '')[:100]}...\n")
                
            except Exception as e:
                # 这里捕获的是代码执行中抛出的异常
                continue

        # 写入详细的统计信息
        stats = f"\n=== 执行统计 ===\n"
        stats += f"总计数: {total_count}\n"
        stats += f"成功数: {success_count}\n"
        stats += f"失败数: {total_count - success_count}\n"
        stats += f"成功率: {success_count/total_count*100:.2f}%\n\n"
        
        # 添加错误类型统计
        if error_stats:
            stats += "=== 错误类型统计 ===\n"
            for error_type, count in sorted(error_stats.items(), key=lambda x: x[1], reverse=True):
                stats += f"{error_type}: {count} 次 ({count/total_count*100:.1f}%)\n"
        
        log.write(stats)
        print(stats)
        
    print(f"执行日志已保存到: {os.path.abspath(log_file)}")
    return log_file, failed_items, error_stats

def get_error_log(failed_items, error_stats, output_file=None):
    """生成执行错误日志文件"""
    if not failed_items:
        print("没有执行错误")
        return None
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"error_log_{timestamp}.json"
    
    # 准备错误分析报告
    error_report = {
        "summary": {
            "total_errors": len(failed_items),
            "error_types": error_stats,
            "most_common_error": max(error_stats.items(), key=lambda x: x[1]) if error_stats else None
        },
        "errors": failed_items
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(error_report, f, ensure_ascii=False, indent=2)
    
    print(f"错误日志已保存到: {os.path.abspath(output_file)}")
    return output_file

def analyze_errors(error_log_file):
    """分析错误日志并提供建议"""
    with open(error_log_file, 'r', encoding='utf-8') as f:
        error_data = json.load(f)
    
    print("\n=== 错误分析报告 ===")
    print(f"总错误数: {error_data['summary']['total_errors']}")
    print(f"最常见的错误类型: {error_data['summary']['most_common_error']}")
    
    # 按计算类型分组错误
    calc_errors = {}
    for error in error_data['errors']:
        calc_name = error['calc_name']
        if calc_name not in calc_errors:
            calc_errors[calc_name] = []
        calc_errors[calc_name].append(error)
    
    print("\n=== 按计算类型分组的错误 ===")
    for calc_name, errors in calc_errors.items():
        print(f"\n计算: {calc_name} (错误数: {len(errors)})")
        error_types = {}
        for error in errors:
            error_type = error['error_type']
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {error_type}: {count} 次")
    
    # 提供常见错误的解决方案建议
    print("\n=== 常见错误解决方案建议 ===")
    common_solutions = {
        "NameError": "检查变量或函数名是否正确拼写，确保所有需要的模块已导入",
        "TypeError": "检查函数参数类型是否正确，确保传递给函数的参数类型与预期一致",
        "AttributeError": "检查对象是否有所调用的属性或方法，可能是对象类型不正确",
        "ValueError": "检查输入值是否在有效范围内，确保数据格式正确",
        "KeyError": "检查字典键是否存在，确保访问的键在字典中",
        "ImportError": "检查模块是否安装，路径是否正确，模块名是否拼写正确"
    }
    
    for error_type in error_data['summary']['error_types']:
        if error_type in common_solutions:
            print(f"{error_type}: {common_solutions[error_type]}")

def main():
    # 设置默认参数
    default_json_file = "./examples/toolkits/med/output_code_replaced.json"
    default_log_file = "./examples/toolkits/med/med.log"
    
    # 如果没有提供参数，使用默认值
    if len(sys.argv) < 2:
        print(f"使用默认参数:")
        print(f"JSON文件: {default_json_file}")
        print(f"日志文件: {default_log_file}")
        json_file = default_json_file
        log_file = default_log_file
        error_log_file = None
        get_error = True  # 默认生成错误日志
    else:
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
        
        # 如果没有提供日志文件，使用默认值
        if log_file is None:
            log_file = default_log_file

    # 执行代码并获取失败项
    log_file, failed_items, error_stats = execute_rationale_code(json_file, log_file)
    
    # 如果需要生成错误日志
    if get_error and failed_items:
        error_log_file = get_error_log(failed_items, error_stats, error_log_file)
        if error_log_file:
            analyze_errors(error_log_file)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())