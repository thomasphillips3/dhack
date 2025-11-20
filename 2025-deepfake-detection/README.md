# Deepfake Detection Workshop

## "Seeing What AI Sees" — Detecting Deepfakes with Python

A hands-on 1-hour workshop teaching students to detect AI-generated images using metadata forensics, noise analysis, and convolutional neural networks.

## Learning Objectives

By the end of this workshop, students will:
1. Understand how deepfakes are created and detected
2. Inspect image metadata to identify potential AI-generated content
3. Use pre-trained AI models to detect patterns invisible to humans
4. Visualize which image features neural networks focus on (bonus)

## Workshop Schedule

### **0:00 – 0:10 → Kickoff & Context**
- **Warm-up question:** “How can you *tell* if an image is fake — and how could AI tell?”  
- Show 2–3 Gemini vs. real photos — quick “hands up” poll.  
- Explain:  
  - What deepfakes are (GANs, diffusion models in 2 mins).  
  - Why EXIF data and image noise matter.  
  - What convolutional networks look for (edges, textures, patterns).  

> **Key takeaway:** Real cameras leave *fingerprints* (metadata + sensor noise). AI art leaves *footprints* (pattern artifacts).

## DeepfakeKit API

To make the workshop easier to teach and more fun to code, we introduce a **helper API** that hides the boilerplate.  
Students can still run advanced analysis — metadata, noise stats, CNN features, and ensemble detection — with only a few clean lines of Python.

---

### Why an API?
- **Simplifies syntax:** no clutter, no long import blocks.
- **Safe fallback:** runs even without TensorFlow/OpenCV.  
- **Unified interface:** same object for all tasks — `DeepfakeKit`.

---

### Installation (Colab-friendly)
```bash
!pip install pillow exifread numpy
# Optional: for CNN and visualization
# !pip install tensorflow opencv-python matplotlib
```

### Quickstart
```python
from deepfakekit import DeepfakeKit
k = DeepfakeKit()

result = k.ensemble_flag('images/sample.jpg')
print(result)
```

## Workshop Flow (with API)

### **0:00 – 0:08 Kickoff & Context**
Same as before; discuss “fingerprints vs. footprints.”

### **0:08 – 0:20 Metadata Forensics**
```python
r = k.check_metadata('images/sample.jpg')
print(r.flags)
```
- Ask: which images have **no EXIF** or **missing camera**?

### **0:20 – 0:35 Noise & Sharpness Check**
```python
n = k.noise_stats('images/sample.jpg')
print(n.sharpness_laplacian, n.grayscale_std)
```
- Compare real vs. fake sharpness.

### **0:35 – 0:50 CNN Intuition (optional)**
```python
c = k.cnn_feature_intensity('images/sample.jpg')
print(c.feature_intensity)
```
- Visualize:
```python
k.plot_first_layer('images/sample.jpg', channels=6)
```

### **0:50 – 0:57 One‑Liner Ensemble**
```python
out = k.batch_ensemble('images')
sorted(out, key=lambda d: d.get('total_score', 0), reverse=True)[:5]
```

### **0:57 – 1:00 Wrap-Up**
- “If *you* were designing a deepfake detector, what signals would you add?”
- Encourage creativity — watermarking, bias detection, multimodal models.

## Requirements
- `deepfakekit.py` in the same directory or Colab.
- Folder `images/` with 5 real and 5 Gemini images.
- Internet connection for TensorFlow weights (optional).

## Project Structure

```
2025-deepfake-detection/
├── README.md                    # Workshop overview (this file)
├── SETUP.md                     # Installation instructions
├── WORKSHOP_CHECKLIST.md        # Day-of checklist for instructors
├── instructor_guide.md          # Complete teaching guide with answers
├── requirements.txt             # Python package dependencies
│
├── deepfakekit.py              # Main detection library
├── quick_start.py              # Test installation script
├── demo_complete.py            # Full demonstration script
│
├── exercises/                  # Student exercises
│   ├── exercise_1_metadata.py  # Metadata forensics
│   ├── exercise_2_noise.py     # Noise analysis
│   ├── exercise_3_cnn.py       # CNN visualization
│   └── exercise_4_ensemble.py  # Ensemble detection
│
└── images/                     # Sample images folder
    └── README.md               # Guide for preparing images
```

## Quick Start

**For Students:**
1. Follow instructions in `SETUP.md`
2. Run `python quick_start.py` to test your setup
3. Work through exercises in the `exercises/` folder (1-4 in order)

**For Instructors:**
1. Read `instructor_guide.md` for complete teaching notes
2. Use `WORKSHOP_CHECKLIST.md` to prepare
3. Run `python demo_complete.py` to test
4. Prepare sample images (see `images/README.md`)

## Additional Resources

- **SETUP.md** - Detailed installation guide for Colab, local, and Jupyter
- **instructor_guide.md** - Teaching script, answer keys, troubleshooting
- **WORKSHOP_CHECKLIST.md** - Day-of preparation checklist
- **images/README.md** - Guide for preparing test images

## Stretch Challenge

Students can combine multiple detection techniques:

```python
score = metadata_flag + cnn_confidence
if score > 1.5:
    print("Likely deepfake!")
```

## API Reference

See `deepfakekit.py` for the complete DeepfakeKit API implementation. Key methods:

- `check_metadata(path)` - Extract and analyze image metadata
- `noise_stats(path)` - Compute sharpness and noise statistics
- `cnn_feature_intensity(path)` - Run CNN-based feature extraction
- `ensemble_flag(path)` - Combined multi-method detection
- `batch_ensemble(folder)` - Analyze multiple images at once

## Contributing

This workshop material is designed for educational use. Feedback and suggestions are welcome!
