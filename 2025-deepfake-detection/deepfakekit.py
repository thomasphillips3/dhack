"""
deepfakekit.py — A tiny helper API for teaching deepfake detection quickly.

Usage (quickstart):
-------------------
from deepfakekit import DeepfakeKit

k = DeepfakeKit()
r = k.check_metadata('images/sample.jpg')
print(r.flags)

score = k.cnn_feature_intensity('images/sample.jpg')  # requires tensorflow
k.plot_first_layer('images/sample.jpg')               # optional visualization

flags = k.ensemble_flag('images/sample.jpg')
print(flags)
"""
from __future__ import annotations
import os
import io
import math
import json
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple, List

try:
    from PIL import Image, ImageStat, ImageOps
except Exception as e:
    raise RuntimeError("Pillow (PIL) is required. Try: pip install pillow") from e

try:
    import exifread
    _HAS_EXIFREAD = True
except Exception:
    _HAS_EXIFREAD = False

try:
    import cv2
    _HAS_CV2 = True
except Exception:
    _HAS_CV2 = False

try:
    import numpy as np
    _HAS_NUMPY = True
except Exception:
    _HAS_NUMPY = False

_HAS_TF = False
def _lazy_import_tf():
    global _HAS_TF
    if not _HAS_TF:
        try:
            import tensorflow as tf
            from tensorflow.keras.applications import MobileNetV2
            from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
            from tensorflow.keras.preprocessing import image
            _HAS_TF = True
            return tf, MobileNetV2, preprocess_input, image
        except Exception as e:
            raise RuntimeError("TensorFlow is required for CNN features. Try: pip install tensorflow==2.*") from e

@dataclass
class MetadataResult:
    tags: Dict[str, Any]
    flags: Dict[str, bool]

@dataclass
class NoiseResult:
    sharpness_laplacian: Optional[float]
    grayscale_std: Optional[float]
    notes: List[str]

@dataclass
class CNNResult:
    feature_intensity: Optional[float]
    notes: List[str]

