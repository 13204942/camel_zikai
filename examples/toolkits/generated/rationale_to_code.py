#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
from pathlib import Path

def convert_args_to_dict_format(tool_name, args):
    """
    根据工具名称和参数将参数转换为正确的字典格式
    """
    # BMI计算器参数转换
    if tool_name == "bmi_calculator":
        return {
            "weight": (args.get("weight_value"), args.get("weight_unit")),
            "height": (args.get("height_value"), args.get("height_unit"))
        }
    
    # 理想体重计算器参数转换
    elif tool_name == "ideal_body_weight":
        return {
            "height": (args.get("height_value"), args.get("height_unit")),
            "sex": args.get("sex"),
            "age": args.get("age")
        }
    
    # 肌酐清除率计算器参数转换
    elif tool_name == "creatinine_clearance":
        return {
            "weight": (args.get("weight_value"), args.get("weight_unit")),
            "height": (args.get("height_value"), args.get("height_unit")),
            "sex": args.get("sex"),
            "creatinine": (args.get("creatinine_value"), args.get("creatinine_unit")),
            "age": (args.get("age_value"), args.get("age_unit"))
        }
    
    # 调整体重计算器参数转换  
    elif tool_name == "adjusted_body_weight":
        return {
            "weight": (args.get("weight_value"), args.get("weight_unit")),
            "height": (args.get("height_value"), args.get("height_unit")),
            "sex": args.get("sex"),
            "age": args.get("age")
        }
    
    # 默认情况直接返回原始参数
    return args

def generate_code_from_rationale(rationale_data, output_dir, case_index=None):
    """
    将rationale数据转换为对应的Python代码调用

    参数:
        rationale_data: JSON数据中的一个病例数据
        output_dir: 输出目录
        case_index: 病例索引
    """
    usr_msg = rationale_data.get("usr_msg", "")
    rationale_list = rationale_data.get("rationale", [])
    final_answer = rationale_data.get("final_answer", "")
    calc_name = rationale_data.get("metadata", {}).get("calc_name", "Unknown Calculation")
    
    code_lines = [
        "#!/usr/bin/env python",
        "# -*- coding: utf-8 -*-",
        "",
        f"# 计算: {calc_name}",
        f"# 最终答案: {final_answer}",
        "",
        "from camel.toolkits.medcalc_bench import adjusted_body_weight, bmi_calculator, ideal_body_weight, creatinine_clearance",
        "",
        "# 用户消息摘要:",
        "'''" + usr_msg[:150] + "..." + "'''",
        "",
        ""
    ]
    
    step_count = 1
    variables = []
    
    for item in rationale_list:
        if "tool_name" not in item:
            continue
            
        tool_name = item.get("tool_name")
        args = item.get("args", {})
        
        if not args:
            continue
            
        variable_name = f"step{step_count:02d}"
        variables.append(variable_name)
        
        # 根据工具类型生成正确的代码
        if tool_name == "bmi_calculator":
            converted_args = convert_args_to_dict_format(tool_name, args)
            code_lines.append(f"{variable_name} = bmi_calculator.bmi_calculator_explanation({converted_args})")
            
        elif tool_name == "ideal_body_weight":
            converted_args = convert_args_to_dict_format(tool_name, args)
            code_lines.append(f"{variable_name} = ideal_body_weight.ibw_explanation({converted_args})")
            
        elif tool_name == "creatinine_clearance":
            converted_args = convert_args_to_dict_format(tool_name, args)
            code_lines.append(f"{variable_name} = creatinine_clearance.generate_cockcroft_gault_explanation({converted_args})")
            
        elif tool_name == "adjusted_body_weight":
            converted_args = convert_args_to_dict_format(tool_name, args)
            code_lines.append(f"{variable_name} = adjusted_body_weight.abw_explanation({converted_args})")
            
        code_lines.append("")
        step_count += 1
    
    # 添加最后一个结果的打印
    if variables:
        code_lines.append(f"# 打印最终结果")
        code_lines.append(f"result = {variables[-1]}")
        code_lines.append("print(result)")
        code_lines.append("")
    
    # 生成文件名
    filename = f"case_{case_index or 'unknown'}.py"
    file_path = os.path.join(output_dir, filename)
    
    # 写入文件
    with open(file_path, 'w') as f:
        f.write('\n'.join(code_lines))
    
    return file_path

def convert_all_cases(rationale_file, output_dir):
    """
    转换所有病例数据为Python代码
    
    参数:
        rationale_file: rationale数据文件路径
        output_dir: 输出目录
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 读取rationale数据
    with open(rationale_file, 'r') as f:
        data = json.load(f)
    
    generated_files = []
    
    # 转换每个病例
    for i, case_data in enumerate(data):
        file_path = generate_code_from_rationale(case_data, output_dir, i+1)
        generated_files.append(file_path)
        print(f"生成代码文件: {file_path}")
    
    return generated_files

if __name__ == "__main__":
    # 设置默认路径
    default_input = "examples/toolkits/rationaledata.json"
    default_output = "examples/toolkits/generated"
    
    # 获取命令行参数
    if len(sys.argv) > 1:
        rationale_file = sys.argv[1]
    else:
        rationale_file = default_input
        
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    else:
        output_dir = default_output
    
    # 转换为绝对路径
    base_dir = Path(__file__).parent.parent.parent.parent
    rationale_file = str(base_dir / rationale_file)
    output_dir = str(base_dir / output_dir)
    
    print(f"从 {rationale_file} 读取数据")
    print(f"输出目录: {output_dir}")
    
    # 执行转换
    files = convert_all_cases(rationale_file, output_dir)
    print(f"共生成 {len(files)} 个Python文件") 