import json
import sys
import os
import traceback
import re
from collections import defaultdict
from datetime import datetime
from examples.toolkits.med.moudles import *

def execute_rationale_code(json_file, log_file=None):
    """执行JSON文件中的rationale代码并统计成功数"""
    success_count = 0
    total_count = 0
    failed_items = []
    error_types = defaultdict(list)  # 按错误类型统计
    calc_types = defaultdict(lambda: defaultdict(int))  # 按计算类型统计错误
    
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
                    for code_idx, code in enumerate(item["rationale"]):
                        # 创建一个新的局部命名空间来执行代码
                        local_vars = {}
                        
                        # 提取计算类型信息
                        calc_type = "未知计算"
                        tool_match = re.search(r'# (\w+) function call:', code)
                        if tool_match:
                            tool_name = tool_match.group(1)
                            calc_type = get_calculation_type(tool_name, code)
                        
                        try:
                            exec(code, globals(), local_vars)
                        except Exception as e:
                            error_type = type(e).__name__
                            error_details = str(e)
                            error_types[error_type].append(idx)
                            calc_types[calc_type][error_type] += 1
                            
                            # 获取更详细的错误信息
                            tb = traceback.format_exc()
                            
                            # 记录错误并中断执行此条目的后续代码
                            log.write(f"执行失败: 条目 {idx}, 代码段 {code_idx+1}, 错误类型: {error_type}, 错误详情: {error_details}\n")
                            log.write(f"计算类型: {calc_type}\n")
                            log.write(f"代码:\n{code}\n")
                            log.write(f"错误追踪:\n{tb}\n")
                            
                            # 记录失败的条目
                            failed_items.append({
                                "index": idx,
                                "error": f"{error_type}: {error_details}",
                                "error_type": error_type,
                                "calc_type": calc_type,
                                "code_index": code_idx,
                                "code": code,
                                "question": item.get('usr_msg', ''),
                                "rationale": item.get("rationale", [])
                            })
                            
                            # 打印错误信息
                            print(f"执行失败: 条目 {idx}, 代码段 {code_idx+1}")
                            print(f"计算类型: {calc_type}")
                            print(f"错误类型: {error_type}")
                            print(f"错误详情: {error_details}")
                            print(f"问题: {item.get('usr_msg', '')[:100]}...")
                            
                            # 中断此条目的执行
                            raise
                        
                    # 如果所有代码都执行成功
                    success_count += 1
                    log.write(f"成功: {item.get('usr_msg', '')[:100]}...\n")
                
                except Exception:
                    # 这里不需要做任何事，因为已经在内部循环中记录了错误
                    continue

        # 写入统计信息
        stats = f"\n执行统计:\n"
        stats += f"总计数: {total_count}\n"
        stats += f"成功数: {success_count}\n"
        stats += f"失败数: {total_count - success_count}\n"
        stats += f"成功率: {success_count/total_count*100:.2f}%\n\n"
        
        # 按错误类型统计
        stats += f"=按错误类型统计 -\n"
        for error_type, indices in error_types.items():
            stats += f"错误类型:{error_type}(错误数:{len(indices)})\n"
        
        # 按计算类型统计错误
        stats += f"\n=按计算类型分组的错误 -\n"
        for calc_type, errors in calc_types.items():
            error_count = sum(errors.values())
            stats += f"计算:{calc_type}(错误数:{error_count})"
            for error_type, count in errors.items():
                stats += f"{error_type}:{count} 次"
            stats += "\n"
        
        log.write(stats)
        print(stats)
        
    print(f"执行日志已保存到: {os.path.abspath(log_file)}")
    return log_file, failed_items, error_types, calc_types

def get_calculation_type(tool_name, code):
    """根据工具名称和代码内容推断计算类型"""
    # 从代码中查找计算类型的映射
    mapping = {
        "bmi_calculator": "Body Mass Index(BMI)",
        "ideal_body_weight": "Ideal Body Weight",
        "adjusted_body_weight": "Adjusted Body Weight",
        "creatinine_clearance": "Creatinine clearance(Cockcroft-Gault Equation)",
        "ckd_epi": "CKD-EPI Equations for Glomerular Filtration Rate",
        "mdrd_gfr": "MDRD GFR Calculation",
        "compute_fib4": "Fibrosis-4(FIB-4)Index for Liver Fibrosis",
        "compute_centor_score": "Centor Score (Modified/McIsaac)for strep Pharyngitis",
        "compute_ldl": "LDLcalculated",
        "sirs_criteria": "SIRS Criteria",
        "fredericia_calculator": "QTc Fridericia calculator",
        "target_weight": "Target weight",
        "add_40_weeks": "Estimated Due Date",
        "compute_steroid_conversion": "Steroid Conversion Calculator",
        "mme": "Morphine Milligram Equivalents(MME)Calculator",
        "add_2_weeks": "Estimated of Conception",
        "generate_cha2ds2_vasc": "CHA2DS2-VASc Score"
    }
    
    # 根据工具名获取计算类型
    if tool_name in mapping:
        return mapping[tool_name]
    
    # 如果在映射中找不到，尝试从代码中提取函数名
    func_match = re.search(r'from camel\.toolkits\.medcalc_bench\.(\w+) import (\w+)', code)
    if func_match:
        module_name = func_match.group(1)
        function_name = func_match.group(2)
        
        # 通过模块名和函数名推断计算类型
        if module_name == "bmi_calculator" and "bmi" in function_name:
            return "Body Mass Index(BMI)"
        elif "ideal_body_weight" in module_name:
            return "Ideal Body Weight"
        elif "creatinine_clearance" in module_name:
            return "Creatinine clearance(Cockcroft-Gault Equation)"
        elif "ckd_epi" in module_name:
            return "CKD-EPI Equations for Glomerular Filtration Rate"
        elif "target_weight" in module_name:
            return "Target weight"
        
    # 默认返回工具名作为计算类型
    return tool_name

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
    log_file, failed_items, error_types, calc_types = execute_rationale_code(json_file, log_file)
    
    # 如果需要生成错误日志
    if get_error:
        get_error_log(failed_items, error_log_file)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
