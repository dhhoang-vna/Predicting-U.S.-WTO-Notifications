# Quick Start: Running on Colab GPU T4

## 30-Second Setup

1. **Go to** [Google Colab](https://colab.research.google.com)
2. **Upload** or open notebooks from Google Drive
3. **Enable GPU:** Runtime → Change runtime type → GPU (T4)
4. **Run ALL cells** in each notebook (in order: 1→7)

✅ **Done!** All notebooks auto-detect Colab and set up Google Drive + GPU

---

## Key Points

| Notebook | Time | GPU? | Run? |
|----------|------|------|------|
| 1 - Data Cleaning | 2-3 min | ⚠ Optional | ✓ Run in Colab |
| 2 - USITC Trade | 3-5 min | ⚠ Optional | ✓ Run in Colab |
| 3 - Merging | 2-3 min | ⚠ Optional | ✓ Run in Colab |
| 4 - Labeling | 5-10 min | ⚠ Optional | ✓ Run in Colab |
| **5 - ML Models** | **30-45 min** | ⭐ **REQUIRED** | ✓✓ Run in Colab |
| 6 - IO Analysis | 10-15 min | ⚠ Optional | ✓ Run in Colab |
| **7 - Robustness** | **30-60 min** | ⭐ **REQUIRED** | ✓✓ Run in Colab |

⭐ = GPU highly recommended (5-8× speedup)

---

## What's New in Your Notebooks

Each notebook now starts with an automatic setup cell that:
- ✅ Detects if running in Colab or locally
- ✅ Mounts Google Drive (in Colab)
- ✅ Detects GPU (T4 = 16GB VRAM)
- ✅ Resolves project paths automatically

**Just run the first cell, then everything works!**

---

## If You Get Errors

### Error: "Project root not found"
```python
import os
os.environ['PROJECT_ROOT'] = '/content/drive/MyDrive/Project'
```
Then re-run the first cell.

### Error: "CUDA out of memory"
In Notebook 5, reduce batch size:
```python
per_device_train_batch_size=16  # was 32
per_device_eval_batch_size=16   # was 32
```

### Error: "Files not found"
Make sure folders are uploaded to Google Drive:
- `data/raw/` - Contains Excel files and data files
- `code/` - Contains your notebooks

---

## Performance: Local vs. Colab T4

| Task | CPU | T4 GPU | Speedup |
|------|-----|--------|---------|
| Notebook 5 | 3-4 hrs | 30-45 min | **5-8×** |
| Notebook 7 | 2-3 hrs | 30-60 min | **3-5×** |

**Total time:** ~2-3 hours with T4 vs. ~8-12 hours on CPU

---

## Full Documentation

See **COLAB_GPU_T4_SETUP.md** for:
- Detailed troubleshooting
- GPU memory management
- Batch size tuning
- Package versions
- File structure

---

**Everything is automated. Just run and enjoy 30-45 min training instead of 3-4 hours! 🚀**
