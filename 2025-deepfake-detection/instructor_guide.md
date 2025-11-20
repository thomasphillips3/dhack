# Instructor Guide: Deepfake Detection Workshop

## Overview
This 1-hour workshop teaches advanced high school students how to detect AI-generated images using Python. Students will learn about metadata forensics, noise analysis, and convolutional neural networks.

**Target Audience:** Advanced high school students with Python experience
**Duration:** 60 minutes
**Date:** November 10, 2025
**Location:** Detroit Hackathon

---

## Pre-Workshop Setup (15 minutes before students arrive)

### 1. Environment Setup

**Option A: Google Colab (Recommended)**
- Easiest for students
- No installation needed
- Free GPU access

**Option B: Local Installation**
```bash
pip install pillow exifread numpy
# Optional but recommended:
pip install tensorflow opencv-python matplotlib
```

### 2. Prepare Sample Images

Create an `images/` folder with:
- **5 real photos** (from a phone camera or DSLR)
  - Should have EXIF data intact
  - Variety of subjects (people, nature, objects)

- **5 AI-generated images**
  - Use Gemini, DALL-E, Midjourney, or Stable Diffusion
  - Try to make them look realistic
  - Remove obvious watermarks

**Pro tip:** Include 1-2 "trick" images that challenge the detector!

### 3. Test the Code

Run `demo_complete.py` to verify everything works:
```bash
python demo_complete.py
```

---

## Workshop Schedule

### 0:00 - 0:08: Kickoff & Context (8 minutes)

**Opening Question:**
> "Show of hands: Who's seen a deepfake? Who can tell me how you'd spot one?"

**Key Points to Cover:**
1. **What are deepfakes?**
   - AI-generated images that look real
   - Created by GANs (Generative Adversarial Networks) or diffusion models
   - Used for entertainment, but also misinformation

2. **How do we detect them?**
   - **Fingerprints:** Real cameras leave metadata (EXIF data)
   - **Footprints:** AI leaves mathematical patterns in pixels
   - **Neural networks:** AI to fight AI

3. **Why it matters**
   - Misinformation in news and social media
   - Fraud and scams
   - Need for digital literacy

**Interactive Element:**
Show 2-3 images and do a quick poll:
- "Real or fake?"
- Reveal answers and discuss what clues they used

---

### 0:08 - 0:20: Metadata Forensics (12 minutes)

**Learning Goals:**
- Understand EXIF data
- Detect missing camera information
- Spot AI generator hints

**Teaching Script:**

1. **Explain EXIF data (2 min)**
   - "Every time you take a photo with a phone, it stamps metadata"
   - Show examples: camera model, date, GPS, settings
   - AI generators usually don't include this (or fake it poorly)

2. **Live Demo (3 min)**
   ```python
   from deepfakekit import DeepfakeKit
   kit = DeepfakeKit()

   # Pick an obvious real photo
   result = kit.check_metadata('images/real_photo.jpg')
   print(result.flags)
   print(result.tags)
   ```

   Point out:
   - Camera make/model
   - Date taken
   - Lots of technical details

3. **Students Try (5 min)**
   - Have them run `exercise_1_metadata.py`
   - Walk around to help
   - Ask: "What patterns do you see?"

4. **Discussion (2 min)**
   - "Can metadata alone prove something is fake?"
   - Answer: **No!** Metadata can be stripped or faked
   - That's why we need multiple methods

**Expected Student Discoveries:**
- Real photos have camera make/model
- AI images often have no EXIF at all
- Some AI tools leave hints (e.g., "Software: DALL-E")

**Common Issues:**
- Students might find real photos with no EXIF (if edited/compressed)
- Explain: "That's why we can't rely on this alone!"

---

### 0:20 - 0:35: Noise & Sharpness Analysis (15 minutes)

**Learning Goals:**
- Understand camera sensor noise
- Measure image sharpness
- Compare real vs. AI noise patterns

**Teaching Script:**

1. **Explain Sensor Noise (3 min)**
   - "Real cameras have physical sensors that introduce tiny random errors"
   - AI generates mathematically 'perfect' pixels
   - Show zoomed-in comparison if possible

2. **Introduce Sharpness (2 min)**
   - "We use the Laplacian operator to detect edges"
   - High variance = sharp edges (good)
   - Low variance = blurry/smooth (suspicious)

