import json
import os
import sys
import inspect

# 导入所有函数
from examples.toolkits.med.moudles import *

def get_function_mapping_from_modules():
    """
    从moudles.py文件中获取工具名称到函数的映射
    
    Returns:
        dict: 工具名称到函数的映射字典
    """
    # 获取所有导入的函数
    all_functions = {}
    for name, obj in globals().items():
        if inspect.isfunction(obj) and name.endswith('_explanation'):
            # 将函数名转换为工具名
            # 例如：abw_explanation -> adjusted_body_weight
            # bmi_calculator_explanation -> bmi_calculator
            tool_name = None
            
            # 处理特殊情况
            if name == 'abw_explanation':
                tool_name = 'adjusted_body_weight'
            elif name == 'ibw_explanation':
                tool_name = 'ideal_body_weight'
            elif name == 'generate_cockcroft_gault_explanation':
                tool_name = 'creatinine_clearance'
            elif name == 'mrdr_gfr_explanation':
                tool_name = 'mdrd_gfr'
            elif name == 'compute_fib4_explanation':
                tool_name = 'fibrosis_4'
            elif name == 'compute_cci_explanation':
                tool_name = 'cci'
            elif name == 'generate_cha2ds2_vasc_explanation':
                tool_name = 'cha2ds2_vasc_score'
            elif name == 'calculate_pe_wells_explanation':
                tool_name = 'wells_criteria_pe'
            elif name == 'compute_steroid_conversion_explanation':
                tool_name = 'steroid_conversion'
            elif name == 'compute_anion_gap_explanation':
                tool_name = 'anion_gap'
            elif name == 'compute_delta_gap_explanation':
                tool_name = 'delta_gap'
            elif name == 'compute_serum_osmolality_explanation':
                tool_name = 'sOsm'
            elif name == 'compute_albumin_corrected_anion_explanation':
                tool_name = 'albumin_corrected_anion'
            elif name == 'compute_albumin_corrected_delta_gap_explanation':
                tool_name = 'albumin_corrected_delta_gap'
            elif name == 'compute_albumin_delta_ratio_explanation':
                tool_name = 'albumin_delta_ratio'
            elif name == 'compute_sodium_correction_hyperglycemia_explanation':
                tool_name = 'sch'
            elif name == 'compute_ldl_explanation':
                tool_name = 'ldl_calculated'
            else:
                # 一般情况下去掉_explanation后缀
                tool_name = name.replace('_explanation', '')
            
            all_functions[tool_name] = obj
    
    # 添加手动映射以处理可能的名称差异
    manual_mappings = {
        'steroid_conversion': compute_steroid_conversion_explanation,
        'bsa': bsa_calculator_explaination,
        'bsa_calculator': bsa_calculator_explaination,
        'free_water_deficit': free_water_deficit_explanation,
        'cardiac_risk': compute_cardiac_index_explanation,
        'cardiac_risk_index': compute_cardiac_index_explanation,
        'centor': compute_centor_score_explanation,
        'calcium_correction': calculate_corrected_calcium_explanation,
        'maintenance_fluid': maintenance_fluid_explanation,
        'fever_pain': compute_fever_pain_explanation,
        'feverpain': compute_fever_pain_explanation,
        'glasgow_coma': compute_glasgow_coma_score_explanation,
        'conception': add_2_weeks_explanation,
        'estimated_due_date': add_40_weeks_explanation
    }
    
    # 添加手动映射
    for tool_name, func in manual_mappings.items():
        if tool_name not in all_functions:  # 只有在不存在时才添加
            all_functions[tool_name] = func
    
    return all_functions

def format_args_for_function(tool_name, args):
    """
    根据工具类型格式化参数
    
    Args:
        tool_name: 工具名称
        args: 原始参数字典
    
    Returns:
        dict: 格式化后的参数字典
    """
    formatted_args = {}
    
    # 特殊情况处理
    if tool_name == 'adjusted_body_weight':
        # 按照abw_explanation需要的格式组织参数
        if 'weight_value' in args and 'weight_unit' in args:
            formatted_args['weight'] = (args['weight_value'], args['weight_unit'])
        if 'height_value' in args and 'height_unit' in args:
            formatted_args['height'] = (args['height_value'], args['height_unit'])
        if 'sex' in args:
            formatted_args['sex'] = args['sex']
    
    elif tool_name == 'bmi_calculator':
        # 按照bmi_calculator_explanation需要的格式组织参数
        if 'weight' in args:
            if isinstance(args['weight'], list) and len(args['weight']) == 2:
                formatted_args['weight'] = tuple(args['weight'])
            else:
                formatted_args['weight'] = args['weight']
        if 'height' in args:
            if isinstance(args['height'], list) and len(args['height']) == 2:
                formatted_args['height'] = tuple(args['height'])
            else:
                formatted_args['height'] = args['height']
    
    elif tool_name == 'ideal_body_weight':
        # 按照ibw_explanation需要的格式组织参数
        if 'height_value' in args and 'height_unit' in args:
            formatted_args['height'] = (args['height_value'], args['height_unit'])
        if 'sex' in args:
            formatted_args['sex'] = args['sex']
    
    elif tool_name == 'creatinine_clearance':
        # 按照generate_cockcroft_gault_explanation需要的格式组织参数
        if 'weight_value' in args and 'weight_unit' in args:
            formatted_args['weight'] = (args['weight_value'], args['weight_unit'])
        if 'height_value' in args and 'height_unit' in args:
            formatted_args['height'] = (args['height_value'], args['height_unit'])
        if 'sex' in args:
            formatted_args['sex'] = args['sex']
        if 'creatinine_value' in args and 'creatinine_unit' in args:
            formatted_args['creatinine'] = (args['creatinine_value'], args['creatinine_unit'])
        if 'age_value' in args and 'age_unit' in args:
            formatted_args['age'] = (args['age_value'], args['age_unit'])
    
    elif tool_name == 'steroid_conversion':
        # 按照compute_steroid_conversion_explanation需要的格式组织参数
        if 'source_drug' in args:
            formatted_args['source_drug'] = args['source_drug']
        if 'target_drug' in args:
            formatted_args['target_drug'] = args['target_drug']
        if 'source_route' in args:
            formatted_args['source_route'] = args['source_route']
        if 'target_route' in args:
            formatted_args['target_route'] = args['target_route']
        if 'source_value' in args and 'source_unit' in args:
            formatted_args['source_dose'] = (args['source_value'], args['source_unit'])
        elif 'source_dose_value' in args and 'source_dose_unit' in args:
            formatted_args['source_dose'] = (args['source_dose_value'], args['source_dose_unit'])
    
    else:
        # 默认情况下，尝试将可能是元组的参数转换为正确格式
        for key, value in args.items():
            # 检查是否需要转换为元组格式
            if isinstance(value, list) and len(value) == 2:
                formatted_args[key] = tuple(value)
            elif key.endswith('_value') and key[:-6] + '_unit' in args:
                # 处理形如 'weight_value'/'weight_unit' 的参数对
                base_key = key[:-6]
                unit_key = base_key + '_unit'
                formatted_args[base_key] = (args[key], args[unit_key])
            else:
                # 其他情况直接复制
                if not key.endswith('_unit'):  # 跳过已处理的单位项
                    formatted_args[key] = value
    
    return formatted_args

