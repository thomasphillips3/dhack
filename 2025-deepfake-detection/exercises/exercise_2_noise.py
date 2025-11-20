"""
Exercise 2: Noise & Sharpness Analysis (0:20 - 0:35)
====================================================

Goal: Understand how real camera sensor noise differs from AI-generated image patterns.

What you'll learn:
- What image noise is and why it matters
- How to measure sharpness using Laplacian variance
- How AI images have different noise characteristics than real photos

Time: ~15 minutes
"""

from deepfakekit import DeepfakeKit

# Initialize the DeepfakeKit
kit = DeepfakeKit()

print("=" * 60)
print("EXERCISE 2: NOISE & SHARPNESS ANALYSIS")
print("=" * 60)
print()

# CONCEPT: What is image noise?
# ==============================
print("CONCEPT CHECK:")
print("-" * 60)
print("Real cameras have physical sensors that introduce natural 'noise'")
print("(random pixel variations). AI generators create mathematically")
print("'perfect' pixels that can look too smooth or have unusual patterns.")
print()
print("We measure two things:")
print("  1. SHARPNESS (Laplacian variance) - How crisp are the edges?")
print("  2. NOISE LEVEL (grayscale std dev) - How much natural variation?")
print()

# TODO 1: Analyze a single image
# ===============================
image_path = 'images/sample.jpg'

print(f"Analyzing: {image_path}")
print("-" * 60)

result = kit.noise_stats(image_path)

print(f"\nNOISE STATISTICS:")
print(f"  Sharpness (Laplacian): {result.sharpness_laplacian:.2f}" if result.sharpness_laplacian else "  Sharpness: N/A")
print(f"  Noise Level (Std Dev): {result.grayscale_std:.2f}" if result.grayscale_std else "  Noise: N/A")

if result.notes:
    print(f"\nNotes: {', '.join(result.notes)}")

print()

# INTERPRETATION GUIDE:
# =====================
print("INTERPRETATION:")
print("-" * 60)
print("Sharpness (Laplacian variance):")
print("  - Higher values (>100) = very sharp, crisp edges")
print("  - Medium values (20-100) = normal photo sharpness")
print("  - Low values (<20) = blurry or overly smooth (suspicious!)")
print()
print("Noise Level (Standard Deviation):")
print("  - Higher values (>30) = lots of natural sensor noise")
print("  - Low values (<20) = too 'clean' (might be AI-generated)")
print()

# QUESTION 1: Based on these values, does this image seem real or AI-generated?
# Write your answer here:
# Answer: _______________________________________________________________
# ________________________________________________________________________

print()
print("=" * 60)
print()

# TODO 2: Compare real vs. AI-generated images
# =============================================
print("COMPARING REAL vs. AI IMAGES:")
print("-" * 60)

test_images = [
    'images/sample.jpg',
    # Add more images here:
    # 'images/real_photo_1.jpg',
    # 'images/ai_generated_1.jpg',
    # 'images/real_photo_2.jpg',
    # 'images/ai_generated_2.jpg',
]

results_table = []

for img_path in test_images:
    try:
        result = kit.noise_stats(img_path)

        # Determine if sharpness is suspicious
        sharpness_flag = ""
        if result.sharpness_laplacian:
            if result.sharpness_laplacian < 20:
                sharpness_flag = "⚠️  TOO SMOOTH"
            elif result.sharpness_laplacian > 100:
                sharpness_flag = "✓ SHARP"
            else:
                sharpness_flag = "✓ Normal"

        # Determine if noise level is suspicious
        noise_flag = ""
        if result.grayscale_std:
            if result.grayscale_std < 20:
                noise_flag = "⚠️  TOO CLEAN"
            else:
                noise_flag = "✓ Natural"

        results_table.append({
            'path': img_path,
            'sharpness': result.sharpness_laplacian,
            'noise': result.grayscale_std,
            'sharpness_flag': sharpness_flag,
            'noise_flag': noise_flag
        })

    except FileNotFoundError:
        print(f"ERROR: {img_path} not found!")

# Print results table
print("\nRESULTS TABLE:")
print("-" * 60)
print(f"{'Image':<30} {'Sharpness':<12} {'Noise':<12} {'Assessment'}")
print("-" * 60)

for r in results_table:
    sharpness_str = f"{r['sharpness']:.1f}" if r['sharpness'] else "N/A"
    noise_str = f"{r['noise']:.1f}" if r['noise'] else "N/A"
    assessment = f"{r['sharpness_flag']} {r['noise_flag']}"

    # Truncate long paths
    path_short = r['path'].split('/')[-1][:28]
    print(f"{path_short:<30} {sharpness_str:<12} {noise_str:<12} {assessment}")

print()

# QUESTION 2: What patterns do you notice between real and AI images?
# Write your answer here:
# Answer: _______________________________________________________________
# ________________________________________________________________________

print()
print("=" * 60)
print()

# TODO 3: Find the "most suspicious" image
# =========================================
print("FINDING THE MOST SUSPICIOUS IMAGE:")
print("-" * 60)

# Score each image based on how suspicious it looks
# (Low sharpness + low noise = high suspicion)

for r in results_table:
    suspicion_score = 0

    if r['sharpness'] and r['sharpness'] < 20:
        suspicion_score += 1

    if r['noise'] and r['noise'] < 20:
        suspicion_score += 1

    r['suspicion'] = suspicion_score

# Sort by suspicion score
results_table.sort(key=lambda x: x['suspicion'], reverse=True)

print("\nMOST SUSPICIOUS IMAGES (ranked):")
for i, r in enumerate(results_table[:3], 1):
    path_short = r['path'].split('/')[-1]
    print(f"  {i}. {path_short} (suspicion score: {r['suspicion']}/2)")

print()

# QUESTION 3: Why might some AI images still pass these tests?
# Write your answer here:
# Answer: _______________________________________________________________
# ________________________________________________________________________

print()
print("CHALLENGE:")
print("-" * 60)
print("If you were training an AI to generate fake images that pass")
print("these noise tests, what would you add to make them look more real?")
print()
print("Your ideas:")
print("1. _______________________________________________________________")
print("2. _______________________________________________________________")
print()

# STRETCH CHALLENGE:
# ==================
# Calculate the average sharpness for real vs. AI images
print("STRETCH: Calculate category averages...")
print("-" * 60)

# TODO: Separate your images into 'real' and 'ai' categories and compare averages
# Your code here:

# real_images = [...]
# ai_images = [...]
#
# real_sharpness_avg = ...
# ai_sharpness_avg = ...
#
# print(f"Average sharpness - Real: {real_sharpness_avg:.1f}")
# print(f"Average sharpness - AI:   {ai_sharpness_avg:.1f}")

print()
print("Exercise 2 complete! Move on to exercise_3_cnn.py")
print("=" * 60)
