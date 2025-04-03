#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
该脚本用于从JSON文件中提取rationale部分并执行
"""

import json
import os
import sys

def extract_and_run_rationale(file_path):
    """
    从JSON文件中提取rationale部分并执行
    
    Args:
        file_path: JSON文件路径
    """
    print("正在读取文件:", file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取文件失败: {e}")
        return
    
    for i, item in enumerate(data):
        print(f"\n========== 案例 {i+1} ==========")
        rationale = item.get('rationale', '')
        if not rationale:
            print("找不到rationale部分")
            continue
        
        print("提取到的rationale:")
        print(rationale[:100] + "..." if len(rationale) > 100 else rationale)
        
        # 将rationale保存到临时文件
        temp_file = f"temp_rationale_{i}.py"
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(rationale)
            
            print(f"执行rationale...")
            # 执行临时文件
            os.system(f"python {temp_file}")
            
        except Exception as e:
            print(f"执行失败: {e}")
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        print(f"最终答案: {item.get('final_answer', '未找到')}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = "rationaledata_standard_code.json"
    
    extract_and_run_rationale(file_path) 