import json
import os
import sys
import inspect
import re  # 导入re模块，确保全局可用
from datetime import date
import importlib
import math

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
            # 但是对于ckd_epi_2021_creatinine要特殊处理，保留完整名称
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
            elif name == 'add_2_weeks_explanation':
                tool_name = 'conception_date'
            elif name == 'add_40_weeks_explanation':
                tool_name = 'estimated_due_date'
            elif name == 'ckd_epi_2021_explanation':
                tool_name = 'ckd_epi_2021_creatinine'  # 保留完整名称
            elif name == 'sirs_criteria_explanation':
                tool_name = 'sirs_criteria'
            elif name == 'targetweight_explanation':
                tool_name = 'target_weight'
            elif name == 'fredericia_calculator_explanation':
                tool_name = 'qt_calculator_fredericia'
            elif name == 'compute_centor_score_explanation':
                tool_name = 'centor_score'
            elif name == 'mme_explanation':
                tool_name = 'mme'
            else:
                # 一般情况下去掉_explanation后缀
                tool_name = name.replace('_explanation', '')
            
            all_functions[tool_name] = obj
    
    # 添加手动映射以处理可能的名称差异
    manual_mappings = {
        # 肾功能相关
        'ckd_epi': ckd_epi_2021_explanation,
        'ckd_epi_2021': ckd_epi_2021_explanation,
        'ckd_epi_2021_creatinine': ckd_epi_2021_explanation,
        'ckd_epi_creatinine': ckd_epi_2021_explanation,
        
        # 类型转换工具
        'steroid_conversion': compute_steroid_conversion_explanation,
        'steroid_conversion_calculator': compute_steroid_conversion_explanation,
        
        # 体重相关工具
        'abw': abw_explanation,
        'ibw': ibw_explanation,
        'ideal_weight': ibw_explanation,
        'adjusted_weight': abw_explanation,
        'target_weight': targetweight_explanation,
        
        # BMI和体表面积
        'bsa': bsa_calculator_explaination,
        'bsa_calculator': bsa_calculator_explaination,
        'body_surface_area': bsa_calculator_explaination,
        'body_mass_index': bmi_calculator_explanation,
        
        # 心血管相关
        'map': mean_arterial_pressure_explanation,
        'mean_arterial_pressure': mean_arterial_pressure_explanation,
        'cardiac_risk': compute_cardiac_index_explanation,
        'cardiac_risk_index': compute_cardiac_index_explanation,
        'wells_dvt': compute_wells_criteria_dvt_explanation,
        'wells_pe': calculate_pe_wells_explanation,
        'qt_bazett': bazett_calculator_explanation,
        'qt_calculator_bazett': bazett_calculator_explanation,
        'qt_framingham': framingham_calculator_explanation,
        'qt_calculator_framingham': framingham_calculator_explanation,
        'qt_fredericia': fredericia_calculator_explanation,
        'qt_calculator_fredericia': fredericia_calculator_explanation,
        'qt_hodges': hodges_calculator_explanation,
        'qt_calculator_hodges': hodges_calculator_explanation,
        'qt_rautaharju': rautaharju_calculator_explanation,
        'qt_calculator_rautaharju': rautaharju_calculator_explanation,
        
        # 肾功能
        'creatinine_clearance': generate_cockcroft_gault_explanation,
        'cockcroft_gault': generate_cockcroft_gault_explanation,
        'mdrd': mrdr_gfr_explanation,
        'fena': compute_fena_explanation,
        
        # 肝功能
        'meld': compute_meldna_explanation,
        'meldna': compute_meldna_explanation,
        'meld_na': compute_meldna_explanation,
        'child_pugh': compute_child_pugh_score_explanation,
        'fib4': compute_fib4_explanation,
        'fibrosis4': compute_fib4_explanation,
        
        # 评分系统
        'apache_ii_score': apache_ii_explanation,
        'sofa_score': compute_sofa_explanation,
        'sirs': sirs_criteria_explanation,
        'curb65': curb_65_explanation,
        'curb_65': curb_65_explanation,
        'psi': psi_score_explanation,
        'pneumonia_severity_index': psi_score_explanation,
        'perc': compute_perc_rule_explanation,
        'perc_rule': compute_perc_rule_explanation,
        'glasgow_coma': compute_glasgow_coma_score_explanation,
        'glasgow_bleeding': glasgow_bleeding_score_explanation,
        'centor': compute_centor_score_explanation,
        'centor_score': compute_centor_score_explanation,
        'fever_pain': compute_fever_pain_explanation,
        'feverpain': compute_fever_pain_explanation,
        'charlson': compute_cci_explanation,
        'cci': compute_cci_explanation,
        'charlson_comorbidity_index': compute_cci_explanation,
        'has_bled': compute_has_bled_score_explanation,
        'heart': compute_heart_score_explanation,
        'heart_score': compute_heart_score_explanation,
        'cha2ds2_vasc': generate_cha2ds2_vasc_explanation,
        'caprini': caprini_score_explanation,
        
        # 电解质和酸碱平衡
        'anion_gap': compute_anion_gap_explanation,
        'delta_gap': compute_delta_gap_explanation,
        'albumin_corrected_anion': compute_albumin_corrected_anion_explanation,
        'albumin_corrected_delta_gap': compute_albumin_corrected_delta_gap_explanation,
        'albumin_delta_ratio': compute_albumin_delta_ratio_explanation,
        'sodium_correction': compute_sodium_correction_hyperglycemia_explanation,
        'sch': compute_sodium_correction_hyperglycemia_explanation,
        'calcium_correction': calculate_corrected_calcium_explanation,
        'corrected_calcium': calculate_corrected_calcium_explanation,
        'serum_osmolality': compute_serum_osmolality_explanation,
        'sosm': compute_serum_osmolality_explanation,
        'free_water_deficit': free_water_deficit_explanation,
        'maintenance_fluid': maintenance_fluid_explanation,
        'maintenance_fluid_calc': maintenance_fluid_explanation,
        
        # 药物相关
        'mme': mme_explanation,
        'morphine_milligram_equivalent': mme_explanation,
        
        # 内分泌相关
        'homa_ir': compute_homa_ir_explanation,
        'ldl': compute_ldl_explanation,
        'ldl_calculated': compute_ldl_explanation,
        
        # 妇产科相关
        'conception': add_2_weeks_explanation,
        'conception_date': add_2_weeks_explanation,
        'estimated_conception': add_2_weeks_explanation,
        'edd': add_40_weeks_explanation,
        'estimated_due_date': add_40_weeks_explanation,
        'due_date': add_40_weeks_explanation,
        'gestational_age': compute_gestational_age_explanation
    }
    
    # 添加手动映射
    for tool_name, func in manual_mappings.items():
        all_functions[tool_name] = func  # 移除检查以确保所有映射都被添加
    
    return all_functions

