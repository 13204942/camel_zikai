import json

def delete_non_args_rationale(json_file):
    """删除整个不包含args的数据项"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 过滤整个不包含args字段的数据项
    filtered_data = []
    for item in data:
        # 检查是否至少有一个rationale元素包含args
        has_args = False
        if "rationale" in item and isinstance(item["rationale"], list):
            for r in item["rationale"]:
                if isinstance(r, dict) and "args" in r:
                    has_args = True
                    break
        
        # 如果有包含args的rationale，则保留该数据项
        if has_args:
            filtered_data.append(item)

    # 保存修改后的数据
    output_file = "output_filtered.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)

    print(f"已删除不包含args的数据项，结果保存至: {output_file}")
    print(f"原始数据项数量: {len(data)}, 过滤后数据项数量: {len(filtered_data)}")


if __name__ == "__main__":
    delete_non_args_rationale("output.json")