def generate_direct_code(tool_name, args, function_map):
    """
    直接生成使用模块函数的代码
    
    Args:
        tool_name: 工具名称
        args: 参数字典
        function_map: 工具名称到函数的映射
    
    Returns:
        str: 生成的代码
    """
    if tool_name not in function_map:
        # 尝试寻找相似的工具名
        similar_tools = []
        for name in function_map.keys():
            if tool_name.lower() in name.lower() or name.lower() in tool_name.lower():
                similar_tools.append(name)
        
        if similar_tools:
            similar_str = ", ".join(similar_tools)
            return f"# 未找到工具: {tool_name}\n# 可能相似的工具: {similar_str}"
        else:
            return f"# 未找到工具: {tool_name}"
    
    function = function_map[tool_name]
    module_name = function.__module__
    function_name = function.__name__
    
    # 构建导入语句
    import_stmt = f"from {module_name} import {function_name}"
    
    # 根据工具类型格式化参数
    formatted_args = format_args_for_function(tool_name, args)
    
    # 构建参数字符串，保持可读性
    args_lines = []
    for key, value in formatted_args.items():
        if isinstance(value, tuple) and len(value) == 2:
            # 元组格式的参数
            args_lines.append(f'    "{key}": ({repr(value[0])}, {repr(value[1])}),  # {key}')
        else:
            # 其他格式的参数
            args_lines.append(f'    "{key}": {repr(value)},  # {key}')
    
    args_str = "{\n" + "\n".join(args_lines) + "\n}"
    
    call_stmt = f"""
# 准备输入参数
input_variables = {args_str}

# 调用函数
result = {function_name}(input_variables)

# 打印结果
print(result)
"""
    
    return f"{import_stmt}\n{call_stmt}"

def replace_rationale_with_code_in_json(input_file, output_file=None):
    """
    将JSON文件中的rationale替换为函数调用代码
    
    Args:
        input_file: 输入JSON文件路径
        output_file: 输出JSON文件路径
    
    Returns:
        输出文件路径
    """
    if not output_file:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}_code_replaced{ext}"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取函数映射
    function_map = get_function_mapping_from_modules()
    
    # 记录未找到的工具
    missing_tools = set()
    
    # 替换每个rationale
    for item in data:
        if "rationale" in item and isinstance(item["rationale"], list):
            # 收集所有生成的代码
            all_codes = []
            
            for rationale_item in item["rationale"]:
                if "tool_name" in rationale_item and "args" in rationale_item:
                    tool_name = rationale_item["tool_name"]
                    args = rationale_item["args"]
                    
                    # 生成代码
                    code = generate_direct_code(tool_name, args, function_map)
                    
                    # 如果未找到工具，记录下来
                    if code.startswith("# 未找到工具"):
                        missing_tools.add(tool_name)
                    
                    all_codes.append(f"# {tool_name} 函数调用:\n{code}\n")
            
            # 拼接所有代码
            if all_codes:
                # 创建新的rationale项
                new_rationale = [{
                    "content": "\n\n".join(all_codes)
                }]
                
                # 替换原始的rationale
                item["rationale"] = new_rationale
    
    # 如果有未找到的工具，输出警告
    if missing_tools:
        print(f"警告: 以下工具未找到: {', '.join(missing_tools)}")
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return output_file

def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='将JSON文件中的rationale替换为函数调用代码')
    parser.add_argument('input', help='输入JSON文件路径')
    parser.add_argument('-o', '--output', help='输出JSON文件路径')
    
    args = parser.parse_args()
    
    if not os.path.isfile(args.input):
        print(f"错误: 文件 '{args.input}' 不存在")
        return 1
    
    # 替换rationale
    output_file = replace_rationale_with_code_in_json(args.input, args.output)
    print(f"已将rationale替换为代码，输出文件: {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 