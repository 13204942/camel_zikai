#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
from pathlib import Path

def create_standard_python_code(case_data):
    """
    为每个病例生成标准的Python代码块
    
    参数:
        case_data: JSON数据中的一个病例数据
    
    返回:
        生成的完整Python代码块字符串
    """
    usr_msg = case_data.get("usr_msg", "")
    final_answer = case_data.get("final_answer", "")
    calc_name = case_data.get("metadata", {}).get("calc_name", "Unknown Calculation")
    rationale_list = case_data.get("rationale", [])
    
    # 根据计算名称决定需要导入的模块
    selected_modules = select_modules_for_calc(calc_name)
    import_statements = generate_import_statements(selected_modules)
    
    # 创建标准Python代码块
    code_lines = [
        "#!/usr/bin/env python",
        "# -*- coding: utf-8 -*-",
        "",
        f"# 计算: {calc_name}",
        f"# 最终答案: {final_answer}",
        "",
        import_statements,
        "",
        "# 用户消息摘要:",
        f"'''{usr_msg[:150]}...'''",
        "",
        ""
    ]
    
    # 提取计算步骤并生成代码
    step_count = 1
    variables = []
    
    # 如果有rationale_list，处理其中的工具调用
    if isinstance(rationale_list, list):
        for item in rationale_list:
            # 处理工具调用
            if isinstance(item, dict) and "tool_name" in item and "args" in item:
                tool_name = item.get("tool_name")
                args = item.get("args", {})
                result = item.get("result", "")
                
                var_name = f"step{step_count:02d}"
                variables.append(var_name)
                
                code_step = generate_tool_call_code(tool_name, args, var_name)
                if code_step:
                    code_lines.extend(code_step)
                    step_count += 1
    # 如果rationale是字符串形式，尝试提取已有步骤
    elif isinstance(rationale_list, str) and "step" in rationale_list:
        # 如果rationale已经是完整的Python代码，直接返回
        return rationale_list
    
    # 添加打印结果的代码
    if variables:
        code_lines.append("# 打印最终结果")
        code_lines.append(f"result = {variables[-1]}")
        code_lines.append("print(result)")
        code_lines.append("")
    else:
        # 如果没有解析到具体计算步骤，添加一个基本的计算函数调用
        var_name = "step01"
        default_tool = get_default_tool_for_calc(calc_name)
        if default_tool:
            code_lines.extend(generate_default_tool_call(default_tool, calc_name, var_name))
            code_lines.append("# 打印最终结果")
            code_lines.append(f"result = {var_name}")
            code_lines.append("print(result)")
            code_lines.append("")
    
    return "\n".join(code_lines)

