"""
Quick Start: Test Your Setup
=============================

Run this script to verify everything is installed correctly.
This will test all components of the DeepfakeKit.

Usage:
    python quick_start.py
"""

from deepfakekit import DeepfakeKit
import os

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_installation():
    """Test that all components are working"""
    print_header("DEEPFAKE DETECTION - QUICK START TEST")

    # Check for images folder
    if not os.path.exists('images'):
        print("\n⚠️  WARNING: 'images' folder not found!")
        print("Creating 'images' folder...")
        os.makedirs('images')
        print("\n📝 Next step: Add some test images to the 'images' folder")
        print("   - 5 real photos (from a camera)")
        print("   - 5 AI-generated images")
        print("\nThen run this script again!")
        return

    # Check if there are any images
    image_files = [f for f in os.listdir('images')
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    if not image_files:
        print("\n⚠️  WARNING: No images found in 'images' folder!")
        print("\n📝 Next step: Add some test images:")
        print("   - Real photos: Take pictures with your phone")
        print("   - AI images: Generate with Gemini, DALL-E, etc.")
        print("\nThen run this script again!")
        return

    print(f"\n✓ Found {len(image_files)} images in 'images' folder")

    # Initialize DeepfakeKit
    print("\nInitializing DeepfakeKit...")
    kit = DeepfakeKit()
    print("✓ DeepfakeKit ready!")

    # Test with first image
    test_image = os.path.join('images', image_files[0])
    print(f"\nTesting with: {test_image}")

    # Test 1: Metadata
    print("\n" + "-" * 60)
    print("TEST 1: Metadata Analysis")
    print("-" * 60)
    try:
        result = kit.check_metadata(test_image)
        print("✓ Metadata analysis: WORKING")
        print(f"  - EXIF tags found: {len(result.tags)}")
        print(f"  - Suspicious flags: {sum(result.flags.values())}")
    except Exception as e:
        print(f"✗ Metadata analysis: FAILED")
        print(f"  Error: {e}")
        return

    # Test 2: Noise Analysis
    print("\n" + "-" * 60)
    print("TEST 2: Noise Analysis")
    print("-" * 60)
    try:
        result = kit.noise_stats(test_image)
        print("✓ Noise analysis: WORKING")
        if result.sharpness_laplacian:
            print(f"  - Sharpness: {result.sharpness_laplacian:.2f}")
        if result.grayscale_std:
            print(f"  - Noise level: {result.grayscale_std:.2f}")
        if result.notes:
            print(f"  - Notes: {', '.join(result.notes)}")
    except Exception as e:
        print(f"✗ Noise analysis: FAILED")
        print(f"  Error: {e}")
        return

    # Test 3: CNN Analysis
    print("\n" + "-" * 60)
    print("TEST 3: CNN Analysis (this may take a minute...)")
    print("-" * 60)
    try:
        result = kit.cnn_feature_intensity(test_image)
        print("✓ CNN analysis: WORKING")
        if result.feature_intensity:
            print(f"  - Feature intensity: {result.feature_intensity:.2f}")
        if result.notes:
            print(f"  - Notes: {', '.join(result.notes)}")
    except Exception as e:
        print(f"✗ CNN analysis: FAILED")
        print(f"  Error: {e}")
        print("\n  This is OK if TensorFlow isn't installed.")
        print("  You can still use exercises 1-2 without it!")
        print("  To install: pip install tensorflow")

    # Test 4: Ensemble
    print("\n" + "-" * 60)
    print("TEST 4: Ensemble Detection")
    print("-" * 60)
    try:
        result = kit.ensemble_flag(test_image)
        print("✓ Ensemble detection: WORKING")
        print(f"  - Total score: {result['total_score']:.2f}")
        verdict = "LIKELY FAKE" if result['likely_fake'] else "Likely real"
        print(f"  - Verdict: {verdict}")
    except Exception as e:
        print(f"✗ Ensemble detection: FAILED")
        print(f"  Error: {e}")
        return

    # Success!
    print_header("✓ ALL TESTS PASSED!")
    print("\n🎉 Your setup is ready!")
    print("\nNext steps:")
    print("  1. Read README.md for workshop overview")
    print("  2. Start with exercise_1_metadata.py")
    print("  3. Work through exercises 2-4 in order")
    print("\nInstructors:")
    print("  - Read instructor_guide.md for teaching notes")
    print("  - Run demo_complete.py for a full demonstration")
    print("\nHave fun detecting deepfakes! 🔍\n")

if __name__ == "__main__":
    try:
        test_installation()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ UNEXPECTED ERROR: {e}")
        print("\nPlease check:")
        print("  1. Is Python 3.8+ installed? (python --version)")
        print("  2. Are packages installed? (pip install -r requirements.txt)")
        print("  3. Is deepfakekit.py in the current folder?")
        print("\nIf problems persist, see SETUP.md for troubleshooting.")
