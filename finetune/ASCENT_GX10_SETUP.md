# Asus Ascent GX10 Setup Guide

Your Asus Ascent GX10 is perfect for Gemma 4 fine-tuning with its NVIDIA Blackwell GPU and 128GB unified memory.

## Hardware Specs
- **GPU**: NVIDIA Blackwell (GB10) - 1 petaFLOP FP4 compute
- **Memory**: 128GB LPDDR5x unified memory
- **CPU**: ARM v9.2-A
- **OS**: Ubuntu Linux
- **Capacity**: Fine-tuning up to 200B parameter models

## Setup Steps

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install ARM-compatible Python
```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 3. Create Virtual Environment
```bash
cd /path/to/agentic-island/finetune
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install ARM-compatible PyTorch
```bash
# For ARM architecture with Blackwell GPU
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Verify GPU Access
```bash
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

## Optimized Training for Ascent GX10

### Use Larger Model
Edit `train_gemma.py` to use Gemma-7B instead of Gemma-2B:
```python
MODEL_ID = "google/gemma-7b"  # Changed from gemma-2b
```

### Increase Batch Size
With 128GB memory, you can use larger batches:
```python
BATCH_SIZE = 8  # Increased from 4
GRADIENT_ACCUMULATION_STEPS = 2  # Reduced from 4
```

### Remove Quantization (Optional)
Blackwell GPU has enough memory to skip 4-bit quantization for better quality:
```python
# In train_gemma.py, change:
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto",
    # load_in_4bit=True  # Comment this out for full precision
)
```

### Increase Sequence Length
```python
MAX_SEQ_LENGTH = 1024  # Increased from 512
```

## Performance Expectations

With your Ascent GX10:
- **Gemma-2B**: ~30-60 minutes per epoch
- **Gemma-7B**: ~2-4 hours per epoch
- **Full precision training**: Better quality, ~2x memory usage
- **4-bit quantization**: Faster, ~50% memory usage

## Troubleshooting

### CUDA not detected
```bash
# Check NVIDIA driver
nvidia-smi

# Install CUDA toolkit if needed
sudo apt install nvidia-cuda-toolkit
```

### ARM compatibility issues
Some packages may need ARM-specific builds. If you encounter errors:
```bash
# Try installing from source
pip install --no-binary :all: <package_name>
```

### Memory issues
Even with 128GB, monitor usage:
```bash
# In another terminal
watch -n 1 nvidia-smi
```

## Advanced: Multi-GPU (if available)
If you have multiple Ascent GX10 units, you can use distributed training:
```python
# Add to train_gemma.py
import torch.distributed as dist
# Configure for multi-GPU training
```

## Running Training

```bash
cd finetune
source .venv/bin/activate
python prepare_gemma_data.py
python train_gemma.py
```

Your Ascent GX10 should handle Gemma-7B fine-tuning comfortably with its 128GB unified memory and Blackwell GPU.
