import json
import sys
import os
import traceback
from datetime import datetime
from examples.toolkits.med.moudles import *

def execute_rationale_code(json_file, log_file=None):
    """执行JSON文件中的rationale代码并统计成功数和答案正确率"""
    success_count = 0
    total_count = 0
    correct_answer_count = 0
    failed_items = []
    error_stats = {}
    answer_discrepancies = []
    
    if log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"execution_log_{timestamp}.txt"
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(log_file, 'w', encoding='utf-8') as log:
        log.write(f"执行日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"输入文件: {json_file}\n\n")
        
        for idx, item in enumerate(data):
            if "rationale" not in item or not isinstance(item["rationale"], list):
                continue
                
            total_count += 1
            calc_name = item.get('metadata', {}).get('calc_name', '未知计算')
            final_answer = item.get('final_answer', None)
            
            try:
                local_vars = {'__result__': None}
                tool_answer = None
                
                for code_idx, code in enumerate(item["rationale"]):
                    try:
                        modified_code = code + "\n__result__ = locals().get('result', None)"
                        exec(modified_code, globals(), local_vars)
                        
                        # 获取执行结果
                        execution_result = local_vars.get('__result__', {})
                        if isinstance(execution_result, dict):
                            tool_answer = execution_result.get('Answer', None)
                        
                    except Exception as e:
                        error_type = type(e).__name__
                        error_stats[error_type] = error_stats.get(error_type, 0) + 1
                        
                        error_trace = traceback.format_exc()
                        failed_items.append({
                            "index": idx,
                            "calc_name": calc_name,
                            "error_type": error_type,
                            "error_message": str(e),
                            "error_trace": error_trace,
                            "code_snippet": code.splitlines()[0][:100] + "...",
                            "question": item.get('usr_msg', '')[:200] + "...",
                            "rationale_index": code_idx,
                            "expected_answer": final_answer or '无'
                        })
                        log.write(f"\n--- 执行失败 (项目 {idx}) ---\n")
                        log.write(f"计算名称: {calc_name}\n")
                        log.write(f"问题摘要: {item.get('usr_msg', '')[:200]}...\n")
                        log.write(f"代码片段: {code.splitlines()[0][:100]}...\n")
                        log.write(f"错误类型: {error_type}\n")
                        log.write(f"错误信息: {str(e)}\n")
                        log.write(f"预期答案: {final_answer or '无'}\n")
                        log.write(f"错误堆栈:\n{error_trace}\n")
                        raise
                
                # 答案比较逻辑
                if tool_answer is not None and final_answer is not None:
                    try:
                        # 处理可能带单位的答案（如"66.778 kg"）
                        clean_tool_answer = ''.join(c for c in str(tool_answer) 
                                            if c.isdigit() or c in ['.', '-'])
                        clean_final_answer = ''.join(c for c in str(final_answer) 
                                             if c.isdigit() or c in ['.', '-'])
                        
                        tool_float = float(clean_tool_answer)
                        final_float = float(clean_final_answer)
                        
                        is_correct = abs(tool_float - final_float) < 0.001  # 允许0.001的误差
                        if is_correct:
                            correct_answer_count += 1
                        else:
                            answer_discrepancies.append({
                                "index": idx,
                                "calc_name": calc_name,
                                "tool_answer": tool_answer,
                                "final_answer": final_answer,
                                "difference": abs(tool_float - final_float),
                                "question": item.get('usr_msg', '')[:200] + "..."
                            })
                    except (ValueError, TypeError) as e:
                        answer_discrepancies.append({
                            "index": idx,
                            "calc_name": calc_name,
                            "error": "Answer format error",
                            "tool_answer": str(tool_answer),
                            "final_answer": str(final_answer),
                            "question": item.get('usr_msg', '')[:200] + "..."
                        })
                
                success_count += 1
                
            except Exception:
                continue

        # 统计信息
        stats = f"\n=== 执行统计 ===\n"
        stats += f"总项目数: {total_count}\n"
        stats += f"成功执行: {success_count}\n"
        stats += f"执行失败: {total_count - success_count}\n"
        stats += f"执行成功率: {success_count/total_count*100:.2f}%\n\n"
        
        stats += f"=== 答案准确性 ===\n"
        stats += f"正确答案数: {correct_answer_count}\n"
        stats += f"答案错误数: {max(0, success_count - correct_answer_count)}\n"
        stats += f"答案正确率: {correct_answer_count/total_count*100:.2f}%\n\n"
        
        # 错误类型统计
        if error_stats:
            stats += "=== 错误类型统计 ===\n"
            for error_type, count in sorted(error_stats.items(), key=lambda x: x[1], reverse=True):
                stats += f"{error_type}: {count} 次 ({count/total_count*100:.1f}%)\n"
            stats += "\n"
        
        # 答案差异详情
        if answer_discrepancies:
            stats += "=== 全部答案差异===\n"
            for diff in answer_discrepancies:
                stats += (
                    f"项目 {diff['index']} - {diff['calc_name']}\n"
                    f"工具答案: {diff.get('tool_answer', 'N/A')}\n"
                    f"标准答案: {diff.get('final_answer', 'N/A')}\n"
                    f"差异值: {diff.get('difference', 'N/A')}\n"
                    f"问题摘要: {diff.get('question', '')}\n"
                    "----------------------------\n"
                )
            
            # 差异分析
            calc_diff_stats = {}
            for diff in answer_discrepancies:
                calc_name = diff['calc_name']
                if 'difference' in diff:
                    calc_diff_stats.setdefault(calc_name, []).append(diff['difference'])
            
            if calc_diff_stats:
                stats += "\n=== 各类计算平均差异 ===\n"
                for calc_name, diffs in calc_diff_stats.items():
                    avg_diff = sum(diffs) / len(diffs)
                    stats += f"{calc_name}: {avg_diff:.4f} (共{len(diffs)}处差异)\n"
        
        log.write(stats)
        print(stats)
    
    print(f"执行日志已保存到: {os.path.abspath(log_file)}")
    return log_file, failed_items, error_stats, answer_discrepancies

def get_error_log(failed_items, error_stats, output_file=None):
    """生成执行错误日志文件"""
    if not failed_items:
        print("没有执行错误")
        return None
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"error_log_{timestamp}.json"
    
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
            print(f"\n{error_type}解决方案: {common_solutions[error_type]}")

def analyze_answer_discrepancies(answer_discrepancies, output_file=None):
    """生成答案差异分析报告"""
    if not answer_discrepancies:
        print("没有答案差异需要分析")
        return None
    
    if output_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"answer_discrepancy_{timestamp}.json"
    
    # 按计算类型分组
    calc_groups = {}
    for diff in answer_discrepancies:
        calc_groups.setdefault(diff['calc_name'], []).append(diff)
    
    # 计算各类统计量
    report = {
        "summary": {
            "total_discrepancies": len(answer_discrepancies),
            "calculations_with_issues": len(calc_groups)
        },
        "details_by_calculation": {}
    }
    
    for calc_name, diffs in calc_groups.items():
        # 只统计有数值差异的情况
        numerical_diffs = [d for d in diffs if 'difference' in d]
        if numerical_diffs:
            avg_diff = sum(d['difference'] for d in numerical_diffs) / len(numerical_diffs)
            max_diff = max(d['difference'] for d in numerical_diffs)
            min_diff = min(d['difference'] for d in numerical_diffs)
        else:
            avg_diff = max_diff = min_diff = None
        
        report["details_by_calculation"][calc_name] = {
            "count": len(diffs),
            "average_difference": avg_diff,
            "max_difference": max_diff,
            "min_difference": min_diff,
            "examples": diffs[:3]  # 保留3个示例
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"答案差异分析已保存到: {os.path.abspath(output_file)}")
    return output_file

def main():
    default_json_file = "./examples/toolkits/med/output_code_replaced.json"
    default_log_file = "./examples/toolkits/med/med.log"
    
    if len(sys.argv) < 2:
        print(f"使用默认参数:")
        print(f"JSON文件: {default_json_file}")
        print(f"日志文件: {default_log_file}")
        json_file = default_json_file
        log_file = default_log_file
        get_error = True
        get_discrepancy = True
    else:
        json_file = sys.argv[1]
        log_file = None
        get_error = False
        get_discrepancy = False
        
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "--error-log":
                get_error = True
                if i+1 < len(sys.argv) and not sys.argv[i+1].startswith("--"):
                    error_log_file = sys.argv[i+1]
            elif sys.argv[i] == "--discrepancy":
                get_discrepancy = True
            elif i == 2 and not sys.argv[i].startswith("--"):
                log_file = sys.argv[i]
        
        if log_file is None:
            log_file = default_log_file

    # 执行代码
    log_file, failed_items, error_stats, answer_discrepancies = execute_rationale_code(json_file, log_file)
    
    # 生成错误日志
    if get_error and failed_items:
        error_log_file = get_error_log(failed_items, error_stats)
        if error_log_file:
            analyze_errors(error_log_file)
    
    # 生成答案差异分析
    if get_discrepancy and answer_discrepancies:
        discrepancy_file = analyze_answer_discrepancies(answer_discrepancies)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())