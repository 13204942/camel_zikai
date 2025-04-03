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
import os

from camel.agents import RepoAgent
from camel.embeddings import OpenAIEmbedding
from camel.retrievers import VectorRetriever
from camel.storages.vectordb_storages import QdrantStorage

vector_storage = QdrantStorage(
    vector_dim=OpenAIEmbedding().get_output_dim(),
    collection_name="tmp_collection",
    path="local_data/",
)

vr = VectorRetriever(embedding_model=OpenAIEmbedding(), storage=vector_storage)

repo_agent = RepoAgent(
    system_message="你可以根据用户输入的医学问题，查询相应的可以解决这个问题的工具代码来解决这个医学问题，最后返回给用户一个可以解决这个问题的工具代码在\\boxed{}里面",
    repo_paths=["https://github.com/zjrwtx/test_medcalculator"],
    chunk_size=8192,
    top_k=5,
    similarity=0.3,
    vector_retriever=vr,
    github_auth_token=os.getenv("GITHUB_AUTH_TOKEN"),

)
input="""

In 2008, a 59-year-old Japanese woman was admitted for evaluation of renal disease. RA had been diagnosed at another hospital in 1972 when she presented with bilateral arthropathy of the hands, knees, ankles, and feet. Treatment was started with a combination of a gold preparation and nonsteroidal anti-inflammatory drugs (NSAIDs), but was not been effective. Prednisolone (PSL; 15 mg daily) and bucillamine (BUC; 200 mg daily) were started in 1987, but her disease remained active. Methotrexate (MTX; 5 mg daily) was started in 1995 but was discontinued because of nausea. In 2002, urinary protein was found to be positive by a dipstick urine test, and BUC was stopped. Then treatment was continued with PSL (5 mg/day) and loxoprofen (50 mg/day). However, urinary protein excretion increased in 2007, and serum creatinine (Cre) was elevated to 1.96 mg/dL.\nOn admission, the patient was 154.2 cm tall and weighed 44.0 kg, with a blood pressure of 128/60 mmHg and temperature of 36.4 °C. Physical examination did not reveal any abnormalities of the heart and lungs. The joints of her hands, knees, ankles, and feet showed bilateral swelling and deformity. In addition, the lower extremities were edematous. Her cervical spine was unstable, with flexion causing numbness in the upper limbs.\nLaboratory findings were as follows: serum Cre was 4.2 mg/dL, the estimated glomerular filtration rate (eGFR) was 9.3 mL/min/1.73m3, C-reactive protein (CRP) was 0.9 mg/dL, and SAA was 43.2. In addition, rheumatoid factor (RF) was positive at 59 U/mL (normal: < 10), and cyclic citrullinated peptide (CCP) antibodies were positive at 218.5 (normal < 4.5). 24-hour urinary protein excretion was 6.5 g, and the urine sediment contained 1 – 5 red cells per high-power field (HPF). The disease activity score (DAS)-CRP was 7.1. Radiographs showed deformation of the finger and foot joints as well as atlantoaxial joint subluxation. Renal biopsy was performed for evaluation of her kidney disease.\nRenal biopsy\nLight microscopic examination of a biopsy specimen containing 4 glomeruli revealed global sclerosis in all 4. There was severe tubular atrophy, and tubulointerstitial fibrosis occupied ~ 95% of the entire renal cortex. All 4 glomeruli contained multinodular structures of amorphous material with a PAM-positive border. This material was positive for Congo-red and amyloid A, but was negative for κ and λ chains, β-2 microglobulin, and transthyretin (). Electron microscopy showed randomly arranged fibrils measuring 8 – 12 nm in diameter corresponding to the amyloid deposits (f). AA amyloidosis was diagnosed from these findings. In addition to the glomeruli, amyloid deposits were mainly observed in the interlobular artery walls and tubulointerstitium (e). Endoscopic biopsy of the stomach, duodenum, and colon revealed AA-positive deposits in the small arteries and tissues of the submucosal layer (a).\nClinical course\nPSL was discontinued, and administration of a soluble tumor necrosis factor (TNF) receptor inhibitor (etanercept; 25 mg every 2 weeks) was started in May 2008, but it was not effective. By September 2008, Cre was increased to 6.0 mg/dL. She underwent surgery to prepare an arteriovenous fistula for hemodialysis. Etanercept was discontinued, and a humanized anti-interleukin-6 receptor antibody (tocilizumab; 8 mg/kg = 360 mg/month) was started in February 2009. After 3 months, her CRP decreased to 0.0 mg/dL, and the DAS28-CRP sore was 2.12. After 2 years of tocilizumab therapy, urinary protein excretion was decreased to 1.1 g/day, and Cre was 4.0 mg/dL. Subsequently, Cre remained in the range of 4.5 – 5.0 mg/dL until December 2017. While Cre increased to 7.1 mg/dL after initiation of treatment with denosumab (a human monoclonal antibody that binds to receptor activator of NFκB ligand) for osteoporosis in October 2018, it remained at 7.0 mg/dL in June 2019 ().\nGastroduodenal biopsy was performed in May 2013 and May 2017. On both occasions, no amyloid deposits were detected in the submucosal blood vessels (b). What is the patient's Creatinine Clearance using the Cockroft-Gault Equation in terms of mL/min? You should use the patient's adjusted body weight in kg instead of the patient's actual body weight if the patient is overweight or obese based on their BMI. If the patient's BMI's normal, set their adjusted body weight to the minimum of the ideal body and actual weight. If the patient is underweight, please set their adjusted body weight to their actual body weight.


"""
response = repo_agent.step(input)

