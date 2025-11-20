"""
Exercise 4: Ensemble Detection (0:50 - 0:57)
============================================

Goal: Combine all detection methods into a single powerful detector that's better
      than any individual method alone.

What you'll learn:
- How to combine multiple signals (metadata, noise, CNN)
- How ensemble methods improve accuracy
- How to scan entire folders of images

Time: ~7 minutes
"""

from deepfakekit import DeepfakeKit
import json

# Initialize the DeepfakeKit
kit = DeepfakeKit()

print("=" * 60)
print("EXERCISE 4: ENSEMBLE DETECTION")
print("=" * 60)
print()

# CONCEPT: What is ensemble detection?
# =====================================
print("CONCEPT CHECK:")
print("-" * 60)
print("An ENSEMBLE combines multiple detection methods to make a final")
print("decision. Think of it like asking multiple experts and voting.")
print()
print("We combine:")
print("  1. Metadata analysis (EXIF data)")
print("  2. Noise analysis (sharpness, patterns)")
print("  3. CNN features (deep learning)")
print()
print("Each method gets a 'weight' - how much we trust it.")
print()

# TODO 1: Run ensemble detection on a single image
# =================================================
image_path = 'images/sample.jpg'

print(f"Running full ensemble on: {image_path}")
print("-" * 60)

result = kit.ensemble_flag(image_path)

# Pretty-print the full result
print("\nFULL ANALYSIS RESULTS:")
print(json.dumps(result, indent=2))

print()
print("UNDERSTANDING THE OUTPUT:")
print("-" * 60)
print(f"Metadata flags:     {result['metadata']}")
print(f"Noise stats:        {result['noise']}")
print(f"CNN intensity:      {result['cnn']['feature_intensity']}")
print(f"Total score:        {result['total_score']:.2f}")
print(f"VERDICT:            {'🚨 LIKELY FAKE' if result['likely_fake'] else '✓ Likely real'}")
print()

# QUESTION 1: How does the total score combine the different signals?
print("QUESTION 1: How is the total score calculated? (Look at the code!)")
print("Answer: _______________________________________________________________")
print("________________________________________________________________________")
print()

print()
print("=" * 60)
print()

# TODO 2: Batch process an entire folder
# =======================================
print("BATCH PROCESSING:")
print("-" * 60)
print("Now let's scan an entire folder of images at once.")
print()

folder_path = 'images'

print(f"Scanning folder: {folder_path}")
print("(This may take a minute for the first run)")
print()

try:
    results = kit.batch_ensemble(folder_path)

    print(f"Processed {len(results)} images\n")

    # Sort by suspicion (highest score = most suspicious)
    results.sort(key=lambda r: r.get('total_score', 0), reverse=True)

    # Display results table
    print("RESULTS (sorted by suspicion):")
    print("-" * 90)
    print(f"{'Image':<25} {'Total Score':<12} {'Verdict':<15} {'Key Flags'}")
    print("-" * 90)

    for r in results:
        if 'error' in r:
            path_short = r['path'].split('/')[-1][:23]
            print(f"{path_short:<25} ERROR: {r['error']}")
            continue

        path_short = r['path'].split('/')[-1][:23]
        score = r.get('total_score', 0)
        verdict = "🚨 LIKELY FAKE" if r.get('likely_fake') else "✓ Likely real"

        # Highlight key flags
        key_flags = []
        if r['metadata'].get('no_exif'):
            key_flags.append("no_exif")
        if r['metadata'].get('has_ai_generator_hint'):
            key_flags.append("AI_hint")
        if r['noise']['sharpness_laplacian'] and r['noise']['sharpness_laplacian'] < 20:
            key_flags.append("low_sharp")

        flags_str = ", ".join(key_flags) if key_flags else "none"

        print(f"{path_short:<25} {score:<12.2f} {verdict:<15} {flags_str}")

    print()

    # Summary statistics
    num_fake = sum(1 for r in results if r.get('likely_fake', False))
    num_real = len(results) - num_fake

    print("SUMMARY:")
    print("-" * 60)
    print(f"Total images:     {len(results)}")
    print(f"Likely real:      {num_real}")
    print(f"Likely fake:      {num_fake}")
    print(f"Detection rate:   {num_fake / len(results) * 100:.1f}% flagged as fake")
    print()

