"""
Complete Deepfake Detection Demo
=================================

This script demonstrates the full deepfake detection pipeline.
Use this for:
  - Instructor demonstrations
  - Quick testing
  - Understanding the complete workflow

Author: Detroit Hackathon 2025
"""

from deepfakekit import DeepfakeKit
import json

def print_section(title):
    """Helper to print section headers"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def print_subsection(title):
    """Helper to print subsection headers"""
    print(f"\n{title}")
    print("-" * 70)

def analyze_single_image(kit, image_path):
    """
    Run complete analysis on a single image.

    Args:
        kit: DeepfakeKit instance
        image_path: Path to image file
    """
    print_section(f"ANALYZING: {image_path}")

    # 1. Metadata Analysis
    print_subsection("1. METADATA ANALYSIS")
    meta = kit.check_metadata(image_path)

    print("Suspicious flags:")
    for flag, value in meta.flags.items():
        indicator = "⚠️  YES" if value else "✓ No"
        print(f"  {flag:25s} {indicator}")

    print(f"\nTotal EXIF tags found: {len(meta.tags)}")

    # Show some interesting tags
    interesting_tags = ['Image Make', 'Image Model', 'DateTime', 'Software']
    print("\nKey metadata:")
    for tag in interesting_tags:
        value = meta.tags.get(tag, 'Not found')
        print(f"  {tag:20s} {value}")

    # 2. Noise Analysis
    print_subsection("2. NOISE ANALYSIS")
    noise = kit.noise_stats(image_path)

    if noise.sharpness_laplacian is not None:
        sharpness_assessment = "TOO SMOOTH (suspicious)" if noise.sharpness_laplacian < 20 else "Normal"
        print(f"Sharpness (Laplacian):  {noise.sharpness_laplacian:8.2f} → {sharpness_assessment}")
    else:
        print("Sharpness: Could not compute")

    if noise.grayscale_std is not None:
        noise_assessment = "TOO CLEAN (suspicious)" if noise.grayscale_std < 20 else "Normal"
        print(f"Noise Level (Std Dev):  {noise.grayscale_std:8.2f} → {noise_assessment}")
    else:
        print("Noise: Could not compute")

    if noise.notes:
        print(f"\nNotes: {', '.join(noise.notes)}")

    # 3. CNN Analysis
    print_subsection("3. CNN FEATURE ANALYSIS")
    try:
        cnn = kit.cnn_feature_intensity(image_path)

        if cnn.feature_intensity is not None:
            if cnn.feature_intensity > 50:
                cnn_assessment = "Strong match to real photos"
            elif cnn.feature_intensity > 30:
                cnn_assessment = "Uncertain"
            else:
                cnn_assessment = "UNUSUAL PATTERNS (suspicious)"

            print(f"Feature Intensity:      {cnn.feature_intensity:8.2f} → {cnn_assessment}")
        else:
            print("CNN analysis failed")

        if cnn.notes:
            print(f"Notes: {', '.join(cnn.notes)}")

    except Exception as e:
        print(f"CNN analysis not available: {e}")
        print("(Install TensorFlow to enable: pip install tensorflow)")

    # 4. Ensemble Decision
    print_subsection("4. ENSEMBLE VERDICT")
    result = kit.ensemble_flag(image_path)

    print(f"Combined Score:         {result['total_score']:8.2f}")
    print(f"Threshold:              0.70")
    print()

    if result['likely_fake']:
        print("🚨 VERDICT: LIKELY FAKE")
        print("\nReasons:")
        if result['metadata']['no_exif']:
            print("  - No EXIF data found")
        if result['metadata']['missing_camera']:
            print("  - Missing camera information")
        if result['metadata']['has_ai_generator_hint']:
            print("  - AI generator detected in metadata")
        if result['noise']['sharpness_laplacian'] and result['noise']['sharpness_laplacian'] < 20:
            print("  - Image too smooth/blurry")
        if result['cnn']['feature_intensity'] and result['cnn']['feature_intensity'] < 30:
            print("  - Unusual CNN patterns")
    else:
        print("✓ VERDICT: LIKELY REAL")
        print("\nThis image passes most authenticity checks.")

    print()
    return result

def batch_analyze_folder(kit, folder_path):
    """
    Analyze all images in a folder and generate a summary report.

    Args:
        kit: DeepfakeKit instance
        folder_path: Path to folder containing images
    """
    print_section(f"BATCH ANALYSIS: {folder_path}")

    results = kit.batch_ensemble(folder_path)

    if not results:
        print("No images found in folder!")
        return

    print(f"Processed {len(results)} images\n")

    # Sort by suspicion score
    results.sort(key=lambda r: r.get('total_score', 0), reverse=True)

    # Print summary table
    print_subsection("RESULTS TABLE")
    print(f"{'Image':<30} {'Score':<8} {'Verdict':<15} {'Key Flags'}")
    print("-" * 70)

    for r in results:
        if 'error' in r:
            path_short = r['path'].split('/')[-1][:28]
            print(f"{path_short:<30} ERROR: {r['error']}")
            continue

        path_short = r['path'].split('/')[-1][:28]
        score = r.get('total_score', 0)
        verdict = "🚨 FAKE" if r.get('likely_fake') else "✓ Real"

        # Key flags
        flags = []
        if r['metadata'].get('no_exif'):
            flags.append("no_exif")
        if r['metadata'].get('has_ai_generator_hint'):
            flags.append("AI_hint")
        if r['noise']['sharpness_laplacian'] and r['noise']['sharpness_laplacian'] < 20:
            flags.append("smooth")

        flags_str = ", ".join(flags) if flags else "-"

        print(f"{path_short:<30} {score:<8.2f} {verdict:<15} {flags_str}")

    # Statistics
    print_subsection("SUMMARY STATISTICS")

    num_fake = sum(1 for r in results if r.get('likely_fake', False))
    num_real = len(results) - num_fake
    avg_score = sum(r.get('total_score', 0) for r in results) / len(results)

    print(f"Total images:        {len(results)}")
    print(f"Flagged as fake:     {num_fake} ({num_fake/len(results)*100:.1f}%)")
    print(f"Flagged as real:     {num_real} ({num_real/len(results)*100:.1f}%)")
    print(f"Average score:       {avg_score:.2f}")

    # Show most suspicious
    print_subsection("TOP 3 MOST SUSPICIOUS")
    for i, r in enumerate(results[:3], 1):
        if 'error' not in r:
            path_short = r['path'].split('/')[-1]
            score = r.get('total_score', 0)
            print(f"{i}. {path_short} (score: {score:.2f})")

    print()

def main():
    """Main demonstration function"""
    print("=" * 70)
    print("  DEEPFAKE DETECTION DEMO")
    print("  Detroit Hackathon 2025")
    print("=" * 70)

    # Initialize the kit
    print("\nInitializing DeepfakeKit...")
    kit = DeepfakeKit()
    print("Ready!\n")

    # Demo 1: Single image analysis
    print("\n" + "=" * 70)
    print("DEMO 1: SINGLE IMAGE ANALYSIS")
    print("=" * 70)

    image_path = 'images/sample.jpg'
    try:
        analyze_single_image(kit, image_path)
    except FileNotFoundError:
        print(f"\nERROR: {image_path} not found!")
        print("Please create an 'images' folder with sample images.")
        print("\nFor now, skipping to batch demo...\n")

    # Demo 2: Batch analysis
    print("\n" + "=" * 70)
    print("DEMO 2: BATCH FOLDER ANALYSIS")
    print("=" * 70)

    folder_path = 'images'
    try:
        batch_analyze_folder(kit, folder_path)
    except FileNotFoundError:
        print(f"\nERROR: {folder_path} folder not found!")
        print("Create an 'images' folder and add test images to run batch analysis.")

    # Wrap up
    print_section("DEMO COMPLETE")
    print("Key takeaways:")
    print("  1. Metadata can reveal AI generation (missing EXIF, camera info)")
    print("  2. Noise patterns differ between real cameras and AI generators")
    print("  3. CNNs can detect subtle patterns humans can't see")
    print("  4. Ensemble methods combine signals for better accuracy")
    print()
    print("Remember: This is a teaching tool, not production-grade forensics!")
    print()

if __name__ == "__main__":
    main()