print(response.msgs[0].content)

"""
Based on your request to learn how to use a `ChatAgent` in CAMEL, I will 
explain key aspects of the implementation provided in the source code 
"retrieved" and guide you on how to create and utilize the `ChatAgent` 
effectively.

### Overview of `ChatAgent`

`ChatAgent` is designed to interact with language models, supporting 
conversation management, memory, and tool integration. 
It can perform tasks like handling user queries, responding with structured 
data, and performing computations.

### Basic Usage of `ChatAgent`

Here's a step-by-step guide on how to implement and utilize a `ChatAgent`:

1. **Import Necessary Modules**:
   Ensure to import the relevant classes from the CAMEL library.

   ```python
   from camel.agents import ChatAgent
   ```

2. **Creating a `ChatAgent` Instance**:
   When you create an instance of `ChatAgent`, you can optionally pass a 
   `system_message` to define its role and behavior.

   ```python
   agent = ChatAgent(system_message="You are a helpful assistant.")
   ```

3. **Interacting with the Agent**:
   You can have a conversation by using the `step()` method, which allows you 
   to send messages and get responses.

   ```python
   user_message = "Hello, can you help me with a question?"
   response = agent.step(user_message)
   print(response.msgs[0].content)  # Print the agent's response
   ```

### Advanced Features

#### Integrating Tools

You can define tools (functions) that the agent can call during its operation.

```python
from camel.toolkits import FunctionTool

def calculator(a: int, b: int) -> int:
    return a + b

# Create ChatAgent with a tool
agent_with_tool = ChatAgent(tools=[calculator])
response = agent_with_tool.step("What is 2 + 2 using the calculator?")
```

#### Structured Output

You can specify structured outputs using Pydantic models to control the 
format of the response.

```python
from pydantic import BaseModel
from typing import List

class StructuredResponse(BaseModel):
    points: List[str]
    summary: str

agent = ChatAgent()
response = agent.step(
    "List benefits of exercise", response_format=StructuredResponse
)
```

### Example with a Specific Model

The code examples you provided also show how to specify and configure models 
used by `ChatAgent`. Here's how to create a `ChatAgent` with a custom model:

```python
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType

model = ModelFactory.create(
    model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
    model_type="gpt-3.5-turbo",  # Example model
    api_key="your_api_key",  # Ensure you have appropriate credentials
    model_config_dict={"temperature": 0.7}
)

camel_agent = ChatAgent(
    system_message="You are a helpful assistant.", model=model
)

user_message = "What are the best practices for using AI?"
response = camel_agent.step(user_message)
print(response.msgs[0].content)
```

### Conclusion

You can leverage `ChatAgent` in CAMEL to create powerful conversational agents 
that can perform a variety of tasks, integrate tools, and manage conversations 
effectively. The examples given demonstrate basic usage, tool integration, 
structured output formats, and model specification, allowing you to customize 
the behavior of your chat agent to suit your needs.

If you need more specific features or have other questions about the CAMEL 
framework, feel free to ask!

"""
