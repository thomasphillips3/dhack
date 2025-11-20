"""
Exercise 1: Metadata Forensics (0:08 - 0:20)
============================================

Goal: Learn how to inspect image metadata (EXIF data) to find clues about whether
      an image came from a real camera or was AI-generated.

What you'll learn:
- What EXIF data is and why it matters
- How to detect missing camera information
- How to spot AI generation hints in metadata

Time: ~12 minutes
"""

from deepfakekit import DeepfakeKit

# Initialize the DeepfakeKit
kit = DeepfakeKit()

print("=" * 60)
print("EXERCISE 1: METADATA FORENSICS")
print("=" * 60)
print()

# TODO 1: Check a single image's metadata
# ========================================
# Replace 'images/sample.jpg' with the path to one of your test images
image_path = 'images/sample.jpg'

print(f"Analyzing: {image_path}")
print("-" * 60)

# Call check_metadata() to analyze the image
result = kit.check_metadata(image_path)

# Print the flags (suspicious indicators)
print("\nSUSPICIOUS FLAGS:")
print(f"  No EXIF data found:       {result.flags['no_exif']}")
print(f"  Missing camera info:      {result.flags['missing_camera']}")
print(f"  AI generator hint found:  {result.flags['has_ai_generator_hint']}")

# Print some of the actual metadata tags
print("\nSAMPLE METADATA TAGS:")
for key, value in list(result.tags.items())[:5]:  # Show first 5 tags
    print(f"  {key}: {value}")

print()

# QUESTION 1: What do the flags tell you about this image?
# Write your answer here:
# Answer: _______________________________________________________________
# ________________________________________________________________________

print()
print("=" * 60)
print()

# TODO 2: Compare multiple images
# ================================
# Now let's check several images and compare their metadata

test_images = [
    'images/sample.jpg',
    # Add more image paths here:
    # 'images/real_photo.jpg',
    # 'images/ai_generated.jpg',
]

print("COMPARING MULTIPLE IMAGES:")
print("-" * 60)

for img_path in test_images:
    try:
        result = kit.check_metadata(img_path)

        # Count how many red flags this image has
        red_flags = sum([
            result.flags['no_exif'],
            result.flags['missing_camera'],
            result.flags['has_ai_generator_hint']
        ])

        print(f"\n{img_path}")
        print(f"  Red flags: {red_flags}/3")
        print(f"  Tags found: {len(result.tags)}")

        # Show if it has camera make/model
        camera_make = None
        for key, value in result.tags.items():
            if 'make' in key.lower():
                camera_make = value
                break

        if camera_make:
            print(f"  Camera: {camera_make}")
        else:
            print(f"  Camera: NOT FOUND")

    except FileNotFoundError:
        print(f"\n{img_path}")
        print(f"  ERROR: File not found!")

print()
print("=" * 60)
print()

# QUESTION 2: Which images appear to be AI-generated based on metadata?
# Write your answer here:
# Answer: _______________________________________________________________
# ________________________________________________________________________

# QUESTION 3: Can metadata alone definitively prove an image is fake? Why or why not?
# Write your answer here:
# Answer: _______________________________________________________________
# ________________________________________________________________________

print()
print("CHALLENGE:")
print("-" * 60)
print("Research: What are some ways that AI generators could fake")
print("EXIF data to make their images look real?")
print()
print("Your ideas:")
print("1. _______________________________________________________________")
print("2. _______________________________________________________________")
print("3. _______________________________________________________________")
print()

# STRETCH CHALLENGE:
# ==================
# Write code to find images with NO metadata at all:

print("STRETCH: Finding images with no metadata...")
print("-" * 60)

# TODO: Loop through all images and find ones with result.flags['no_exif'] == True
# Your code here:

# for img_path in test_images:
#     result = kit.check_metadata(img_path)
#     if result.flags['no_exif']:
#         print(f"  {img_path} has NO EXIF data!")

print()
print("Exercise 1 complete! Move on to exercise_2_noise.py")
print("=" * 60)