class DeepfakeKit:
    def __init__(self, mobilenet_weights: str = 'imagenet'):
        self._tf_bundle = None
        self._mobilenet = None
        self._mobilenet_weights = mobilenet_weights

    def check_metadata(self, path: str) -> MetadataResult:
        """
        Check image metadata (EXIF data) for signs of AI generation or missing camera info.

        Returns:
            MetadataResult with tags (all EXIF data) and flags (suspicious indicators)
        """
        tags = {}
        flags = {
            'no_exif': False,
            'missing_camera': False,
            'has_ai_generator_hint': False,
        }
        if not os.path.exists(path):
            raise FileNotFoundError(path)

        if _HAS_EXIFREAD:
            try:
                with open(path, 'rb') as f:
                    tags = {k: str(v) for k, v in exifread.process_file(f, details=False).items()}
            except Exception:
                tags = {}
        else:
            try:
                img = Image.open(path)
                exif = img.getexif()
                if exif:
                    for k, v in exif.items():
                        tags[str(k)] = str(v)
            except Exception:
                pass

        if not tags:
            flags['no_exif'] = True

        joined = " ".join(tags.values()).lower() if tags else ""
        if ('image make' not in (k.lower() for k in tags.keys())) and ('make' not in joined):
            flags['missing_camera'] = True

        ai_keywords = ['ai', 'generated', 'stable diffusion', 'midjourney', 'dalle', 'gemini']
        if any(re.search(rf'\b{kw}\b', joined) for kw in ai_keywords):
            flags['has_ai_generator_hint'] = True

        return MetadataResult(tags=tags, flags=flags)

    def noise_stats(self, path: str) -> NoiseResult:
        """
        Analyze image noise and sharpness patterns.
        Real cameras have natural sensor noise; AI images often have unusual patterns.

        Returns:
            NoiseResult with sharpness_laplacian (edge sharpness) and grayscale_std (noise level)
        """
        notes: List[str] = []
        if not _HAS_NUMPY:
            return NoiseResult(None, None, notes + ["numpy not installed"])
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        import numpy as np
        gray = Image.open(path).convert('L')
        arr = np.array(gray)

        grayscale_std = float(arr.std())
        sharpness = None
        if _HAS_CV2:
            try:
                sharpness = float(cv2.Laplacian(arr, cv2.CV_64F).var())
            except Exception:
                notes.append("cv2 Laplacian failed")
        else:
            notes.append("opencv not installed; skipping Laplacian sharpness")
        return NoiseResult(sharpness_laplacian=sharpness, grayscale_std=grayscale_std, notes=notes)

    def _ensure_mobilenet(self):
        """Lazy-load MobileNetV2 model (only when needed)"""
        if self._mobilenet is None:
            tf, MobileNetV2, preprocess_input, image = _lazy_import_tf()
            self._tf_bundle = (tf, MobileNetV2, preprocess_input, image)
            self._mobilenet = MobileNetV2(weights=self._mobilenet_weights, include_top=False, pooling='avg')

    def cnn_feature_intensity(self, path: str) -> CNNResult:
        """
        Extract CNN features using MobileNetV2 and compute feature intensity.
        Different patterns between real and AI-generated images.

        Returns:
            CNNResult with feature_intensity (higher values = more complex patterns)
        """
        notes: List[str] = []
        self._ensure_mobilenet()
        tf, MobileNetV2, preprocess_input, image = self._tf_bundle

        if not os.path.exists(path):
            raise FileNotFoundError(path)

        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = preprocess_input(x[None, ...])
        feats = self._mobilenet.predict(x, verbose=0)
        if feats is None:
            return CNNResult(None, notes + ["no features produced"])

        import numpy as np
        intensity = float(np.linalg.norm(feats))
        return CNNResult(intensity, notes)

    def plot_first_layer(self, path: str, channels: int = 6):
        """
        Visualize what the first CNN layer "sees" in the image.
        Shows edge detectors, texture filters, etc.

        Args:
            path: Path to image file
            channels: Number of feature maps to display
        """
        self._ensure_mobilenet()
        tf, MobileNetV2, preprocess_input, image = self._tf_bundle
        import numpy as np
        import matplotlib.pyplot as plt

        base = MobileNetV2(weights=self._mobilenet_weights, include_top=False)
        first_conv = None
        for layer in base.layers:
            if 'conv' in layer.name:
                first_conv = layer
                break
        if first_conv is None:
            print("No conv layer found.")
            return

        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = preprocess_input(x[None, ...])
        act_model = tf.keras.Model(inputs=base.input, outputs=first_conv.output)
        acts = act_model.predict(x, verbose=0)[0]

        n = min(channels, acts.shape[-1])
        fig, axes = plt.subplots(2, 3, figsize=(12, 8))
        axes = axes.flatten()

        for i in range(n):
            axes[i].imshow(acts[..., i], cmap='viridis')
            axes[i].axis('off')
            axes[i].set_title(f'Feature map {i}')

        plt.tight_layout()
        plt.show()

    def ensemble_flag(self, path: str, meta_weight: float = 0.7, cnn_weight: float = 0.3,
                      sharpness_floor: float = 20.0, intensity_floor: float = 40.0) -> Dict[str, Any]:
        """
        Combine multiple detection methods into a single score.

        Args:
            path: Path to image file
            meta_weight: How much to weight metadata signals (0-1)
            cnn_weight: How much to weight CNN signals (0-1)
            sharpness_floor: Minimum sharpness for real images
            intensity_floor: Minimum CNN intensity for real images

        Returns:
            Dict with all analysis results and a 'likely_fake' boolean
        """
        meta = self.check_metadata(path)
        noise = self.noise_stats(path)
        try:
            cnn = self.cnn_feature_intensity(path)
        except Exception as e:
            cnn = CNNResult(None, [str(e)])

        meta_score = 1.0 if (meta.flags['no_exif'] or meta.flags['missing_camera'] or meta.flags['has_ai_generator_hint']) else 0.0
        sharpness_ok = (noise.sharpness_laplacian or 0.0) >= sharpness_floor if (noise.sharpness_laplacian is not None) else True
        intensity_ok = (cnn.feature_intensity or 0.0) >= intensity_floor if (cnn.feature_intensity is not None) else False

        total_score = meta_weight * meta_score + cnn_weight * (1.0 if intensity_ok else 0.0)
        likely_fake = (total_score >= 0.7) or (not sharpness_ok and meta_score > 0)

        return {
            'path': path,
            'metadata': meta.flags,
            'noise': {
                'sharpness_laplacian': noise.sharpness_laplacian,
                'grayscale_std': noise.grayscale_std,
            },
            'cnn': {
                'feature_intensity': cnn.feature_intensity,
                'notes': cnn.notes,
            },
            'total_score': total_score,
            'likely_fake': bool(likely_fake),
            'notes': ['Teaching-only heuristic; not a real forensic tool.']
        }

    def batch_ensemble(self, folder: str) -> List[Dict[str, Any]]:
        """
        Run ensemble detection on all images in a folder.

        Args:
            folder: Path to folder containing images

        Returns:
            List of detection results (one per image)
        """
        out = []
        for name in os.listdir(folder):
            if name.lower().endswith(('.jpg', '.jpeg', '.png')):
                try:
                    out.append(self.ensemble_flag(os.path.join(folder, name)))
                except Exception as e:
                    out.append({'path': os.path.join(folder, name), 'error': str(e)})
        return out