def debug_tool_mappings():
    """调试工具映射，打印所有可用的工具名称"""
    function_map = get_function_mapping_from_modules()
    print(f"可用工具总数: {len(function_map)}")
    print("\n已知工具映射:")
    
    # 按名称排序显示所有工具
    for name in sorted(function_map.keys()):
        print(f"- {name} -> {function_map[name].__name__}")
    
    # 检查特定函数是否存在
    critical_tools = [
        "ckd_epi_2021_creatinine", 
        "steroid_conversion", 
        "conception_date", 
        "mdrd", 
        "creatinine_clearance"
    ]
    
    print("\n关键工具检查:")
    for tool in critical_tools:
        if tool in function_map:
            print(f"✓ {tool} -> {function_map[tool].__name__}")
        else:
            print(f"✗ 缺失: {tool}")
    
    return function_map

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
    if tool_name in ['adjusted_body_weight', 'abw', 'adjusted_weight']:
        # 按照abw_explanation需要的格式组织参数
        if 'weight_value' in args and 'weight_unit' in args:
            formatted_args['weight'] = (args['weight_value'], args['weight_unit'])
        if 'height_value' in args and 'height_unit' in args:
            formatted_args['height'] = (args['height_value'], args['height_unit'])
        if 'sex' in args:
            formatted_args['sex'] = args['sex']
    
    elif tool_name in ['bmi_calculator', 'body_mass_index']:
        # 按照bmi_calculator_explanation需要的格式组织参数
        if 'weight_value' in args and 'weight_unit' in args:
            formatted_args['weight'] = (args['weight_value'], args['weight_unit'])
        elif 'weight' in args:
            if isinstance(args['weight'], list) and len(args['weight']) == 2:
                formatted_args['weight'] = tuple(args['weight'])
            else:
                formatted_args['weight'] = args['weight']
                
        if 'height_value' in args and 'height_unit' in args:
            formatted_args['height'] = (args['height_value'], args['height_unit'])
        elif 'height' in args:
            if isinstance(args['height'], list) and len(args['height']) == 2:
                formatted_args['height'] = tuple(args['height'])
            else:
                formatted_args['height'] = args['height']
    
    elif tool_name in ['ideal_body_weight', 'ibw', 'ideal_weight']:
        # 按照ibw_explanation需要的格式组织参数
        if 'height_value' in args and 'height_unit' in args:
            formatted_args['height'] = (args['height_value'], args['height_unit'])
        if 'sex' in args:
            formatted_args['sex'] = args['sex']
    
    elif tool_name in ['creatinine_clearance', 'cockcroft_gault']:
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
    
    elif tool_name in ['ckd_epi_2021_creatinine', 'ckd_epi_2021', 'ckd_epi']:
        # 按照ckd_epi_2021_explanation需要的格式组织参数
        if 'sex' in args:
            formatted_args['sex'] = args['sex']
        if 'age_value' in args and 'age_unit' in args:
            formatted_args['age'] = (args['age_value'], args['age_unit'])
        
        # 处理肌酐值格式化，修复μmol/L单位问题
        if 'creatinine_value' in args and 'creatinine_unit' in args:
            unit = args['creatinine_unit']
            # 统一单位表示，处理μmol/L的特殊字符问题
            if unit == 'μmol/L' or unit == 'umol/L' or unit == 'µmol/L':
                # 将μmol/L转换为mg/dL，mg/dL是函数内部能识别的单位
                value = args['creatinine_value']
                # μmol/L到mg/dL的转换系数是约0.0113
                formatted_args['creatinine'] = (value / 88.4, 'mg/dL')
            else:
                formatted_args['creatinine'] = (args['creatinine_value'], args['creatinine_unit'])
        
        if 'race' in args:
            formatted_args['race'] = args['race']
    
    elif tool_name in ['steroid_conversion', 'steroid_conversion_calculator']:
        # 按照compute_steroid_conversion_explanation需要的格式组织参数
        # 修复input steroid参数
        if 'source_drug' in args and 'source_route' in args:
            # 统一药物名称的大小写格式
            source_drug = args['source_drug']
            # 特殊处理药物名称中的大小写，所有药物名称需要转换为首字母大写其他小写以匹配conversion_dict的键
            drug_name = f"{source_drug} {args['source_route']}"
            dose_value = None
            dose_unit = 'mg'
            
            if 'source_value' in args and 'source_unit' in args:
                dose_value = args['source_value']
                dose_unit = args['source_unit']
            elif 'source_dose_value' in args and 'source_dose_unit' in args:
                dose_value = args['source_dose_value']
                dose_unit = args['source_dose_unit']
            elif 'dose_value' in args and 'dose_unit' in args:
                dose_value = args['dose_value']
                dose_unit = args['dose_unit']
            elif 'dose' in args:
                if isinstance(args['dose'], (int, float)):
                    dose_value = args['dose']
                elif isinstance(args['dose'], (list, tuple)) and len(args['dose']) == 2:
                    dose_value = args['dose'][0]
                    dose_unit = args['dose'][1]
            if dose_value is not None:
                formatted_args['input steroid'] = [drug_name, dose_value, dose_unit]
        elif 'input_steroid' in args:
            drug_name = args['input_steroid']
            dose_value = args['input_value']
            dose_unit = args['input_unit']
            formatted_args['input steroid'] = [drug_name, dose_value, dose_unit]
                
        # 处理目标药物参数
        if 'target_drug' in args and 'target_route' in args:
            # 统一药物名称的大小写格式
            target_drug = args['target_drug']
            formatted_args['target steroid'] = f"{target_drug} {args['target_route']}"
        elif 'target_steroid' in args:
            formatted_args['target steroid'] = f"{args['target_steroid']}"

        # 如果没有提供足够的参数，尝试使用默认值
        if 'input steroid' not in formatted_args:
            # 设置默认值 - 但这不是一个好的解决方案，应当在更上游处理
            formatted_args['input steroid'] = ["Hydrocortisone PO", 100.0, "mg"]
            print(f"警告: 使用默认值 {formatted_args['input steroid']} 作为输入甾体药物")

        if 'target steroid' not in formatted_args:
            # 设置默认值
            formatted_args['target steroid'] = "PrednisoLONE PO"
            print(f"警告: 使用默认值 {formatted_args['target steroid']} 作为目标甾体药物")
    
    elif tool_name in ['conception_date', 'conception', 'estimated_conception']:
        # 修复conception_date参数
        if 'last_menstrual_period' in args:
            formatted_args['menstrual_date'] = args['last_menstrual_period']
        elif 'lmp' in args:
            formatted_args['menstrual_date'] = args['lmp']
        elif 'menstrual_date' in args:
            formatted_args['menstrual_date'] = args['menstrual_date']
                
        # 添加cycle_length参数，但只在参数中提供时
        if 'cycle_length' in args:
            formatted_args['cycle_length'] = args['cycle_length']
    
    elif tool_name in ['estimated_due_date', 'edd', 'due_date']:
        # 修复estimated_due_date参数 - 实际需要的参数是menstrual_date
        if 'last_menstrual_period' in args:
            formatted_args['menstrual_date'] = args['last_menstrual_period']
        elif 'lmp' in args:
            formatted_args['menstrual_date'] = args['lmp']
        elif 'menstrual_date' in args:
            formatted_args['menstrual_date'] = args['menstrual_date']
        
        # 添加cycle_length参数，但只在参数中提供时
        if 'cycle_length' in args:
            formatted_args['cycle_length'] = args['cycle_length']
    
    elif tool_name in ['target_weight', 'targetweight']:
        # 修复target_weight参数 - 只使用提供的参数
        if 'height_value' in args and 'height_unit' in args:
            formatted_args['height'] = (args['height_value'], args['height_unit'])
        elif 'height' in args and isinstance(args['height'], list) and len(args['height']) == 2:
            formatted_args['height'] = tuple(args['height'])
        
        # 添加 body_mass_index 参数，确保总是提供
        if 'target_bmi' in args:
            formatted_args['body_mass_index'] = (args['target_bmi'], 'kg/m^2')
        elif 'bmi' in args:
            if isinstance(args['bmi'], (list, tuple)) and len(args['bmi']) == 2:
                formatted_args['body_mass_index'] = tuple(args['bmi'])
            else:
                formatted_args['body_mass_index'] = (args['bmi'], 'kg/m^2')
        elif 'body_mass_index' in args:
            if isinstance(args['body_mass_index'], (list, tuple)) and len(args['body_mass_index']) == 2:
                formatted_args['body_mass_index'] = tuple(args['body_mass_index'])
            else:
                formatted_args['body_mass_index'] = (args['body_mass_index'], 'kg/m^2')
        elif 'bmi_value' in args and 'bmi_unit' in args:
            formatted_args['body_mass_index'] = (args['bmi_value'], args['bmi_unit'])

        else:
            # 如果没有提供BMI值，使用健康体重的BMI值
            formatted_args['body_mass_index'] = (22.0, 'kg/m^2')
    
    elif tool_name in ['fibrosis_4', 'fib4', 'fibrosis4']:
        # 修复fibrosis_4参数
        if 'age_value' in args and 'age_unit' in args:
            formatted_args['age'] = (args['age_value'], args['age_unit'])
        if 'alt_value' in args and 'alt_unit' in args:
            formatted_args['alt'] = (args['alt_value'], args['alt_unit'])
        elif 'alt' in args and isinstance(args['alt'], list) and len(args['alt']) == 2:
            formatted_args['alt'] = tuple(args['alt'])
        
        if 'ast_value' in args and 'ast_unit' in args:
            formatted_args['ast'] = (args['ast_value'], args['ast_unit'])
        elif 'ast' in args and isinstance(args['ast'], list) and len(args['ast']) == 2:
            formatted_args['ast'] = tuple(args['ast'])
        
        if 'platelet_count_value' in args and 'platelet_count_unit' in args:
            formatted_args['platelet_count'] = (args['platelet_count_value'], args['platelet_count_unit'])
        elif 'platelet_count' in args and isinstance(args['platelet_count'], list) and len(args['platelet_count']) == 2:
            formatted_args['platelet_count'] = tuple(args['platelet_count'])
        elif 'platelet' in args and isinstance(args['platelet'], list) and len(args['platelet']) == 2:
            formatted_args['platelet_count'] = tuple(args['platelet'])
        elif 'platelet_value' in args and 'platelet_unit' in args:
            formatted_args['platelet_count'] = (args['platelet_value'], args['platelet_unit'])
    
    elif tool_name in ['qt_calculator_fredericia', 'qt_fredericia']:
        # 修复QT计算器参数 - 修复qt_interval参数
        if 'qt_value' in args and 'qt_unit' in args:
            formatted_args['qt_interval'] = (args['qt_value'], args['qt_unit'])
        elif 'qt' in args and isinstance(args['qt'], list) and len(args['qt']) == 2:
            formatted_args['qt_interval'] = tuple(args['qt'])
        elif 'qt_interval_value' in args and 'qt_interval_unit' in args:
            formatted_args['qt_interval'] = (args['qt_interval_value'], args['qt_interval_unit'])
        
        if 'heart_rate_value' in args and 'heart_rate_unit' in args:
            formatted_args['heart_rate'] = (args['heart_rate_value'], args['heart_rate_unit'])
        elif 'heart_rate' in args and isinstance(args['heart_rate'], list) and len(args['heart_rate']) == 2:
            formatted_args['heart_rate'] = tuple(args['heart_rate'])
    
    elif tool_name in ['centor_score', 'centor']:
        # 修复centor_score参数
        if 'age_value' in args and 'age_unit' in args:
            formatted_args['age'] = (args['age_value'], args['age_unit'])
        elif 'age' in args and isinstance(args['age'], list) and len(args['age']) == 2:
            formatted_args['age'] = tuple(args['age'])
        elif 'age' in args and not isinstance(args['age'], (list, tuple)):
            formatted_args['age'] = (args['age'], 'years')
        
        # 确保温度参数存在，从问题文本中解析或提供默认值
        if 'temperature_value' in args and 'temperature_unit' in args:
            formatted_args['temperature'] = (args['temperature_value'], args['temperature_unit'])
        elif 'temperature' in args and isinstance(args['temperature'], list) and len(args['temperature']) == 2:
            formatted_args['temperature'] = tuple(args['temperature'])
        elif 'temperature' in args and not isinstance(args['temperature'], (list, tuple)):
            formatted_args['temperature'] = (args['temperature'], '°C')
        else:
            # 如果没有提供温度，使用默认值 37°C (98.6°F) - 正常体温
            formatted_args['temperature'] = (37.0, '°C')
        
        for param in ['exudate_swelling_tonsils', 'tender_lymph_nodes', 'cough_absent']:
            if param in args:
                formatted_args[param] = args[param]
    
    elif tool_name in ['sirs_criteria', 'sirs']:
        # 修复sirs_criteria参数
        if 'temperature_value' in args and 'temperature_unit' in args:
            formatted_args['temperature'] = (args['temperature_value'], args['temperature_unit'])
        elif 'temperature' in args and isinstance(args['temperature'], list) and len(args['temperature']) == 2:
            formatted_args['temperature'] = tuple(args['temperature'])
        elif 'temperature' in args and not isinstance(args['temperature'], (list, tuple)):
            formatted_args['temperature'] = (args['temperature'], '°C')
        
        if 'heart_rate_value' in args and 'heart_rate_unit' in args:
            formatted_args['heart_rate'] = (args['heart_rate_value'], args['heart_rate_unit'])
        elif 'heart_rate' in args and isinstance(args['heart_rate'], list) and len(args['heart_rate']) == 2:
            formatted_args['heart_rate'] = tuple(args['heart_rate'])
        elif 'heart_rate' in args and not isinstance(args['heart_rate'], (list, tuple)):
            formatted_args['heart_rate'] = (args['heart_rate'], 'beats/min')
        
        if 'wbc_value' in args and 'wbc_unit' in args:
            formatted_args['wbc'] = (args['wbc_value'], args['wbc_unit'])
        elif 'wbc' in args and isinstance(args['wbc'], list) and len(args['wbc']) == 2:
            formatted_args['wbc'] = tuple(args['wbc'])
        elif 'wbc' in args and not isinstance(args['wbc'], (list, tuple)):
            formatted_args['wbc'] = (args['wbc'], 'cells/µL')
        
        # 确保respiratory_rate有正确的格式
        if 'respiratory_rate_value' in args and 'respiratory_rate_unit' in args:
            formatted_args['respiratory_rate'] = (args['respiratory_rate_value'], args['respiratory_rate_unit'])
        elif 'respiratory_rate' in args and isinstance(args['respiratory_rate'], list) and len(args['respiratory_rate']) == 2:
            formatted_args['respiratory_rate'] = tuple(args['respiratory_rate'])
        elif 'respiratory_rate' in args and not isinstance(args['respiratory_rate'], (list, tuple)):
            formatted_args['respiratory_rate'] = (args['respiratory_rate'], 'breaths/min')
        
        # 确保paco2有正确的格式
        if 'paco2_value' in args and 'paco2_unit' in args:
            formatted_args['paco2'] = (args['paco2_value'], args['paco2_unit'])
        elif 'paco2' in args and isinstance(args['paco2'], list) and len(args['paco2']) == 2:
            formatted_args['paco2'] = tuple(args['paco2'])
        elif 'paco2' in args and not isinstance(args['paco2'], (list, tuple)):
            formatted_args['paco2'] = (args['paco2'], 'mmHg')
    
    elif tool_name in ['ldl_calculated', 'ldl']:
        # 修复ldl_calculated参数 - 确保使用total_cholestrol作为键名
        # 处理总胆固醇参数 - 确保键名正确性
        if 'cholesterol_value' in args and 'cholesterol_unit' in args:
            formatted_args['total_cholestrol'] = (args['cholesterol_value'], args['cholesterol_unit'])
        elif 'total_cholesterol_value' in args and 'total_cholesterol_unit' in args:
            formatted_args['total_cholestrol'] = (args['total_cholesterol_value'], args['total_cholesterol_unit'])
        elif 'total_cholestrol_value' in args and 'total_cholestrol_unit' in args:
            formatted_args['total_cholestrol'] = (args['total_cholestrol_value'], args['total_cholestrol_unit'])
        elif 'cholesterol' in args and isinstance(args['cholesterol'], list) and len(args['cholesterol']) == 2:
            formatted_args['total_cholestrol'] = tuple(args['cholesterol'])
        elif 'total_cholesterol' in args and isinstance(args['total_cholesterol'], list) and len(args['total_cholesterol']) == 2:
            formatted_args['total_cholestrol'] = tuple(args['total_cholesterol'])
        # 尝试查找其他可能的键名
        elif 'tc_value' in args and 'tc_unit' in args:
            formatted_args['total_cholestrol'] = (args['tc_value'], args['tc_unit'])
        elif 'tc' in args and isinstance(args['tc'], list) and len(args['tc']) == 2:
            formatted_args['total_cholestrol'] = tuple(args['tc'])
            
        # 当所有方法都找不到时，使用默认值
        if 'total_cholestrol' not in formatted_args:
            # 使用默认的正常胆固醇水平数值
            formatted_args['total_cholestrol'] = (200.0, 'mg/dL')
        
        # 处理HDL胆固醇参数
        if 'hdl_value' in args and 'hdl_unit' in args:
            formatted_args['hdl_cholestrol'] = (args['hdl_value'], args['hdl_unit'])
        elif 'hdl_cholesterol_value' in args and 'hdl_cholesterol_unit' in args:
            formatted_args['hdl_cholestrol'] = (args['hdl_cholesterol_value'], args['hdl_cholesterol_unit'])
        elif 'hdl_cholestrol_value' in args and 'hdl_cholestrol_unit' in args:
            formatted_args['hdl_cholestrol'] = (args['hdl_cholestrol_value'], args['hdl_cholestrol_unit'])
        elif 'hdl' in args and isinstance(args['hdl'], list) and len(args['hdl']) == 2:
            formatted_args['hdl_cholestrol'] = tuple(args['hdl'])
        elif 'hdl_cholesterol' in args and isinstance(args['hdl_cholesterol'], list) and len(args['hdl_cholesterol']) == 2:
            formatted_args['hdl_cholestrol'] = tuple(args['hdl_cholesterol'])
            
        # 当所有方法都找不到时，使用默认值
        if 'hdl_cholestrol' not in formatted_args:
            # 使用默认的HDL胆固醇水平数值
            formatted_args['hdl_cholestrol'] = (50.0, 'mg/dL')
        
        # 处理甘油三酯参数
        if 'triglycerides_value' in args and 'triglycerides_unit' in args:
            formatted_args['triglycerides'] = (args['triglycerides_value'], args['triglycerides_unit'])
        elif 'triglycerides' in args and isinstance(args['triglycerides'], list) and len(args['triglycerides']) == 2:
            formatted_args['triglycerides'] = tuple(args['triglycerides'])
        elif 'triglyceride' in args and isinstance(args['triglyceride'], list) and len(args['triglyceride']) == 2:
            formatted_args['triglycerides'] = tuple(args['triglyceride'])
        elif 'triglyceride_value' in args and 'triglyceride_unit' in args:
            formatted_args['triglycerides'] = (args['triglyceride_value'], args['triglyceride_unit'])
        elif 'tg_value' in args and 'tg_unit' in args:
            formatted_args['triglycerides'] = (args['tg_value'], args['tg_unit'])
        elif 'tg' in args and isinstance(args['tg'], list) and len(args['tg']) == 2:
            formatted_args['triglycerides'] = tuple(args['tg'])
            
        # 当所有方法都找不到时，使用默认值
        if 'triglycerides' not in formatted_args:
            # 使用默认的三酸甘油酯水平数值
            formatted_args['triglycerides'] = (150.0, 'mg/dL')
    
    elif tool_name in ['mme', 'morphine_milligram_equivalent']:
        # 修复mme参数，特别注意药物名称的大小写
        # 药物名称的特殊大小写映射
        drug_name_case_map = {
            "fentanyl": "FentaNYL",
            "fentanyl buccal": "FentaNYL buccal",
            "fentanyl patch": "FentaNYL patch",
            "hydrocodone": "HYDROcodone",
            "hydromorphone": "HYDROmorphone",
            "oxycodone": "OxyCODONE",
            "oxymorphone": "OxyMORphone",
            "tramadol": "TraMADol",
            "codeine": "Codeine", 
            "methadone": "Methadone",
            "morphine": "Morphine",
            "tapentadol": "Tapentadol",
            "buprenorphine": "Buprenorphine"
        }
        
        # 检查原始参数中是否已经有正确格式的参数
        drug_keys = [key for key in args.keys() if ('dose' in key.lower() and ' dose' in key.lower()) or ('per day' in key.lower() and ' per day' in key.lower())]
        
        # 如果已经存在标准格式的参数，直接使用但确保药物名称大小写正确
        if any(' Dose' in key for key in drug_keys) and any(' Dose Per Day' in key for key in drug_keys):
            for key in drug_keys:
                if ' Dose' in key:
                    # 提取药物名称
                    drug_name = key.split(' Dose')[0]
                    # 检查并纠正药物名称大小写
                    drug_name_lower = drug_name.lower()
                    if drug_name_lower in drug_name_case_map:
                        corrected_drug_name = drug_name_case_map[drug_name_lower]
                        corrected_key = f"{corrected_drug_name} Dose"
                        dose_per_day_key = f"{corrected_drug_name} Dose Per Day"
                        
                        # 处理剂量值
                        if isinstance(args[key], (list, tuple)) and len(args[key]) == 2:
                            formatted_args[corrected_key] = tuple(args[key])
                        else:
                            # 尝试找到单位
                            if key + '_unit' in args:
                                formatted_args[corrected_key] = (args[key], args[key + '_unit'])
                            else:
                                formatted_args[corrected_key] = (args[key], 'mg')
                        
                        # 处理每日剂量
                        day_key = f"{drug_name} Dose Per Day"
                        if day_key in args:
                            if isinstance(args[day_key], (list, tuple)) and len(args[day_key]) == 2:
                                formatted_args[dose_per_day_key] = tuple(args[day_key])
                            else:
                                formatted_args[dose_per_day_key] = (args[day_key], 'per day')
        # 处理其他格式的参数
        else:
            # 如果有明确的drug参数
            if 'drug' in args:
                drug_name = args['drug']
                # 处理特殊情况：药物名称中的特殊大小写
                drug_name_lower = drug_name.lower()
                if drug_name_lower in drug_name_case_map:
                    drug_name = drug_name_case_map[drug_name_lower]
                
                # 查找对应的剂量信息
                if 'dose' in args:
                    if isinstance(args['dose'], (list, tuple)) and len(args['dose']) == 2:
                        formatted_args[drug_name + ' Dose'] = tuple(args['dose'])
                    elif 'dose_unit' in args:
                        formatted_args[drug_name + ' Dose'] = (args['dose'], args['dose_unit'])
                    else:
                        formatted_args[drug_name + ' Dose'] = (args['dose'], 'mg')
                
                # 查找对应的频率信息
                if 'frequency' in args:
                    if isinstance(args['frequency'], (int, float)):
                        formatted_args[drug_name + ' Dose Per Day'] = (args['frequency'], 'per day')
                    else:
                        formatted_args[drug_name + ' Dose Per Day'] = args['frequency']
                elif 'per_day' in args:
                    if isinstance(args['per_day'], (int, float)):
                        formatted_args[drug_name + ' Dose Per Day'] = (args['per_day'], 'per day')
                    else:
                        formatted_args[drug_name + ' Dose Per Day'] = args['per_day']
                else:
                    formatted_args[drug_name + ' Dose Per Day'] = (1, 'per day')  # 默认每天一次
    
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
    # 针对MME错误调用steroid_conversion的问题进行修复
    if "calc_name" in args and args["calc_name"] == "Morphine Milligram Equivalents (MME) Calculator":
        tool_name = "mme"  # 强制使用正确的工具
    
    # 处理特定的工具名变体 
    if tool_name == "qt_calculator_bazett" and tool_name not in function_map and "qt_bazett" in function_map:
        tool_name = "qt_bazett"
    elif tool_name == "qt_calculator_framingham" and tool_name not in function_map and "qt_framingham" in function_map:
        tool_name = "qt_framingham"
    elif tool_name == "qt_calculator_fredericia" and tool_name not in function_map and "qt_fredericia" in function_map:
        tool_name = "qt_fredericia"
    elif tool_name == "qt_calculator_hodges" and tool_name not in function_map and "qt_hodges" in function_map:
        tool_name = "qt_hodges"
    elif tool_name == "qt_calculator_rautaharju" and tool_name not in function_map and "qt_rautaharju" in function_map:
        tool_name = "qt_rautaharju"
    elif tool_name == "heart_score" and tool_name not in function_map and "heart" in function_map:
        tool_name = "heart"
    elif tool_name == "centor_score" and tool_name not in function_map and "centor" in function_map:
        tool_name = "centor"
    elif tool_name == "perc_rule" and tool_name not in function_map and "perc" in function_map:
        tool_name = "perc"
    
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
            return f"# 未找到工具: {tool_name}\n# 可能需要更新工具映射"
    
    function = function_map[tool_name]
    module_name = function.__module__
    function_name = function.__name__
    
    # 构建导入语句
    import_stmt = f"from {module_name} import {function_name}"
    
    # 根据工具类型格式化参数
    formatted_args = format_args_for_function(tool_name, args)
    if tool_name == "steroid_conversion":
        print(formatted_args)
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
# reall for parms
input_variables = {args_str}

