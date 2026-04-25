# LangChain/LangGraph Multi-Agent System with Gemma

This directory contains a multi-agent orchestration system powered by Gemma running on an ASUS Ascent GX10.

## Setup

### 1. Install Dependencies

```bash
cd agents
pip install -r requirements.txt
```

### 2. Start Gemma HTTP API on ASUS Ascent GX10

On your ASUS Ascent GX10, you need to run an HTTP API server for Gemma. Here's how to set it up:

#### Option A: Using vLLM (Recommended)

```bash
# On ASUS Ascent GX10
pip install vllm

# Start the API server
python -m vllm.entrypoints.api_server \
    --model google/gemma-4-2b-it \
    --host 0.0.0.0 \
    --port 8000 \
    --tensor-parallel-size 1 \
    --dtype float16
```

#### Option B: Using Transformers with FastAPI

Create a simple API server on the ASUS:

```python
# gemma_server.py (run on ASUS)
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

app = FastAPI()

MODEL_ID = "google/gemma-4-2b-it"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto",
    load_in_4bit=True
)
tokenizer.pad_token = tokenizer.eos_token

class GenerateRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.95
    do_sample: bool = True

@app.post("/generate")
def generate(request: GenerateRequest):
    inputs = tokenizer(request.prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=request.max_new_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            do_sample=request.do_sample,
            pad_token_id=tokenizer.eos_token_id
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"generated_text": generated_text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

Run it with:
```bash
pip install fastapi uvicorn
python gemma_server.py
```

### 3. Connect from Local Machine

Find the ASUS IP address:
```bash
# On ASUS
hostname -I
```

Then update the base_url in the agent scripts:
```python
base_url="http://<ASUS_IP>:8000"
```

## Usage

### Test Agent

Run a simple test agent:
```bash
cd agents
python test_agent.py
```

To connect to ASUS:
```python
run_test_agent(
    "Your query here",
    base_url="http://<ASUS_IP>:8000"
)
```

### Multi-Agent System

Run the multi-agent orchestration:
```bash
python multi_agent.py
```

To connect to ASUS:
```python
run_multi_agent(
    "Your query here",
    base_url="http://<ASUS_IP>:8000"
)
```

## Architecture

### Files

- `gemma_llm.py` - Custom LangChain LLM wrapper for Gemma
- `test_agent.py` - Simple single-agent example
- `multi_agent.py` - Multi-agent orchestration with specialized agents

### Multi-Agent System

The multi-agent system includes three specialized agents:

1. **Research Agent** - Gathers and summarizes information
2. **Analysis Agent** - Analyzes research data and provides insights
3. **Summary Agent** - Synthesizes findings into actionable conclusions

## Customization

### Adding New Agents

Create a new agent function in `multi_agent.py`:

```python
def create_custom_agent(base_url: str):
    llm = create_gemma_llm(base_url=base_url, temperature=0.5, max_new_tokens=512)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Your custom system prompt"),
        MessagesPlaceholder(variable_name="messages"),
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    def custom_node(state: MultiAgentState):
        messages = state["messages"]
        response = chain.invoke({"messages": messages})
        return {"messages": [AIMessage(content=response)]}
    
    return custom_node
```

Then add it to the workflow:
```python
workflow.add_node("custom", custom_node)
workflow.add_edge("previous_node", "custom")
```

### Adjusting Parameters

Modify LLM parameters in the agent creation:
```python
llm = create_gemma_llm(
    base_url=base_url,
    temperature=0.7,        # Higher = more creative
    max_new_tokens=512,     # Maximum response length
    top_p=0.95,            # Nucleus sampling
)
```

## Troubleshooting

### Connection Refused

- Ensure the Gemma API server is running on ASUS
- Check firewall settings on ASUS
- Verify the IP address is correct
- Test connectivity: `curl http://<ASUS_IP>:8000`

### Slow Responses

- Reduce `max_new_tokens` parameter
- Use quantization (4-bit) on the ASUS
- Consider using a smaller model (gemma-2b instead of gemma-7b)

### Out of Memory

- Enable 4-bit quantization on ASUS
- Reduce batch size in the API server
- Use gradient checkpointing if training

## Next Steps

1. Set up the Gemma HTTP API on your ASUS Ascent GX10
2. Test connectivity from your local machine
3. Run the test agent to verify functionality
4. Experiment with the multi-agent system
5. Customize agents for your specific use case