3. **Live Demo (3 min)**
   ```python
   result = kit.noise_stats('images/real_photo.jpg')
   print(f"Sharpness: {result.sharpness_laplacian}")
   print(f"Noise: {result.grayscale_std}")
   ```

   Compare with an AI image - point out differences

4. **Students Work (5 min)**
   - Have them run `exercise_2_noise.py`
   - Encourage comparing multiple images

5. **Discussion (2 min)**
   - "What patterns did you find?"
   - "Can AI generators add fake noise?"
   - Answer: **Yes!** This is an arms race

**Expected Student Discoveries:**
- Real photos: higher sharpness variance
- AI images: sometimes "too perfect"
- Some modern AI adds synthetic noise to fool detectors!

**Common Questions:**
- Q: "Why is my real photo showing low sharpness?"
  - A: Could be motion blur, out of focus, or heavy compression

- Q: "This AI image has high sharpness!"
  - A: Modern generators are getting better! That's why we combine methods

---

### 0:35 - 0:50: CNN Visualization (15 minutes)

**Learning Goals:**
- Understand how CNNs "see" images
- Extract and interpret feature vectors
- Visualize CNN activations

**Teaching Script:**

1. **Explain CNNs (4 min)**
   - "A CNN is like having millions of tiny pattern detectors"
   - First layers detect edges and colors
   - Deep layers detect complex patterns (faces, objects, styles)
   - We're using MobileNetV2, trained on millions of real photos

   **Analogy:**
   "Think of it like this: The CNN learned what 'real photos' look like from millions of examples. When it sees an AI image, the patterns don't quite match up - like hearing an accent you've never heard before."

2. **Live Demo: Feature Extraction (3 min)**
   ```python
   result = kit.cnn_feature_intensity('images/real_photo.jpg')
   print(f"Feature Intensity: {result.feature_intensity}")
   ```

   - Higher intensity = patterns match training data (real photos)
   - Lower intensity = unusual patterns (potentially AI)

3. **Live Demo: Visualization (3 min)**
   ```python
   kit.plot_first_layer('images/real_photo.jpg', channels=6)
   ```

   Explain what they're seeing:
   - Each plot is one "filter" in the CNN
   - Bright areas = filter activated
   - Common: edge detectors, texture filters

4. **Students Explore (4 min)**
   - Run `exercise_3_cnn.py`
   - Try visualizing different images
   - Compare real vs. AI feature maps

5. **Wrap-up Discussion (1 min)**
   - "This is how AI fights AI"
   - Limitation: can be fooled by new AI techniques

**Expected Student Discoveries:**
- CNNs respond differently to AI vs. real images
- Feature maps can be wild and abstract!
- The first layer looks for edges, colors, simple patterns

**Common Questions:**
- Q: "Why are these images so weird?"
  - A: You're seeing what individual neurons detect, not the final output

- Q: "What do the deeper layers see?"
  - A: More abstract patterns! (You can show this if time permits)

**Technical Note:**
First run will download MobileNetV2 weights (~14MB). Warn students this might take a minute.

---

### 0:50 - 0:57: Ensemble Detection (7 minutes)

**Learning Goals:**
- Combine multiple detection methods
- Understand ensemble voting
- Scan folders of images

**Teaching Script:**

1. **Explain Ensemble Methods (2 min)**
   - "Ensemble = combining multiple experts"
   - Each method gets a weight (how much we trust it)
   - Default: 70% metadata, 30% CNN
   - "Why not equal?" - Metadata is harder to fake (for now)

2. **Live Demo (2 min)**
   ```python
   result = kit.ensemble_flag('images/suspicious.jpg')
   print(f"Total Score: {result['total_score']}")
   print(f"Verdict: {result['likely_fake']}")
   ```

   Show the combined scoring

3. **Batch Processing Demo (2 min)**
   ```python
   results = kit.batch_ensemble('images')
   # Sort and show top suspects
   results.sort(key=lambda r: r.get('total_score', 0), reverse=True)
   for r in results[:3]:
       print(f"{r['path']}: {r['total_score']}")
   ```

4. **Students Try (1 min)**
   - Quick run of `exercise_4_ensemble.py`
   - See full results on their images

