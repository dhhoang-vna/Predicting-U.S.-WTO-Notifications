"""
Colab GPU T4 Utilities
Shared functions for setting up and optimizing Colab environments.

Usage in notebooks:
    from colab_utils import setup_colab, get_project_root, print_gpu_usage
    INFO = setup_colab()
    PROJECT_ROOT = get_project_root()
    print_gpu_usage()
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Detect Colab environment
def is_colab() -> bool:
    """Check if running in Google Colab."""
    if "COLAB_RELEASE_TAG" in os.environ or "COLAB_GPU" in os.environ:
        return True
    if "google.colab" in sys.modules:
        return True
    try:
        from google.colab import drive
        return True
    except (ImportError, AttributeError):
        return False


def setup_colab() -> Dict[str, Any]:
    """
    Setup Google Colab environment and return environment info.
    
    Returns:
        Dict with keys:
        - 'in_colab': bool, whether running in Colab
        - 'gpu_available': bool, whether GPU is available
        - 'gpu_name': str, GPU name if available
        - 'gpu_memory_gb': float, GPU memory in GB if available
        - 'device': str, 'cuda' or 'cpu'
        - 'drive_mounted': bool, whether Google Drive is mounted
    """
    info = {
        'in_colab': is_colab(),
        'gpu_available': False,
        'gpu_name': None,
        'gpu_memory_gb': 0,
        'device': 'cpu',
        'drive_mounted': False,
    }
    
    # Environment detection
    env_str = "COLAB" if info['in_colab'] else "LOCAL"
    print(f"\n{'='*70}")
    print(f"Environment: {env_str}")
    print(f"{'='*70}")
    
    # Mount Google Drive if in Colab
    if info['in_colab']:
        try:
            from google.colab import drive
            print("Mounting Google Drive...")
            drive.mount("/content/drive", force_remount=False)
            info['drive_mounted'] = True
            print("✓ Google Drive mounted at /content/drive/MyDrive")
        except Exception as e:
            print(f"⚠ Drive mount error: {e}")
    
    # GPU detection
    try:
        import torch
        if torch.cuda.is_available():
            info['gpu_available'] = True
            info['gpu_name'] = torch.cuda.get_device_name(0)
            info['gpu_memory_gb'] = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            info['device'] = 'cuda'
            
            print(f"✓ GPU Available: {info['gpu_name']} ({info['gpu_memory_gb']:.1f} GB)")
            if info['gpu_name'] == 'Tesla T4':
                print("  T4 GPU has 16GB VRAM. Monitor memory usage in GPU-heavy cells.")
            
            # Optimize GPU settings
            if info['in_colab']:
                os.environ['CUDA_VISIBLE_DEVICES'] = '0'
                os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
                torch.cuda.empty_cache()
                print("  GPU optimization: Memory growth enabled")
        else:
            print("⚠ GPU NOT detected (CPU mode - slower)")
    except ImportError:
        print("⚠ PyTorch not installed yet")
    
    print(f"Device: {info['device'].upper()}")
    print(f"{'='*70}\n")
    
    return info


def get_project_root(verbose: bool = True) -> Path:
    """
    Resolve project root for both local and Colab environments.
    
    Args:
        verbose: Print debugging info
        
    Returns:
        Path to project root
        
    Raises:
        FileNotFoundError: If project root cannot be located
    """
    def _looks_like_root(p: Path) -> bool:
        try:
            checks = [
                (p / 'README.md').exists(),
                (p / 'code').exists(),
                (p / 'data').exists(),
            ]
            return all(checks)
        except (OSError, PermissionError):
            return False
    
    candidates = []
    cwd = Path.cwd().resolve()
    
    # Check environment variable first
    env_root = os.environ.get('PROJECT_ROOT', '').strip()
    if env_root:
        candidates.append(Path(env_root))
    
    # Add cwd and parents
    candidates.extend([cwd] + list(cwd.parents))
    
    # Add Colab paths
    if is_colab():
        candidates.extend([
            Path('/content/drive/MyDrive/Project'),
            Path('/content/drive/My Drive/Project'),
            Path('/root/Project'),
        ])
    else:
        # Local paths
        candidates.extend([
            Path('/mnt/g/My Drive/Project'),
            Path('G:/My Drive/Project'),
        ])
    
    # Deduplicate and find first valid
    seen = set()
    for p in candidates:
        s = str(p)
        if s not in seen:
            seen.add(s)
            if _looks_like_root(p):
                if verbose:
                    print(f"✓ Project root: {p}")
                return p
    
    # Fallback
    if _looks_like_root(cwd):
        if verbose:
            print(f"✓ Project root (fallback): {cwd}")
        return cwd
    
    # Error message
    error_msg = (
        f"Could not locate project root.\n"
        f"Current directory: {cwd}\n"
        f"Checked (first 5):\n"
    )
    for i, p in enumerate(candidates[:5], 1):
        error_msg += f"  {i}. {p}\n"
    error_msg += (
        "\nSolution:\n"
        "  1. Ensure project files are uploaded to Google Drive\n"
        "  2. Set environment variable: os.environ['PROJECT_ROOT'] = '/path/to/project'\n"
        "  3. Run this cell again"
    )
    raise FileNotFoundError(error_msg)


def print_gpu_usage() -> None:
    """Print current GPU memory usage."""
    try:
        import torch
        if torch.cuda.is_available():
            total = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            alloc = torch.cuda.memory_allocated() / (1024**3)
            cached = torch.cuda.memory_reserved() / (1024**3)
            free = total - cached
            print(
                f"GPU Memory: {alloc:.2f}GB allocated / {cached:.2f}GB cached / "
                f"{free:.2f}GB free (Total: {total:.1f}GB)"
            )
        else:
            print("GPU not available")
    except Exception as e:
        print(f"Error getting GPU memory: {e}")


def clear_gpu_memory() -> None:
    """Clear GPU cache and free memory."""
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            print("✓ GPU cache cleared")
    except Exception:
        pass


def configure_batch_size(
    task: str = "distilbert"
) -> Dict[str, int]:
    """
    Get recommended batch size based on task and GPU.
    
    Args:
        task: One of 'distilbert', 'tfidf', 'baseline'
        
    Returns:
        Dict with 'train_batch_size' and 'eval_batch_size'
    """
    is_gpu = False
    try:
        import torch
        is_gpu = torch.cuda.is_available()
    except ImportError:
        pass
    
    recommendations = {
        'distilbert': {
            'cpu': {'train_batch_size': 8, 'eval_batch_size': 8},
            'gpu': {'train_batch_size': 32, 'eval_batch_size': 32},
        },
        'tfidf': {
            'cpu': {'train_batch_size': 128, 'eval_batch_size': 128},
            'gpu': {'train_batch_size': 256, 'eval_batch_size': 256},
        },
        'baseline': {
            'cpu': {'train_batch_size': 128, 'eval_batch_size': 128},
            'gpu': {'train_batch_size': 256, 'eval_batch_size': 256},
        },
    }
    
    device = 'gpu' if is_gpu else 'cpu'
    config = recommendations.get(task, recommendations['baseline'])
    batch_config = config.get(device, config['cpu'])
    
    print(f"Batch size (task={task}, device={device}):")
    print(f"  Train: {batch_config['train_batch_size']}")
    print(f"  Eval: {batch_config['eval_batch_size']}")
    
    return batch_config


def validate_data_files(project_root: Path, required_files: list) -> bool:
    """
    Validate that required data files exist.
    
    Args:
        project_root: Path to project root
        required_files: List of relative paths to check
        
    Returns:
        True if all files exist, False otherwise
    """
    missing = []
    for f in required_files:
        path = project_root / f
        if not path.exists():
            missing.append(f)
    
    if missing:
        print(f"⚠ Missing files: {', '.join(missing)}")
        return False
    else:
        print(f"✓ All required files found")
        return True
