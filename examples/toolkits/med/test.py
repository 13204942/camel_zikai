# bmi_calculator 函数调用
from camel.toolkits.medcalc_bench.bmi_calculator import bmi_calculator_explanation

# 准备输入参数
input_variables = {
    "weight": (70, 'kg'),      # 体重 (公斤)
    "height": (175, 'cm'),     # 身高 (厘米)
    "sex": "Male"              # 性别
}

# 调用函数
result = bmi_calculator_explanation(input_variables)

# 打印结果
print(result)


# ideal_body_weight 函数调用
from camel.toolkits.medcalc_bench.ideal_body_weight import ibw_explanation

# 准备输入参数
input_variables = {
    "height": (176, 'cm'),     # 身高 (厘米)
    "sex": 'Male'              # 性别
}

# 调用函数
result = ibw_explanation(input_variables)

# 打印结果
print(result)


# creatinine_clearance 函数调用
from camel.toolkits.medcalc_bench.creatinine_clearance import generate_cockcroft_gault_explanation

# 准备输入参数
input_variables = {
    "weight": (68, 'kg'),      # 体重 (公斤)
    "height": (176, 'cm'),     # 身高 (厘米)
    "sex": 'Male',             # 性别
    "creatinine": (1.0, 'mg/dL'),  # 肌酐值 (mg/dL)
    "age": (56, 'years')       # 年龄 (岁)
}

# 调用函数
result = generate_cockcroft_gault_explanation(input_variables)

# 打印结果
print(result)