**Expected Student Discoveries:**
- Ensemble is more reliable than any single method
- Some images fool one test but not others
- You can tune weights for better accuracy

---

### 0:57 - 1:00: Wrap-Up & Discussion (3 minutes)

**Reflection Questions:**

1. **"If you were designing a deepfake detector, what would you add?"**
   - Accept creative answers
   - Possible ideas: analyze consistency across frames (for video), check lighting/shadows, semantic analysis

2. **"What are the limitations of these methods?"**
   - Arms race: AI generators improve constantly
   - Compressed/edited real photos can fail tests
   - Need large datasets to train better detectors

3. **"Where should this technology be used? Where shouldn't it?"**
   - Good: verifying news, combating fraud
   - Careful: privacy concerns, false positives
   - Discussion on ethics and bias

**Final Thoughts:**
- "This is a simplified teaching detector, not production-ready"
- "Real forensic tools use dozens of signals"
- "The race between generators and detectors never ends"

**Call to Action:**
- "Keep learning about AI safety"
- "Think critically about images you see online"
- "Consider studying computer vision or AI security"

---

## Answer Key for Exercises

### Exercise 1: Metadata Forensics

**Question 1:** "What do the flags tell you about this image?"
- **Sample Answer:** If `no_exif: True` and `missing_camera: True`, the image likely wasn't taken by a camera - possibly AI-generated or heavily edited.

**Question 2:** "Which images appear to be AI-generated based on metadata?"
- **Depends on their images** - typically those with no EXIF or AI hints

**Question 3:** "Can metadata alone definitively prove an image is fake?"
- **Answer:** No! Metadata can be stripped (making real photos look suspicious) or faked (making AI images look real). That's why we need multiple detection methods.

**Challenge:** "Ways AI could fake EXIF data?"
- Copy EXIF from real photos
- Generate realistic-looking timestamps
- Add fake camera model information
- Embed GPS coordinates from real locations

### Exercise 2: Noise Analysis

**Question 1:** "Does this image seem real or AI-generated?"
- **Sample Answer:** "Sharpness of 15 is very low, suggesting it might be AI-generated or heavily blurred."

**Question 2:** "What patterns do you notice?"
- **Expected:** Real photos tend to have higher sharpness variance and higher noise levels. AI images are often "too clean."

**Question 3:** "Why might some AI images still pass these tests?"
- **Answer:** Modern AI generators can add synthetic noise and control sharpness to mimic real cameras. Some generators specifically train to fool these detectors.

**Challenge:** "What would you add to make AI images look more real?"
- Add random sensor noise patterns
- Simulate lens distortion
- Add compression artifacts
- Vary sharpness naturally

### Exercise 3: CNN Visualization

**Question 1:** "What does the feature intensity suggest?"
- **Sample Answer:** "An intensity of 52.3 is relatively high, suggesting the CNN recognizes patterns it's seen in real photos during training."

**Question 2:** "Which feature maps showed the strongest activation?"
- **Varies by image** - often edge detection filters on high-contrast boundaries

**Question 3:** "Do the CNN results align with earlier findings?"
- **Expected:** Usually yes, but sometimes CNNs catch fakes that pass metadata/noise tests, showing the value of ensemble methods.

**Deep Dive:** "Why can CNNs detect deepfakes humans can't see?"
- CNNs process millions of images and learn subtle statistical patterns
- Humans rely on semantic understanding; CNNs see pixel-level patterns
- AI generators might create visually convincing images but with unusual mathematical signatures

**Stretch Challenge:** "Other statistics we could compute?"
- Maximum activation values
- Variance of feature activations
- Activation sparsity (how many neurons fire)
- Layer-by-layer comparison of patterns

### Exercise 4: Ensemble Detection

**Question 1:** "How is the total score calculated?"
- **Answer:** `total_score = (meta_weight * metadata_score) + (cnn_weight * cnn_score)`
- Default: `0.7 * metadata_score + 0.3 * cnn_score`

**Question 2:** "Top 3 images flagged as fake - do you agree?"
- **Varies by dataset** - discuss false positives and false negatives

**Question 3:** "Which weight configuration seems most accurate?"
- **Expected:** Depends on the test set, but balanced (0.5/0.5) often works well. Metadata-heavy (0.7/0.3) is more conservative.

**Reflection Answers:**