def select_modules_for_calc(calc_name):
    """根据计算名称选择需要的模块"""
    # 通用模块
    common_modules = ["adjusted_body_weight", "bmi_calculator", "ideal_body_weight"]
    
    # 根据计算名称添加特定模块
    if "Creatinine Clearance" in calc_name:
        return common_modules + ["creatinine_clearance"]
    elif "BMI" in calc_name:
        return ["bmi_calculator"]
    elif "Ideal Body Weight" in calc_name:
        return ["ideal_body_weight"]
    elif "Adjusted Body Weight" in calc_name:
        return common_modules
    elif "BSA" in calc_name or "Body Surface Area" in calc_name:
        return ["bsa_calculator"]
    elif "Anion Gap" in calc_name:
        return ["anion_gap"]
    elif "MDRD GFR" in calc_name:
        return ["mdrd_gfr"]
    elif "CKD-EPI" in calc_name:
        return ["ckd_epi_2021_creatinine"]
    elif "QT" in calc_name:
        if "Bazett" in calc_name:
            return ["qt_calculator_bazett"]
        elif "Framingham" in calc_name:
            return ["qt_calculator_framingham"]
        elif "Fredericia" in calc_name:
            return ["qt_calculator_fredericia"]
        elif "Hodges" in calc_name:
            return ["qt_calculator_hodges"]
        elif "Rautaharju" in calc_name:
            return ["qt_calculator_rautaharju"]
        else:
            return ["qt_calculator_bazett", "qt_calculator_framingham", "qt_calculator_fredericia", 
                   "qt_calculator_hodges", "qt_calculator_rautaharju"]
    elif "SOFA" in calc_name:
        return ["sofa"]
    elif "APACHE II" in calc_name:
        return ["apache_ii"]
    elif "CURB-65" in calc_name:
        return ["curb_65"]
    elif "PSI Score" in calc_name or "Pneumonia Severity Index" in calc_name:
        return ["psi_score"]
    elif "MELD-Na" in calc_name:
        return ["meldna"]
    elif "Child-Pugh" in calc_name:
        return ["child_pugh_score"]
    elif "Caprini" in calc_name:
        return ["caprini_score"]
    elif "CHA2DS2-VASc" in calc_name:
        return ["cha2ds2_vasc_score"]
    elif "HAS-BLED" in calc_name:
        return ["has_bled_score"]
    elif "HEART Score" in calc_name:
        return ["heart_score"]
    elif "Glasgow Coma" in calc_name:
        return ["glasgow_coma_score"]
    elif "Glasgow Bleeding" in calc_name:
        return ["glasgow_bleeding_score"]
    elif "Cardiac Risk Index" in calc_name:
        return ["cardiac_risk_index"]
    elif "FeverPAIN" in calc_name:
        return ["feverpain"]
    elif "Centor" in calc_name:
        return ["centor_score"]
    elif "Wells" in calc_name:
        if "DVT" in calc_name:
            return ["wells_criteria_dvt"]
        elif "PE" in calc_name:
            return ["wells_criteria_pe"]
        else:
            return ["wells_criteria_dvt", "wells_criteria_pe"]
    elif "FIB-4" in calc_name or "Fibrosis" in calc_name:
        return ["fibrosis_4"]
    elif "Framingham Risk" in calc_name:
        return ["framingham_risk_score"]
    elif "HOMA-IR" in calc_name:
        return ["homa_ir"]
    elif "Free Water Deficit" in calc_name:
        return ["free_water_deficit"]
    elif "Serum Osmolality" in calc_name:
        return ["sOsm"]
    elif "Gestational Age" in calc_name:
        return ["gestational_age"]
    elif "Estimated Due Date" in calc_name:
        return ["estimated_due_date"]
    elif "Conception Date" in calc_name:
        return ["conception_date"]
    elif "Delta Gap" in calc_name:
        if "Albumin Corrected" in calc_name:
            return ["albumin_corrected_delta_gap"]
        else:
            return ["delta_gap"]
    elif "Albumin Corrected Anion" in calc_name:
        return ["albumin_corrected_anion"]
    elif "Albumin Delta Ratio" in calc_name:
        return ["albumin_delta_ratio"]
    elif "Calcium Correction" in calc_name:
        return ["calcium_correction"]
    elif "LDL" in calc_name:
        return ["ldl_calculated"]
    elif "Mean Arterial Pressure" in calc_name:
        return ["mean_arterial_pressure"]
    elif "Maintenance Fluid" in calc_name:
        return ["maintenance_fluid_calc"]
    elif "Target Weight" in calc_name:
        return ["target_weight"]
    elif "FENa" in calc_name:
        return ["compute_fena"]
    elif "MME" in calc_name:
        return ["mme"]
    elif "PERC" in calc_name:
        return ["perc_rule"]
    elif "SIRS" in calc_name:
        return ["sirs_criteria"]
    elif "SCH" in calc_name:
        return ["sch"]
    elif "Steroid Conversion" in calc_name:
        return ["steroid_conversion"]
    elif "CCI" in calc_name or "Charlson Comorbidity Index" in calc_name:
        return ["cci"]
    else:
        # 默认返回常用模块
        return common_modules

def generate_import_statements(modules):
    """生成导入语句"""
    return f"from camel.toolkits.medcalc_bench import {', '.join(modules)}"

