# Deepfake Detection Workshop - Day-of Checklist

Use this checklist to ensure you're ready for the deepfake detection workshop!

---

## One Week Before

- [ ] **Test all code** on the platform students will use (Colab or local)
- [ ] **Gather sample images**
  - [ ] 5 real photos with EXIF data
  - [ ] 5 AI-generated images
  - [ ] All saved in `images/` folder
- [ ] **Run `quick_start.py`** to verify setup
- [ ] **Run `demo_complete.py`** to verify complete workflow
- [ ] **Read `instructor_guide.md`** thoroughly
- [ ] **Prepare your own examples** for the warm-up question
- [ ] **Test internet connection** at venue (if using Colab or downloading TensorFlow)

## One Day Before

- [ ] **Print or share digitally:**
  - [ ] Student access to exercise files
  - [ ] SETUP.md for installation instructions
  - [ ] Link to Colab notebook (if using)

- [ ] **Prepare presentation/slides** (if using)
  - [ ] Example deepfakes for warm-up
  - [ ] Explanation slides for GANs/CNNs (optional)

- [ ] **Test WiFi at venue**
  - [ ] Can students download packages?
  - [ ] Can TensorFlow download weights?
  - [ ] Backup plan if WiFi fails?

- [ ] **Prepare backup materials**
  - [ ] USB drives with pre-installed packages (optional)
  - [ ] Offline copies of all files
  - [ ] Pre-downloaded TensorFlow weights (if possible)

## Morning of Workshop

- [ ] **Arrive early** (30-45 min before start)
- [ ] **Test projection/screen sharing**
- [ ] **Test live coding environment**
- [ ] **Verify internet connection**
- [ ] **Have `demo_complete.py` ready to run**
- [ ] **Open all exercise files** in advance
- [ ] **Prepare your "real vs. fake" poll images**

## Materials Checklist

### Digital Materials
- [ ] All `.py` exercise files
- [ ] `deepfakekit.py` library
- [ ] Sample images in `images/` folder
- [ ] README.md, SETUP.md, instructor_guide.md
- [ ] requirements.txt

### Physical Materials (Optional)
- [ ] Printed handouts with key concepts
- [ ] Notebook and pen for notes
- [ ] Extension cord / power strip for students' laptops
- [ ] Sticky notes for Q&A

### Backup Plan
- [ ] Offline installation packages (if WiFi unreliable)
- [ ] Pre-configured Colab notebooks
- [ ] Alternative exercises if TensorFlow fails

## During Workshop Timeline

### 0:00 - 0:08: Kickoff (8 min)
- [ ] Welcome students
- [ ] Warm-up question: "How can you tell if an image is fake?"
- [ ] Show 2-3 example images (real vs. AI)
- [ ] Quick poll
- [ ] Explain: GANs, metadata, CNNs (briefly)

**Be ready to:**
- Answer "What are deepfakes?"
- Explain why detection matters
- Set expectations for the hour

---

### 0:08 - 0:20: Exercise 1 - Metadata (12 min)
- [ ] Explain EXIF data concept
- [ ] Live demo: `kit.check_metadata()`
- [ ] Students work on `exercises/exercise_1_metadata.py`
- [ ] Walk around to help
- [ ] Discussion: Can metadata alone prove fakery?

**Watch for:**
- Students struggling with file paths
- Questions about missing EXIF in real photos
- Students finishing early → point to stretch challenges

---

### 0:20 - 0:35: Exercise 2 - Noise (15 min)
- [ ] Explain sensor noise concept
- [ ] Introduce sharpness (Laplacian)
- [ ] Live demo: `kit.noise_stats()`
- [ ] Students work on `exercises/exercise_2_noise.py`
- [ ] Discuss patterns they find

**Watch for:**
- OpenCV not installed (graceful fallback)
- Confusion about what sharpness means
- Questions about "too perfect" AI images

---

### 0:35 - 0:50: Exercise 3 - CNN (15 min)
- [ ] Explain CNNs (keep it simple!)
- [ ] Live demo: `kit.cnn_feature_intensity()`
- [ ] Live demo: `kit.plot_first_layer()` (visualizations!)
- [ ] Students work on `exercises/exercise_3_cnn.py`
- [ ] Discuss feature maps

**Watch for:**
- First TensorFlow run takes time (weights download)
- Students amazed by visualizations!
- Questions about what CNNs "see"

**If TensorFlow fails:**
- Skip to Exercise 4 using only metadata/noise
- Or switch to Colab

---

### 0:50 - 0:57: Exercise 4 - Ensemble (7 min)
- [ ] Explain ensemble concept
- [ ] Live demo: `kit.ensemble_flag()`
- [ ] Live demo: `kit.batch_ensemble()`
- [ ] Students run `exercises/exercise_4_ensemble.py`
- [ ] Show sorted results

**Watch for:**
- Excitement when everything comes together!
- Questions about tuning weights
- Students testing their own scoring functions

---

### 0:57 - 1:00: Wrap-Up (3 min)
- [ ] Reflection question: "What would you add to a detector?"
- [ ] Discuss limitations and ethics
- [ ] Encourage further learning
- [ ] Share resources
- [ ] Thank students!

**Final message:**
"Think critically about images you see online. The race between generators and detectors never ends, but now you understand how detection works!"

## Key Learning Objectives

By the end, students should be able to:
- [ ] Explain what EXIF metadata is and why it matters
- [ ] Understand how camera sensor noise differs from AI patterns
- [ ] Describe (at a high level) how CNNs detect patterns
- [ ] Combine multiple signals into an ensemble detector
- [ ] Think critically about deepfakes and detection

## Common Issues & Solutions

### "Module not found: deepfakekit"
**Solution:** Make sure `deepfakekit.py` is in the same folder or uploaded to Colab.

### "No images in folder"
**Solution:** Students need to create `images/` folder and add test images.

### "TensorFlow won't install"
**Solution:** Skip Exercise 3 or switch to Colab.

### Students finish at very different times
**Solution:**
- Fast: Stretch challenges in each exercise
- Slow: Skip Exercise 3, focus on ensemble

### WiFi dies
**Solution:**
- Switch to local installation (if packages pre-installed)
- Share one internet connection via hotspot
- Use pre-downloaded weights

### A student finds a bug
**Solution:**
- Acknowledge it! "Great debugging!"
- Fix it together or note it for later
- Turn it into a learning moment

## Post-Workshop

- [ ] Collect student feedback (quick survey)
  - What was most interesting?
  - What was confusing?
  - Too fast / too slow?

- [ ] Note what worked well
- [ ] Note what to improve
- [ ] Share success stories
- [ ] Update materials based on feedback

## Tips for Success

1. **Energy!** Keep it engaging and interactive
2. **Pace yourself** - it's easy to run long on CNN section
3. **Encourage questions** - pause frequently
4. **Celebrate discoveries** - when students find patterns
5. **Be flexible** - adjust pacing based on student engagement
6. **Have fun!** Your enthusiasm is contagious

## Emergency Contacts

- IT Support: _______________
- Venue Contact: _______________
- Your Contact: _______________

## Final Check (5 min before start)

- [ ] Laptop/computer working
- [ ] Projector/screen connected
- [ ] Internet working
- [ ] Demo ready to run
- [ ] Students have access to files
- [ ] Whiteboard/markers available (if using)
- [ ] Water bottle for you!
- [ ] Deep breath - you've got this! 💪

**You're ready! Have an amazing workshop!**
