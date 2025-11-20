# Setup Guide: Deepfake Detection Workshop

This guide will help you set up the environment for the deepfake detection workshop.

## Quick Start (Students)

### Option 1: Google Colab (Easiest - Recommended)

1. **Open Google Colab:** [colab.research.google.com](https://colab.research.google.com)

2. **Create a new notebook**

3. **Install requirements:**
   ```python
   !pip install pillow exifread numpy tensorflow opencv-python matplotlib
   ```

4. **Upload files:**
   - Click the folder icon on the left sidebar
   - Upload `deepfakekit.py`
   - Create a folder called `images` and upload your test images
   - Upload the exercise files you want to run

5. **Run an exercise:**
   ```python
   !python exercises/exercise_1_metadata.py
   ```

**Pros:**
- No installation needed
- Free GPU access (for faster CNN processing)
- Works on any device with a browser

**Cons:**
- Need internet connection
- Files don't persist (need to re-upload each session)

---

### Option 2: Local Installation (Python on your computer)

**Prerequisites:**
- Python 3.8 or higher ([Download Python](https://www.python.org/downloads/))
- pip (comes with Python)

**Steps:**

1. **Download the workshop files:**
   - Download all `.py` files and `README.md` to a folder
   - Create a subfolder called `images`

2. **Open terminal/command prompt** in that folder:
   - **Mac/Linux:** Right-click folder → "Open in Terminal"
   - **Windows:** Shift + Right-click folder → "Open PowerShell window here"

3. **Install requirements:**

   **Minimal installation (metadata and noise only):**
   ```bash
   pip install pillow exifread numpy opencv-python
   ```

   **Full installation (includes CNN features):**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install pillow exifread numpy tensorflow opencv-python matplotlib
   ```

4. **Verify installation:**
   ```bash
   python -c "from deepfakekit import DeepfakeKit; print('Success!')"
   ```

5. **Run an exercise:**
   ```bash
   python exercises/exercise_1_metadata.py
   ```

**Troubleshooting:**

- **"pip not found":**
  - Try `pip3` instead of `pip`
  - Or `python -m pip install ...`

- **"Permission denied":**
  - Add `--user` flag: `pip install --user pillow`

- **TensorFlow installation fails:**
  - You can skip TensorFlow and still do exercises 1-2
  - Try installing a specific version: `pip install tensorflow==2.13.0`
  - On Mac M1/M2, use: `pip install tensorflow-macos`

---

### Option 3: Jupyter Notebook (Local)

If you prefer interactive notebooks:

1. **Install Jupyter:**
   ```bash
   pip install jupyter
   ```

2. **Start Jupyter:**
   ```bash
   jupyter notebook
   ```

3. **Create a new notebook** and run the exercise code cell by cell

---

## Setup for Instructors

### Pre-Workshop Checklist (1 day before)

- [ ] Test all exercise files on the platform students will use (Colab or local)
- [ ] Prepare sample images (5 real, 5 AI-generated)
- [ ] Verify TensorFlow can download MobileNetV2 weights
- [ ] Run `demo_complete.py` to ensure everything works
- [ ] Prepare backup plan if WiFi is unreliable

### Preparing Sample Images

**Real Photos (5 images):**
1. Take photos with a phone camera or DSLR
2. **Do NOT edit them** (preserve EXIF data)
3. Variety of subjects: people, nature, objects, etc.
4. Save as JPG (not PNG, which often strips EXIF)

**AI-Generated Images (5 images):**
1. Use free tools:
   - [Gemini](https://gemini.google.com/) (free, good quality)
   - [DALL-E 3](https://openai.com/dall-e-3) (via Bing Image Creator)
   - [Stable Diffusion](https://stablediffusionweb.com/) (free)

2. Prompts to try:
   - "A realistic photo of a person sitting in a coffee shop"
   - "A high-quality photograph of a sunset over mountains"
   - "A photorealistic image of a dog playing in a park"

3. Download as JPG or PNG
4. Try to make them look realistic (challenging for the detector)

**Optional: "Trick" Images**
- A real photo that's been edited (EXIF stripped)
- An AI image with fake EXIF added
- A highly compressed real photo

### Image Folder Structure

```
2025-deepfake-detection/
├── deepfakekit.py
├── demo_complete.py
├── quick_start.py
├── requirements.txt
├── README.md
├── SETUP.md
├── instructor_guide.md
├── WORKSHOP_CHECKLIST.md
├── exercises/
│   ├── exercise_1_metadata.py
│   ├── exercise_2_noise.py
│   ├── exercise_3_cnn.py
│   └── exercise_4_ensemble.py
└── images/
    ├── README.md
    ├── real_photo_*.jpg (5 images)
    └── ai_generated_*.jpg (5 images)
```

### Testing Before Workshop

**Run the demo:**
```bash
python demo_complete.py
```

**Expected output:**
- Metadata analysis showing camera info for real photos
- No EXIF for AI images
- Sharpness and noise statistics
- CNN feature extraction (may take a minute first time)
- Final ensemble verdicts

**If something fails:**
- Check that all images are in the `images/` folder
- Verify Python packages are installed
- Test with a minimal example:
  ```python
  from deepfakekit import DeepfakeKit
  kit = DeepfakeKit()
  print(kit.check_metadata('images/sample.jpg'))
  ```

---

## Platform-Specific Notes

### Google Colab Tips

**Mounting Google Drive (to save files):**
```python
from google.colab import drive
drive.mount('/content/drive')
```

**Uploading files programmatically:**
```python
from google.colab import files
uploaded = files.upload()  # Opens file picker
```

**Faster TensorFlow on Colab:**
- Runtime → Change runtime type → GPU
- This makes CNN analysis much faster!

### Windows-Specific Issues

**Long path names:**
- Keep folder names short
- Put workshop folder in `C:\workshop\` instead of deep in Documents

**Visual Studio Build Tools** (if TensorFlow fails):
- Download from: https://visualstudio.microsoft.com/downloads/
- Install "Desktop development with C++"

### Mac M1/M2 Chips

**TensorFlow installation:**
```bash
pip install tensorflow-macos
pip install tensorflow-metal  # For GPU acceleration
```

**Alternative:** Use Miniforge and create a conda environment
```bash
conda create -n deepfake python=3.10
conda activate deepfake
conda install -c apple tensorflow-deps
pip install tensorflow-macos
```

### Linux

Usually works out of the box! If TensorFlow fails:
```bash
pip install tensorflow-cpu  # Lighter version without GPU
```

---

## Verifying Installation

Run this test script to check everything is working:

```python
# test_installation.py
from deepfakekit import DeepfakeKit
import sys

print("Testing DeepfakeKit installation...\n")

kit = DeepfakeKit()

# Test 1: Metadata
try:
    result = kit.check_metadata('images/sample.jpg')
    print("✓ Metadata analysis: OK")
except Exception as e:
    print(f"✗ Metadata analysis: FAILED ({e})")

# Test 2: Noise
try:
    result = kit.noise_stats('images/sample.jpg')
    print("✓ Noise analysis: OK")
except Exception as e:
    print(f"✗ Noise analysis: FAILED ({e})")

# Test 3: CNN
try:
    result = kit.cnn_feature_intensity('images/sample.jpg')
    print("✓ CNN analysis: OK")
except Exception as e:
    print(f"✗ CNN analysis: FAILED ({e})")
    print("  (TensorFlow may not be installed - this is optional)")

# Test 4: Ensemble
try:
    result = kit.ensemble_flag('images/sample.jpg')
    print("✓ Ensemble detection: OK")
except Exception as e:
    print(f"✗ Ensemble detection: FAILED ({e})")

print("\nInstallation test complete!")
```

Save this as `test_installation.py` and run:
```bash
python test_installation.py
```

---

## Minimal vs. Full Installation

### Minimal (No TensorFlow - faster install)

**Pros:**
- Faster installation (~30 seconds)
- Smaller download (~50MB)
- Works on older computers

**Cons:**
- No CNN features (Exercise 3 won't work)
- No visualization (plot_first_layer won't work)

**When to use:**
- Students have slow internet
- Older computers
- Just want to teach metadata/noise concepts

**Installation:**
```bash
pip install pillow exifread numpy opencv-python
```

### Full (With TensorFlow - recommended)

**Pros:**
- Complete workshop experience
- CNN visualization is very impressive!
- Shows state-of-the-art detection

**Cons:**
- Larger download (~500MB for TensorFlow)
- Slower installation (5-10 minutes)
- Requires more RAM

**Installation:**
```bash
pip install pillow exifread numpy tensorflow opencv-python matplotlib
```

---

## Common Error Messages

### `ModuleNotFoundError: No module named 'deepfakekit'`

**Solution:**
- Make sure `deepfakekit.py` is in the same folder as your exercise files
- Or add the folder to Python's path:
  ```python
  import sys
  sys.path.append('/path/to/workshop/folder')
  ```

### `FileNotFoundError: images/sample.jpg`

**Solution:**
- Create an `images` folder in the same directory
- Add at least one image named `sample.jpg`
- Check that the path is correct (use forward slashes even on Windows)

### `ImportError: cannot import name 'MobileNetV2'`

**Solution:**
- TensorFlow is not properly installed
- Try: `pip install --upgrade tensorflow`
- Or use CPU-only version: `pip install tensorflow-cpu`

### `Could not load dynamic library 'cudart64_110.dll'`

**This is just a warning - you can ignore it!**
- It means TensorFlow will use CPU instead of GPU
- Still works fine, just a bit slower

### `OMP: Error #15: Initializing libiomp5md.dll`

**Solution (Windows):**
```bash
pip install intel-openmp
```

Or set environment variable:
```python
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
```

---

## Getting Help

**During the workshop:**
- Raise your hand and an instructor will help
- Check with a neighbor - pair programming!
- Try the minimal installation if full install fails

**After the workshop:**
- GitHub issues: [link to your repo]
- Email: [your email]
- Stack Overflow: Tag questions with `deepfake-detection`

---

## Next Steps

Once setup is complete:
1. Read `README.md` for workshop overview
2. Instructors: Read `instructor_guide.md`
3. Students: Start with `exercises/exercise_1_metadata.py`
4. For a quick demo: Run `python quick_start.py`

**Good luck! You're ready to detect deepfakes!**