1. **Strengths of ensemble detection:**
   - More robust than individual methods
   - Catches fakes that fool single tests
   - Can be tuned for different use cases

2. **Limitations:**
   - Can't detect brand-new generation techniques
   - Might flag edited real photos
   - Requires all components working

3. **Additional signals to add:**
   - Reverse image search
   - Check for inconsistent lighting/shadows
   - Analyze facial features (if applicable)
   - Video: check temporal consistency
   - Semantic analysis (does the scene make sense?)

---

## Troubleshooting Guide

### Common Technical Issues

**Issue:** "TensorFlow won't install"
- **Solution:** Use Colab, or install TensorFlow 2.x specifically
- **Workaround:** Students can still do exercises 1-2 without TensorFlow

**Issue:** "No module named 'deepfakekit'"
- **Solution:** Make sure `deepfakekit.py` is in the same folder
- Or add to path: `import sys; sys.path.append('.')`

**Issue:** "Images folder not found"
- **Solution:** Create `images/` directory in the same folder as scripts
- Check that image paths are correct

**Issue:** "MobileNetV2 download is slow"
- **Solution:** Pre-download weights before class if possible
- Or have students share WiFi download

**Issue:** "Plots aren't showing"
- **Solution:** In Colab, plots show inline automatically
- Locally, might need `plt.show()` or run in Jupyter

### Pedagogical Challenges

**Challenge:** "Students finish at different speeds"
- **Solution:**
  - Fast finishers: Stretch challenges in each exercise
  - Slower students: Skip CNN visualization if needed, focus on ensemble

**Challenge:** "Student asks about production detectors"
- **Answer:** Real forensic tools (e.g., Adobe Content Authenticity) use:
  - Dozens more signals
  - Trained on millions of examples
  - Constant updates as AI evolves
  - Legal/cryptographic verification

**Challenge:** "Student found a way to fool the detector"
- **Response:** "Excellent! That's exactly how this arms race works. What would you add to catch your trick?"

**Challenge:** "Discussion about deepfake ethics gets heated"
- **Guide:**
  - Acknowledge valid concerns on all sides
  - Focus on responsible use of technology
  - Emphasize critical thinking over fear

---

## Extensions & Advanced Topics

If you have extra time or advanced students:

### 1. Build a Web Interface (30 min extension)
```python
import streamlit as st
from deepfakekit import DeepfakeKit

st.title("Deepfake Detector")
uploaded = st.file_uploader("Upload an image")
if uploaded:
    kit = DeepfakeKit()
    result = kit.ensemble_flag(uploaded)
    st.write(result)
```

### 2. Train a Custom Classifier
- Collect labeled dataset (real vs. fake)
- Extract features using DeepfakeKit
- Train sklearn classifier (LogisticRegression, RandomForest)

### 3. Video Deepfake Detection
- Extract frames from video
- Check temporal consistency
- Analyze face warping artifacts

### 4. Research Modern Techniques
- CLIP-based detection
- Blockchain verification
- Content Credentials (C2PA standard)

---

## Additional Resources

**For Students:**
- [Deepfake Detection Challenge (Kaggle)](https://www.kaggle.com/c/deepfake-detection-challenge)
- [AI Safety resources](https://www.aisafety.com)
- [EXIF data explained](https://photographylife.com/what-is-exif-data)

**For Instructors:**
- [GANs explained (3Blue1Brown)](https://www.youtube.com/watch?v=aircAruvnKk)
- [Diffusion models explained](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)
- [The State of Deepfakes 2024](https://arxiv.org/abs/2402.xxxxx) (search for latest papers)

**Academic Papers:**
- "FaceForensics++: Learning to Detect Manipulated Facial Images"
- "The Eyes Tell All: Detecting Political Orientation from Eye Movement Data"
- "CNN-generated images are surprisingly easy to spot... for now"

---

## Feedback & Iteration

After the workshop, collect feedback:
1. What was most interesting?
2. What was confusing?
3. Too fast / too slow?
4. What would you change?

Use this to improve for next time!

---

## License & Attribution

This curriculum is open source. Feel free to adapt and share!

**Created for:** Detroit Hackathon 2025
**Author:** [Your Name]
**Last Updated:** November 2025

---

**Good luck with your workshop! The students are going to love this.**