def get_default_tool_for_calc(calc_name):
    """根据计算名称获取默认工具"""
    if "Creatinine Clearance" in calc_name:
        return "creatinine_clearance"
    elif "BMI" in calc_name:
        return "bmi_calculator"
    elif "Ideal Body Weight" in calc_name:
        return "ideal_body_weight"
    elif "Adjusted Body Weight" in calc_name:
        return "adjusted_body_weight"
    # ... 添加其他工具的映射
    return None


def generate_tool_call_code(tool_name, args, var_name):
    """根据工具名称和参数生成代码"""
    code_lines = []
    
    if tool_name == "bmi_calculator":
        code_lines.append(f"{var_name} = bmi_calculator.bmi_calculator_explanation({{")
        code_lines.append(f'    "weight": ({args.get("weight_value")}, "{args.get("weight_unit")}"),')
        code_lines.append(f'    "height": ({args.get("height_value")}, "{args.get("height_unit")}")')
        code_lines.append("})")
        code_lines.append("")
    
    elif tool_name == "ideal_body_weight":
        code_lines.append(f"{var_name} = ideal_body_weight.ibw_explanation({{")
        code_lines.append(f'    "height": ({args.get("height_value")}, "{args.get("height_unit")}"),')
        code_lines.append(f'    "sex": "{args.get("sex")}",')
        code_lines.append(f'    "age": {args.get("age")}')
        code_lines.append("})")
        code_lines.append("")
    
    elif tool_name == "adjusted_body_weight":
        code_lines.append(f"{var_name} = adjusted_body_weight.abw_explanation({{")
        code_lines.append(f'    "weight": ({args.get("weight_value")}, "{args.get("weight_unit")}"),')
        code_lines.append(f'    "height": ({args.get("height_value")}, "{args.get("height_unit")}"),')
        code_lines.append(f'    "sex": "{args.get("sex")}",')
        code_lines.append(f'    "age": {args.get("age")}')
        code_lines.append("})")
        code_lines.append("")
    
    elif tool_name == "creatinine_clearance":
        code_lines.append(f"{var_name} = creatinine_clearance.generate_cockcroft_gault_explanation({{")
        code_lines.append(f'    "weight": ({args.get("weight_value")}, "{args.get("weight_unit")}"),')
        code_lines.append(f'    "height": ({args.get("height_value")}, "{args.get("height_unit")}"),')
        code_lines.append(f'    "sex": "{args.get("sex")}",')
        code_lines.append(f'    "creatinine": ({args.get("creatinine_value")}, "{args.get("creatinine_unit")}"),')
        code_lines.append(f'    "age": ({args.get("age_value")}, "{args.get("age_unit")}")')
        code_lines.append("})")
        code_lines.append("")
    
    # 为其他工具类型添加处理逻辑
    # ... 添加更多工具的代码生成
    
    return code_lines

def replace_rationale_with_code(input_file, output_file=None):
    """
    将rationaledata.json文件中的rationale部分替换为标准Python代码块
    
    参数:
        input_file: 输入的JSON文件路径
        output_file: 输出的JSON文件路径，默认为None（覆盖原文件）
    """
    # 读取JSON数据
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # 遍历每个病例
    for i, case_data in enumerate(data):
        # 如果rationale已经是字符串形式的Python代码，保留它
        if isinstance(case_data.get("rationale"), str) and case_data.get("rationale").startswith("#!/usr/bin/env python"):
            continue
            
        # 生成标准Python代码
        complete_code = create_standard_python_code(case_data)
        
        # 将整个代码块作为rationale
        data[i]["rationale"] = complete_code
    
    # 写入输出文件
    output_path = output_file if output_file else input_file
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    return output_path

if __name__ == "__main__":
    # 设置默认路径
    default_input = "output.json"
    default_output = "rationaledata_standard_code.json"
    
    # 获取命令行参数
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = default_input
        
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = default_output
    
    # 转换为绝对路径
    base_dir = Path(__file__).parent
    input_file = str(base_dir / input_file)
    output_file = str(base_dir / output_file)
    
    print(f"从 {input_file} 读取数据")
    print(f"输出到 {output_file}")
    
    # 执行替换
    output_path = replace_rationale_with_code(input_file, output_file)
    print(f"已将rationale替换为标准Python代码: {output_path}") 