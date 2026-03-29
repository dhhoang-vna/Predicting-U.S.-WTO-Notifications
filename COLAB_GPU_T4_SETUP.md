# Colab GPU T4 Setup Guide

**Last Updated:** March 29, 2026  
**Environment:** Google Colab with GPU T4  
**Python Version:** 3.10+  

---

## Quick Start

All notebooks have been updated with automatic Colab detection and Google Drive mounting. To run on Colab:

1. **Upload to Colab or link from Drive:**
   - Go to [Google Colab](https://colab.research.google.com)
   - Upload notebooks or open directly from Google Drive
   
2. **Enable GPU:**
   - Runtime → Change runtime type → GPU (T4 recommended)
   - Runtime → Run all or Run individual cells

3. **First Cell Auto-Runs** ✓
   - All notebooks now have a Colab setup cell at the top
   - This cell automatically:
     - ✓ Detects Colab environment
     - ✓ Mounts Google Drive
     - ✓ Checks GPU availability (T4)
     - ✓ Resolves project paths

---

## What's New in Each Notebook

### 1_notifs_data.ipynb
- **Setup:** Auto-detects Colab and local environments
- **GPU:** Not GPU-heavy (data loading & cleaning)
- **Runtime:** ~2-3 minutes on CPU, faster on T4

### 2_usitc_data.ipynb
- **Setup:** Auto-detects Colab and local environments
- **GPU:** Not GPU-heavy (trade data processing)
- **Runtime:** ~3-5 minutes
- **Note:** Large Excel files (~200MB) - may take time to read

### 3_merging.ipynb
- **Setup:** Auto-detects Colab and local environments
- **GPU:** CPU-only (data merging)
- **Runtime:** ~2-3 minutes

### 4_labeling.ipynb
- **Setup:** Auto-detects Colab and local environments
- **GPU:** Not GPU-heavy (label construction)
- **Runtime:** ~5-10 minutes

### 5_analysis_master.ipynb ⭐ (GPU-Heavy)
- **Setup:** Enhanced GPU configuration for T4
- **GPU:** Heavy DistilBERT fine-tuning (~10-15 min/epoch)
- **Runtime:** ~30-45 minutes for full pipeline
- **T4 Memory:** 16GB VRAM - watch for OOM errors
- **Batch Size:** Default 32 for DistilBERT (adjust down if OOM)
- **Enhancements:**
  - `print_gpu_usage()` function to monitor memory
  - Batch size recommendations in notebook
  - Early stopping to avoid long training
  - Mixed precision training support

### 6_IO_extension.ipynb
- **Setup:** Auto-detects Colab and local environments
- **GPU:** CPU-only (IO matrix operations)
- **Runtime:** ~10-15 minutes

### 7_robustness_outcome.ipynb
- **Setup:** Auto-detects Colab and local environments
- **GPU:** Heavy DistilBERT robustness checks
- **Runtime:** ~30-60 minutes depending on theta values tested
- **T4 Memory:** Similar to notebook 5

---

## Troubleshooting

### Google Drive Mount Fails
**Error:** `google.colab.errors.ImportError`

**Solution:**
```python
from google.colab import drive
drive.mount('/content/drive', force_remount=True)
```

### GPU Out-of-Memory (OOM)
**Error:** `RuntimeError: CUDA out of memory`

**Solution (in notebook 5):**
- Reduce `per_device_train_batch_size` from 32 to 16
- Reduce `per_device_eval_batch_size` from 32 to 16
- Increase `gradient_accumulation_steps` (slower but same effective batch size)

```python
# In TrainingArguments, adjust:
per_device_train_batch_size=16,  # instead of 32
per_device_eval_batch_size=16,   # instead of 32
```

### Project Root Not Found
**Error:** `FileNotFoundError: Could not locate project root`

**Solution:**
```python
import os
os.environ['PROJECT_ROOT'] = '/content/drive/MyDrive/Project'
```
Then re-run the setup cell.

### Files Not Visible in Colab
**Issue:** Files stored in local `data/` folder not visible

**Solution:**
1. Upload the `data/` folder to Google Drive
2. Or use Colab's file upload: Files → Upload
3. Then set `PROJECT_ROOT` environment variable

---

## GPU T4 Performance Notes

### Specifications
- **VRAM:** 16 GB (shared with CPU)
- **Architecture:** Tensor cores optimized for ML
- **Boost:** ~4× faster than CPU for deep learning

### Performance Estimates

| Task | Baseline (CPU) | T4 GPU | Speedup |
|------|---|---|---|
| Notebook 1 (data cleaning) | 3 min | 2 min | 1.5× |
| Notebook 2 (USITC data) | 5 min | 4 min | 1.25× |
| Notebook 3 (merging) | 3 min | 2.5 min | 1.2× |
| Notebook 4 (labeling) | 10 min | 8 min | 1.25× |
| Notebook 5 (DistilBERT) | 3-4 hrs | 30-45 min | **5-8×** |
| Notebook 6 (IO extension) | 15 min | 10 min | 1.5× |
| Notebook 7 (robustness) | 2-3 hrs | 30-60 min | **3-5×** |

### Memory Usage

```
GPU Memory Breakdown (Notebook 5):
├─ Model weights: ~268 MB (DistilBERT)
├─ Optimizer state: ~800 MB
├─ Batch data: ~2-4 GB (batch_size=32)
├─ Gradients: ~268 MB
└─ Headroom: ~11-12 GB (for safety)
```

---

## Optimization Tips

### 1. **Early Cell Execution**
Run cell 1 (Colab setup) immediately, before anything else.

### 2. **Memory Monitoring**
Add this to check GPU memory during long runs:

```python
def print_gpu_usage():
    import torch
    if torch.cuda.is_available():
        alloc = torch.cuda.memory_allocated() / (1024**3)
        cached = torch.cuda.memory_reserved() / (1024**3)
        print(f"GPU Memory: {alloc:.2f}GB allocated, {cached:.2f}GB cached")

# Call periodically during training
print_gpu_usage()
```

### 3. **Batch Size Tuning**
For notebook 5, experiment with batch sizes:

```python
# Conservative (safer, slower)
per_device_train_batch_size=16
per_device_eval_batch_size=16
gradient_accumulation_steps=2

# Fast (use if no OOM)
per_device_train_batch_size=32
per_device_eval_batch_size=32
gradient_accumulation_steps=1
```

### 4. **Data Loading**
- Data is loaded into memory once - subsequent epochs are fast
- First run is slower due to CSV parsing
- Use `dtype` specifications to save memory

### 5. **Model Checkpointing**
- Notebook 5 auto-saves best model to Google Drive
- Can resume training if session disconnects
- Check `data/cleaned_data/distilbert_run/` for checkpoints

---

## File Structure in Colab

```
/content/drive/MyDrive/Project/
├── code/
│   ├── 1_notifs_data.ipynb
│   ├── 2_usitc_data.ipynb
│   ├── 3_merging.ipynb
│   ├── 4_labeling.ipynb
│   ├── 5_analysis_master.ipynb           ← GPU-heavy
│   ├── 6_IO_extension.ipynb
│   └── 7_robustness_outcome.ipynb        ← GPU-heavy
├── data/
│   ├── raw/
│   │   ├── Notifications 2010-25.xlsx
│   │   ├── USITC 2010-16 SEA.xlsx
│   │   ├── USITC 2017-22 SEA.xlsx
│   │   ├── USITC 2023-25 SEA.xlsx
│   │   └── io_country_isic2_preavg.csv
│   └── cleaned_data/
│       ├── us_notif_clean_wide.csv
│       ├── usitc_imports_hs4_panel.csv
│       ├── hs4_imports_with_notif_exposure.csv
│       ├── notif_labels_hs4.csv
│       ├── distilbert_run/
│       └── ... (other output CSVs)
├── fig/
│   └── (output plots)
├── README.md
├── requirements.txt
└── COLAB_GPU_T4_SETUP.md (this file)
```

---

## Package Versions

All notebooks use tested versions compatible with Colab T4:

```
numpy>=2.0,<2.1
pandas>=2.2,<2.4
scipy>=1.13,<1.16
scikit-learn>=1.6,<1.8
matplotlib>=3.9,<3.11
seaborn>=0.13,<0.14
openpyxl>=3.1,<3.2
torch>=2.4
transformers==4.45.0
datasets>=2.20
accelerate>=0.33
sentence-transformers>=3.0
```

**Auto-Installation:** Notebook 5 auto-installs these if missing:
```python
import subprocess
import sys
subprocess.check_call([sys.executable, "-m", "pip", "-q", "install", 
                      "transformers==4.45.0", "datasets", "accelerate", ...])
```

---

## FAQ

**Q: Can I run locally after using Colab?**  
A: Yes! The notebooks auto-detect the environment (local or Colab). Just copy the notebooks and data locally.

**Q: How long does notebook 5 take?**  
A: ~30-45 minutes on T4 GPU (vs 3-4 hours on CPU). First cell takes longest due to DistilBERT fine-tuning.

**Q: What if I get disconnected?**  
A: Colab disconnects after 12 hours or 30 min inactivity. Notebook 5 saves checkpoints - you can resume from the last saved model.

**Q: Can I use GPU with paid Colab+ Pro?**  
A: Yes! Colab+ provides A100 GPUs (faster). Notebooks are compatible. Change Runtime → GPU.

**Q: How do I monitor GPU usage live?**  
A: Use `!nvidia-smi` in a cell to show live GPU stats:
```python
!nvidia-smi
```

**Q: Will the code output to Colab or Google Drive?**  
A: Both! Intermediate data/figures are saved to Drive automatically via path resolution.

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review notebook comments for cell-specific notes
3. Verify Google Drive upload with all required files
4. Ensure GPU is enabled (Runtime → Change runtime type)

---

**Happy analyzing with Colab GPU T4! 🚀**
