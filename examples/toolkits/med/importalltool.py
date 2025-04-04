import os
import importlib
import inspect

# 获取medcalc_bench包的路径
import camel.toolkits.medcalc_bench

# 获取medcalc_bench目录
medcalc_bench_dir = os.path.dirname(camel.toolkits.medcalc_bench.__file__)

# 生成导入语句
import_statements = []

# 遍历medcalc_bench目录中的所有.py文件
for filename in sorted(os.listdir(medcalc_bench_dir)):
    # 排除以下文件和目录
    if (
        filename.endswith(".py") 
        and not filename.startswith("__") 
        and filename != "utils" 
        and os.path.isfile(os.path.join(medcalc_bench_dir, filename))
    ):
        # 获取模块名（去掉.py后缀）
        module_name = filename[:-3]
        
        # 导入模块
        module_path = f"camel.toolkits.medcalc_bench.{module_name}"
        try:
            module = importlib.import_module(module_path)
            
            # 查找模块中的所有函数
            functions = [
                name for name, obj in inspect.getmembers(module) 
                if inspect.isfunction(obj) and not name.startswith("_")
            ]
            
            # 为每个函数生成导入语句
            for func_name in functions:
                import_statements.append(f"from {module_path} import {func_name}")
        except Exception as e:
            print(f"Error importing {module_path}: {e}")

# 按字母顺序排序导入语句
import_statements.sort()

# 打印导入语句到当前文件
with open(__file__, "w") as f:
    f.write("\n".join(import_statements) + "\n")

# 执行后删除这段代码本身（将其替换为导入语句）
if __name__ == "__main__":
    print(f"Successfully imported {len(import_statements)} functions from medcalc_bench package")

