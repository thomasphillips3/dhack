"""
Exercise 3: CNN Visualization (0:35 - 0:50)
===========================================

Goal: Understand how Convolutional Neural Networks "see" images and detect patterns
      that humans can't easily spot.

What you'll learn:
- What CNNs are and how they work
- How to extract feature vectors from images
- How to visualize what the AI is "looking at"

Time: ~15 minutes

NOTE: This exercise requires TensorFlow. If it's not installed:
      !pip install tensorflow opencv-python matplotlib
"""

from deepfakekit import DeepfakeKit

# Initialize the DeepfakeKit
kit = DeepfakeKit()

print("=" * 60)
print("EXERCISE 3: CNN VISUALIZATION")
print("=" * 60)
print()

# CONCEPT: What is a CNN?
# =======================
print("CONCEPT CHECK:")
print("-" * 60)
print("A Convolutional Neural Network (CNN) is like having millions of")
print("tiny pattern detectors looking at your image. The first layers")
print("detect simple things (edges, colors), while deeper layers detect")
print("complex things (faces, objects, artistic styles).")
print()
print("We're using MobileNetV2, a CNN trained on millions of real photos.")
print("It 'knows' what real images should look like, so AI-generated")
print("images will produce different patterns.")
print()
print("Loading MobileNetV2... (this may take a moment)")
print()

# TODO 1: Extract CNN features from a single image
# =================================================
image_path = 'images/sample.jpg'

print(f"Analyzing: {image_path}")
print("-" * 60)

try:
    result = kit.cnn_feature_intensity(image_path)

    print(f"\nCNN FEATURE INTENSITY: {result.feature_intensity:.2f}")

    if result.notes:
        print(f"Notes: {', '.join(result.notes)}")

    print()
    print("INTERPRETATION:")
    print("-" * 60)
    print("Feature intensity measures how 'strongly' the CNN responds to")
    print("the image. Higher values mean the image has patterns the CNN")
    print("recognizes from its training on real photos.")
    print()
    print("  - High intensity (>50):   CNN sees familiar 'real photo' patterns")
    print("  - Medium intensity (30-50): Unclear")
    print("  - Low intensity (<30):    Unusual patterns (might be AI-generated)")
    print()

    # QUESTION 1: What does the feature intensity suggest about this image?
    print("QUESTION 1: What does the feature intensity suggest about this image?")
    print("Answer: _______________________________________________________________")
    print()

except Exception as e:
    print(f"ERROR: {e}")
    print("Make sure TensorFlow is installed: pip install tensorflow")

print()
print("=" * 60)
print()

# TODO 2: Visualize what the CNN "sees"
# ======================================
print("VISUALIZING CNN FEATURE MAPS:")
print("-" * 60)
print("Let's look at what the FIRST layer of the CNN detects.")
print("These are like edge detectors and color filters.")
print()

try:
    # This will show 6 feature maps (what 6 different filters detected)
    print(f"Generating feature map visualizations for: {image_path}")
    print("(Close the plot windows to continue)")
    print()

    kit.plot_first_layer(image_path, channels=6)

    print()
    print("What did you see?")
    print("-" * 60)
    print("Each feature map shows what ONE filter detected:")
    print("  - Bright areas = filter activated (detected something)")
    print("  - Dark areas = filter didn't activate")
    print()
    print("Common patterns:")
    print("  - Vertical/horizontal edges")
    print("  - Diagonal lines")
    print("  - Color blobs")
    print("  - Texture patterns")
    print()

    # QUESTION 2: Which feature maps showed the strongest activation?
    print("QUESTION 2: Which feature maps showed the strongest activation?")
    print("Answer: _______________________________________________________________")
    print()

except Exception as e:
    print(f"ERROR: {e}")
    print("Make sure matplotlib is installed: pip install matplotlib")

print()
print("=" * 60)
print()

# TODO 3: Compare CNN features across multiple images
# ===================================================
print("COMPARING CNN FEATURES:")
print("-" * 60)

test_images = [
    'images/sample.jpg',
    # Add more images here:
    # 'images/real_photo_1.jpg',
    # 'images/ai_generated_1.jpg',
    # 'images/real_photo_2.jpg',
    # 'images/ai_generated_2.jpg',
]

print("\nExtracting features from all images...")
print("(This may take a minute)")
print()

feature_results = []

for img_path in test_images:
    try:
        result = kit.cnn_feature_intensity(img_path)

        # Classify based on intensity
        if result.feature_intensity:
            if result.feature_intensity > 50:
                classification = "✓ LIKELY REAL"
            elif result.feature_intensity > 30:
                classification = "? UNCERTAIN"
            else:
                classification = "⚠️  SUSPICIOUS"
        else:
            classification = "ERROR"

        feature_results.append({
            'path': img_path,
            'intensity': result.feature_intensity,
            'classification': classification
        })

        # Show progress
        path_short = img_path.split('/')[-1]
        intensity_str = f"{result.feature_intensity:.1f}" if result.feature_intensity else "N/A"
        print(f"  {path_short:<30} Intensity: {intensity_str:<8} {classification}")

    except FileNotFoundError:
        print(f"  ERROR: {img_path} not found!")
    except Exception as e:
        print(f"  ERROR processing {img_path}: {e}")

print()

# QUESTION 3: Do the CNN results align with the metadata/noise results?
print("QUESTION 3: Do the CNN results align with your earlier findings?")
print("Answer: _______________________________________________________________")
print("________________________________________________________________________")
print()

print()
print("=" * 60)
print()

# TODO 4: Visualize multiple images side-by-side
# ===============================================
print("CHALLENGE: Compare feature maps side-by-side")
print("-" * 60)
print("Pick a real photo and an AI-generated image, then visualize both.")
print("What differences do you notice in their feature maps?")
print()

# Uncomment and modify these lines:
# print("Real photo feature maps:")
# kit.plot_first_layer('images/real_photo.jpg', channels=6)
# print("\nAI-generated feature maps:")
# kit.plot_first_layer('images/ai_generated.jpg', channels=6)

print("Your observations:")
print("1. _______________________________________________________________")
print("2. _______________________________________________________________")
print("3. _______________________________________________________________")
print()

print()
print("DEEP DIVE:")
print("-" * 60)
print("Why do you think CNNs can sometimes detect deepfakes that look")
print("perfect to human eyes?")
print()
print("Hint: Think about what patterns the CNN was trained to recognize.")
print()
print("Your answer:")
print("___________________________________________________________________")
print("___________________________________________________________________")
print("___________________________________________________________________")
print()

# STRETCH CHALLENGE:
# ==================
print("STRETCH CHALLENGE:")
print("-" * 60)
print("The feature intensity is just ONE number summarizing ALL the CNN's")
print("activations. Can you think of other statistics we could compute?")
print()
print("Ideas:")
print("1. _______________________________________________________________")
print("2. _______________________________________________________________")
print()

print()
print("Exercise 3 complete! Move on to exercise_4_ensemble.py")
print("=" * 60)
