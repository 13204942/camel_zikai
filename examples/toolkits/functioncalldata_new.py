# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

import json
import os
import argparse
import tqdm
from typing import Dict, List, Any
import concurrent.futures
import time

from camel.agents import ChatAgent
from camel.configs import DeepSeekConfig
from camel.models import ModelFactory
from camel.toolkits import MedCalcToolkit
from camel.types import ModelPlatformType, ModelType


# 创建自定义JSON编码器处理ToolCallingRecord对象
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # 检查对象是否有to_dict方法
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        # 检查对象是否有__dict__属性，如果有则返回序列化版本
        elif hasattr(obj, '__dict__'):
            return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        # 处理其他无法序列化的类型
        try:
            return str(obj)
        except:
            return f"不可序列化对象: {type(obj).__name__}"


def process_single_item(item, tools, sys_msg, model_config_dict, max_retries=3):
    """
    处理单个数据项并支持重试机制
    
    Args:
        item: 要处理的数据项
        tools: 可用的工具列表
        sys_msg: 系统消息
        model_config_dict: 模型配置字典
        max_retries: 最大重试次数
    
    Returns:
        处理后的结果字典，如果全部重试失败则返回None
    """
    retries = 0
    while retries < max_retries:
        try:
            # 创建模型
            model = ModelFactory.create(
                model_platform=ModelPlatformType.OPENAI,
                model_type=ModelType.GPT_4O,
                model_config_dict=model_config_dict,
            )
            
            # 设置代理
            camel_agent = ChatAgent(
                system_message=sys_msg,
                model=model,
                tools=tools,
            )
            
            # 从数据元素中提取question作为usr_msg
            usr_msg = item.get("question", "")
            if not usr_msg:
                print("警告: 数据元素没有question字段")
                return None
            
            # 获取响应信息
            response = camel_agent.step(usr_msg)
            
            # 提取并转换tool_calls以确保可序列化
            tool_calls = response.info.get("tool_calls", [])
            serializable_tool_calls = []
            for call in tool_calls:
                if hasattr(call, 'to_dict'):
                    serializable_tool_calls.append(call.to_dict())
                elif hasattr(call, '__dict__'):
                    serializable_tool_calls.append({k: v for k, v in call.__dict__.items() if not k.startswith('_')})
                else:
                    # 如果无法序列化，至少保留基本信息
                    serializable_tool_calls.append(str(call))
            
            # 将response.msgs[0].content作为新的元素添加到列表中
            if response.msgs and len(response.msgs) > 0:
                serializable_tool_calls.append({"content": response.msgs[0].content})
            
            # 创建新的数据元素
            result = {
                "usr_msg": usr_msg,
                "rationale": serializable_tool_calls,
                "final_answer": item.get("final_answer", ""),
                "metadata": item.get("metadata", {})
            }
            
            return result
            
        except Exception as e:
            retries += 1
            if retries < max_retries:
                print(f"处理数据时出错 (尝试 {retries}/{max_retries}): {e}")
                time.sleep(1)  # 在重试前短暂等待
            else:
                print(f"处理数据失败，达到最大重试次数 ({max_retries}): {e}")
                return None


def process_json_data(input_file: str, output_file: str, limit: int = None, workers: int = 4) -> None:
    """
    从JSON文件中提取question作为usr_msg，并获取对应的tool_calls作为rationale
    支持并行处理和失败重试

    Args:
        input_file: 输入JSON文件路径
        output_file: 输出JSON文件路径
        limit: 处理的最大项目数，None表示处理所有项目
        workers: 并行工作进程数
    """
    # 定义系统消息
    sys_msg = """You are a helpful assistant.please put the final_answer in the \\boxed{}"""

    # 设置模型配置
    tools = MedCalcToolkit().get_tools()
    
    # model_config_dict = ChatGPTConfig(temperature=0.0).as_dict()
    model_config_dict = DeepSeekConfig(temperature=0.0).as_dict()
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 限制处理数量
    if limit is not None:
        data = data[:limit]
    
    results = []
    
    # 使用线程池并行处理数据
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        # 提交所有任务
        future_to_item = {
            executor.submit(process_single_item, item, tools, sys_msg, model_config_dict): item 
            for item in data
        }
        
        # 使用tqdm显示进度
        for future in tqdm.tqdm(concurrent.futures.as_completed(future_to_item), 
                               total=len(data), 
                               desc="处理数据"):
            result = future.result()
            if result:
                results.append(result)
    
    # 写入结果到JSON文件，使用自定义编码器
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4, cls=CustomJSONEncoder)
    
    print(f"已成功处理 {len(results)}/{len(data)} 个项目。结果保存到 {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="处理JSON文件并生成带有工具调用的结果")
    parser.add_argument("--input", "-i", type=str, required=True, help="输入JSON文件路径")
    parser.add_argument("--output", "-o", type=str, required=True, help="输出JSON文件路径")
    parser.add_argument("--limit", "-l", type=int, default=None, help="处理的最大项目数")
    parser.add_argument("--workers", "-w", type=int, default=4, help="并行工作进程数")
    
    args = parser.parse_args()
    
    process_json_data(args.input, args.output, args.limit, args.workers) 