# call function
result = {function_name}(input_variables)

# return result
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
          
                    
                    # 特殊处理某些工具名
                    if tool_name == "ckd_epi_2021_creatinine" and tool_name not in function_map:
                        tool_name = "ckd_epi_2021"  # 尝试使用另一个名称
                    
                    # 生成代码
                    code = generate_direct_code(tool_name, args, function_map)
                    
                    # 如果未找到工具，记录下来
                    if code.startswith("# 未找到工具"):
                        missing_tools.add(tool_name)
                    
                    all_codes.append(f"# {tool_name} function call:\n{code}\n")
            
            # 拼接所有代码
            if all_codes:
                # 创建新的rationale项
                new_rationale = all_codes
                item["content"] = item["rationale"][-1]["content"]
                # 替换原始的rationale
                item["rationale"] = new_rationale
    
    # 如果有未找到的工具，输出警告
    if missing_tools:
        print(f"警告: 以下工具未找到: {', '.join(missing_tools)}")
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    return output_file

def get_tool_name_from_question(question, args=None):
    """
    从问题或输入参数中提取工具名称
    
    Args:
        question: 问题文本
        args: 可选的参数字典
    
    Returns:
        str: 识别的工具名
    """
    if args and "calc_name" in args:
        # 首先查看是否有明确指定的计算名称
        calc_name = args["calc_name"]
        if "Steroid Conversion" in calc_name:
            return "steroid_conversion"
        elif "Morphine Milligram Equivalents" in calc_name or "MME" in calc_name:
            return "mme"
        elif "LDL" in calc_name:
            return "ldl_calculated"
        # 可以添加更多映射...
    
    # 工具名称映射表
    tool_patterns = {
        r'steroid\s+conversion|equivalent\s+dosage|convert.*steroid': 'steroid_conversion',
        r'mme|morphine\s+milligram\s+equivalent': 'mme',
        r'ldl|low\s+density\s+lipoprotein|cholesterol': 'ldl_calculated',
        r'creatinine\s+clearance|cockcroft\s+gault': 'creatinine_clearance',
        r'ckd\s+epi|egfr': 'ckd_epi_2021_creatinine',
        r'conception\s+date': 'conception_date',
        r'due\s+date|edd': 'estimated_due_date',
        r'target\s+weight': 'target_weight',
        r'fibrosis\s+4|fib\s*-?\s*4': 'fibrosis_4',
        r'qt\s+calculator.*fredericia': 'qt_calculator_fredericia',
        r'qt\s+calculator.*bazett': 'qt_calculator_bazett',
        r'qt\s+calculator.*framingham': 'qt_calculator_framingham',
        r'centor\s+score': 'centor_score',
        r'sirs\s+criteria': 'sirs_criteria',
        # 可以添加更多工具的识别模式
    }
    
    for pattern, tool_name in tool_patterns.items():
        if re.search(pattern, question, re.IGNORECASE):
            return tool_name
    
    # 未识别到工具名
    return None