except FileNotFoundError:
    print(f"ERROR: Folder '{folder_path}' not found!")
    print("Create an 'images' folder and add some test images.")

print()
print("=" * 60)
print()

# QUESTION 2: Which images were flagged as fake? Do you agree?
print("QUESTION 2: List the top 3 images flagged as fake:")
print("1. _______________________________________________________________")
print("2. _______________________________________________________________")
print("3. _______________________________________________________________")
print()
print("Do you agree with the detector's assessment? Why or why not?")
print("________________________________________________________________________")
print()

# TODO 3: Tune the ensemble weights
# ==================================
print("TUNING THE ENSEMBLE:")
print("-" * 60)
print("The ensemble uses default weights:")
print("  - Metadata weight: 0.7 (70%)")
print("  - CNN weight:      0.3 (30%)")
print()
print("Let's try different weights and see what happens.")
print()

# Try with different weights
image_path = 'images/sample.jpg'

print(f"Testing different weights on: {image_path}")
print()

weight_configs = [
    (0.7, 0.3, "Default (trust metadata more)"),
    (0.5, 0.5, "Balanced (equal trust)"),
    (0.3, 0.7, "CNN-heavy (trust AI more)"),
]

for meta_w, cnn_w, description in weight_configs:
    result = kit.ensemble_flag(
        image_path,
        meta_weight=meta_w,
        cnn_weight=cnn_w
    )

    verdict = "FAKE" if result['likely_fake'] else "REAL"
    print(f"{description}")
    print(f"  Weights: meta={meta_w}, cnn={cnn_w}")
    print(f"  Score: {result['total_score']:.2f} → {verdict}")
    print()

# QUESTION 3: How do different weights change the results?
print("QUESTION 3: Which weight configuration seems most accurate for your")
print("            test images? Why?")
print("Answer: _______________________________________________________________")
print("________________________________________________________________________")
print()

print()
print("=" * 60)
print()

# CHALLENGE: Build your own scoring function
# ===========================================
print("CHALLENGE: Custom Scoring Function")
print("-" * 60)
print("Create your own function that combines the signals differently.")
print()
print("Example starter code:")
print()
print("def my_detector(result):")
print("    score = 0")
print("    if result['metadata']['no_exif']:")
print("        score += 1.0")
print("    if result['noise']['sharpness_laplacian'] < 20:")
print("        score += 0.5")
print("    # Add your own logic here!")
print("    return score > 1.0  # True if likely fake")
print()

# TODO: Write your custom detector here:

def my_detector(result):
    """
    Your custom deepfake detector!

    Args:
        result: The output from kit.ensemble_flag()

    Returns:
        True if likely fake, False if likely real
    """
    score = 0

    # Your scoring logic here:
    # ...

    return score > 1.0  # Adjust threshold as needed


# Test your detector
print("Testing your custom detector:")
try:
    result = kit.ensemble_flag(image_path)
    my_verdict = my_detector(result)
    print(f"Your detector says: {'FAKE' if my_verdict else 'REAL'}")
    print(f"Ensemble says:      {'FAKE' if result['likely_fake'] else 'REAL'}")
except Exception as e:
    print(f"Error: {e}")

print()

print()
print("REFLECTION:")
print("-" * 60)
print("1. What are the strengths of ensemble detection?")
print("   _______________________________________________________________")
print()
print("2. What are the limitations? (What could fool it?)")
print("   _______________________________________________________________")
print()
print("3. If you had more time, what other signals would you add?")
print("   _______________________________________________________________")
print()

print()
print("=" * 60)
print("Exercise 4 complete! You've built a complete deepfake detector!")
print("=" * 60)
