# Hackathon Quick Start Guide

Fast-track Gemma fine-tuning for your hackathon demo.

## Fast Mode (Default)

The training script is already configured in **FAST_MODE = True** for quick results:

**Time estimate: 30-60 minutes total**
- Gemma-2B model (smaller, faster)
- 1 epoch only
- 4-bit quantization
- Smaller LoRA rank

## Quick Setup (5 minutes)

```bash
cd finetune
python3 -m venv .venv
source .venv/bin/activate
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
pip install -r requirements.txt
```

## Run Training (30-60 minutes)

```bash
python prepare_gemma_data.py
python train_gemma.py
```

That's it! The script is already in fast mode.

## Test Your Model (2 minutes)

```bash
python inference.py
```

## Total Time: ~40-65 minutes

**Breakdown:**
- Setup: 5 minutes
- Data prep: 2 minutes
- Training: 30-60 minutes
- Testing: 2 minutes

## If You Have More Time

If you want better quality and have 2-3 hours:

Edit `train_gemma.py`:
```python
FAST_MODE = False  # Change to False
```

This will:
- Use Gemma-7B (better quality)
- Train for 3 epochs
- Full precision (no quantization)
- Take ~2-3 hours total

## Demo Tips

For your hackathon demo:
1. **Prepare inference examples** ahead of time
2. **Save sample outputs** during training to show progress
3. **Have a few preset scenarios** ready (e.g., "Kendall and Nicole at the fire pit")
4. **Show the multi-agent conversation** feature in inference.py

## Troubleshooting

**Training too slow?**
- Already in fast mode - this is the quickest option
- Reduce training data: Edit `prepare_gemma_data.py` to use smaller subset

**Still too slow?**
- Use even smaller subset: Take first 1000 examples instead of all 9771
- Edit `prepare_gemma_data.py`:
```python
data = load_training_data(INPUT_FILE)[:1000]  # Use only 1000 examples
```

This would reduce training to ~10-15 minutes but with lower quality.

Good luck with your hackathon!