def execute_rationale_code(rationale, question, rationale_index=None):
    """
    执行医学推理代码，处理各种转换和调用
    
    Args:
        rationale: rationale文本
        question: 问题文本
        rationale_index: 使用的rationale索引
    
    Returns:
        tuple: (结果, 错误信息)
    """
    # 获取工具名到函数的映射
    function_mapping = get_function_mapping_from_modules()
    
    # 解析rationale中的参数
    args = parse_args_from_rationale(rationale, None)
    
    # 获取问题中提到的工具名
    tool_name = get_tool_name_from_question(question, args)
    if not tool_name:
        return None, "无法从问题中识别医学计算工具"
    
    # 修复工具名 - 特殊处理MME被错误地识别为steroid_conversion的情况
    if "calc_name" in args and "Morphine Milligram Equivalents" in args["calc_name"]:
        tool_name = "mme"  # 强制使用正确的工具
    
    # 如果rationale_index存在，从rationale中解析工具名
    if rationale_index is not None:
        code_comments = find_all_code_sections(rationale, tool_name=None)
        if code_comments and 0 <= rationale_index < len(code_comments):
            code_comment = code_comments[rationale_index]
            lines = code_comment.strip().split("\n")
            
            # 确保代码段开始于工具函数调用注释
            if lines and "function call" in lines[0]:
                actual_tool_name = lines[0].split("function call:")[0].replace("#", "").strip()
                if actual_tool_name and actual_tool_name != tool_name:
                    # 特别处理MME和steroid_conversion的冲突
                    if not (actual_tool_name == "steroid_conversion" and "calc_name" in args and "MME" in args["calc_name"]):
                        # 如果识别出的工具名与注释中的工具名不匹配，优先使用注释中的
                        tool_name = actual_tool_name
    
    # 格式化参数以适应函数需求
    formatted_args = format_args_for_function(tool_name, args)
    
    # 调用相应的函数
    if tool_name in function_mapping:
        function = function_mapping[tool_name]
        try:
            result = function(formatted_args)
            
            # 返回结果
            if isinstance(result, dict) and "Answer" in result:
                return result["Answer"], None
            return result, None
        except Exception as e:
            import traceback
            return None, f"执行{tool_name}函数时出错: {str(e)}\n{traceback.format_exc()}"
    else:
        return None, f"未找到名为'{tool_name}'的医学计算工具函数"

def main():
    """命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='将JSON文件中的rationale替换为函数调用代码')
    # 设置默认输入路径
    default_input = "output_filtered.json"
    parser.add_argument('input', 
                        help='输入JSON文件路径', 
                        nargs='?',  # 使参数可选
                        default=default_input)  
    # 设置默认输出路径
    default_output = "output_code_replaced.json"
    parser.add_argument('-o', '--output', 
                        help='输出JSON文件路径',
                        default=default_output)
    parser.add_argument('-d', '--debug', 
                        action='store_true', 
                        help='调试模式，显示所有工具映射')
    
    args = parser.parse_args()
    
    # 调试模式
    if args.debug:
        debug_tool_mappings()
        return 0
    
    if not os.path.isfile(args.input):
        print(f"错误: 文件 '{args.input}' 不存在")
        return 1
    
    # 替换rationale
    output_file = replace_rationale_with_code_in_json(args.input, args.output)
    print(f"已将rationale替换为代码，输出文件: {output_file}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())