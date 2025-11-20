# Sample Images Directory

This folder should contain test images for the deepfake detection workshop.

## Required Images

You need at least **10 images total**:
- **5 real photos** (from actual cameras)
- **5 AI-generated images**

## Where to Get Images

### Real Photos (5 images)

**Option 1: Take your own**
- Use your phone camera or DSLR
- **Important:** Don't edit them (preserve EXIF metadata)
- Variety: people, landscapes, objects, animals, etc.
- Save as JPG format (PNG often strips EXIF)

**Option 2: Download from photography sites**
- [Unsplash](https://unsplash.com/) - Free high-quality photos
- [Pexels](https://pexels.com/) - Free stock photos
- Make sure to download originals with metadata intact

**Naming suggestion:**
- `real_photo_1.jpg`
- `real_photo_2.jpg`
- etc.

### AI-Generated Images (5 images)

**Free AI Image Generators:**

1. **Gemini** (Google)
   - Visit: [gemini.google.com](https://gemini.google.com)
   - Prompt: "Generate a realistic photograph of [subject]"
   - Download the image

2. **DALL-E 3** (via Bing)
   - Visit: [bing.com/create](https://www.bing.com/create)
   - Free with Microsoft account
   - High quality, realistic results

3. **Stable Diffusion**
   - Visit: [stablediffusionweb.com](https://stablediffusionweb.com)
   - Free, no signup required
   - Use realistic model settings

**Good Prompts to Try:**
- "A photorealistic portrait of a person in a coffee shop"
- "A high-quality photograph of a sunset over mountains"
- "A realistic photo of a golden retriever playing in a park"
- "Professional photography of a modern city street at night"
- "Ultra-realistic image of food on a restaurant table"

**Naming suggestion:**
- `ai_generated_1.jpg`
- `ai_generated_2.jpg`
- etc.

## Sample Image for Testing

At minimum, you need one image named `sample.jpg` for the quick start and demo scripts to work.

## File Structure

Your `images/` folder should look like this:

```
images/
├── README.md (this file)
├── sample.jpg (for testing)
├── real_photo_1.jpg
├── real_photo_2.jpg
├── real_photo_3.jpg
├── real_photo_4.jpg
├── real_photo_5.jpg
├── ai_generated_1.jpg
├── ai_generated_2.jpg
├── ai_generated_3.jpg
├── ai_generated_4.jpg
└── ai_generated_5.jpg
```

## Tips for Good Test Images

**For Real Photos:**
- Keep original EXIF data (don't edit in Photoshop, etc.)
- Use different cameras if possible (phone, DSLR, etc.)
- Variety of subjects helps demonstrate the detector

**For AI Images:**
- Try to make them look realistic (challenging for students)
- Mix different AI tools (each has different "fingerprints")
- Include 1-2 "obvious" AI images for early success

**Advanced (Optional):**
- A real photo that's been edited (EXIF stripped) - will confuse the detector!
- An AI image with fake EXIF added - see if detector catches it
- A very compressed real photo - might look suspicious

## Copyright & Ethics

**Important:**
- Only use images you have rights to
- For educational purposes, most uses are covered by fair use
- Don't distribute students' personal photos without permission
- Be mindful of privacy and consent

## Need Help?

If you can't gather images, you can:
1. Ask students to bring their own (1 real photo from their phone)
2. Use the same set of images for the whole class
3. Focus on the concepts with fewer images

**Minimum viable setup:**
- Just `sample.jpg` (can be any image)
- Students can still learn the concepts!

---

**Once you've added images to this folder, run `quick_start.py` to test your setup!**
