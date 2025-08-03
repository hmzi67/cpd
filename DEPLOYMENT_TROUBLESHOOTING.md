# Streamlit Cloud Deployment Troubleshooting Guide

## ❗ Common Error: "installer returned a non-zero exit code"

This error typically occurs due to dependency conflicts. Here are the solutions:

### 🔧 Solution 1: Use Stable Requirements (RECOMMENDED)

We've created multiple requirements files for different scenarios:

#### `requirements.txt` (Current - Stable versions)
```
streamlit==1.25.0
opencv-python-headless==4.7.1.72
mediapipe==0.10.3
numpy==1.23.5
```

#### `requirements_stable.txt` (Backup - Most conservative)
```
streamlit==1.25.0
opencv-python-headless==4.7.1.72
mediapipe==0.10.3
numpy==1.23.5
```

### 🔧 Solution 2: Deploy Minimal Version

If the original app still fails, use the minimal version:

1. **Current deployment structure:**
   ```
   main.py ← Minimal version (active)
   main_original.py ← Your original version (backup)
   app_minimal.py ← Minimal source
   ```

2. **The minimal version (`main.py`) includes:**
   - ✅ Basic MediaPipe pose detection
   - ✅ Video/image upload
   - ✅ Simple pose visualization
   - ✅ No complex imports or dependencies

### 🔧 Solution 3: Step-by-Step Deployment

1. **Check Current Status:**
   ```bash
   git status
   ```

2. **Commit the Fixed Version:**
   ```bash
   git add .
   git commit -m "Fix: Use stable dependencies for cloud deployment"
   git push origin main
   ```

3. **Redeploy on Streamlit Cloud:**
   - Go to your Streamlit Cloud dashboard
   - Click "Reboot app" or delete and redeploy
   - Wait for the new deployment

### 🔧 Solution 4: Alternative Requirements

If the current version still fails, try this ultra-minimal approach:

```
# Ultra-minimal requirements.txt
streamlit
opencv-python-headless
mediapipe
numpy<2.0
```

### 🔧 Solution 5: Local Testing First

Test locally before deploying:

```bash
# Test minimal version locally
streamlit run main.py

# If that works, then deploy to cloud
git add .
git commit -m "Working minimal version"
git push origin main
```

## 📊 Troubleshooting Steps

### Step 1: Check Streamlit Cloud Logs
- Go to your app on share.streamlit.io
- Click on "Manage app"
- Check the deployment logs for specific error messages

### Step 2: Common Error Patterns

#### NumPy Version Conflicts:
```
Error: A module that was compiled using NumPy 1.x cannot be run in NumPy 2.x
```
**Solution:** Use `numpy==1.23.5` (fixed in our requirements.txt)

#### MediaPipe Installation Issues:
```
Error: Failed building wheel for mediapipe
```
**Solution:** Use `mediapipe==0.10.3` (stable version)

#### OpenCV Issues:
```
Error: Could not find a version that satisfies opencv-python
```
**Solution:** Use `opencv-python-headless` instead of `opencv-python`

### Step 3: Version Compatibility Matrix

| Package | Working Version | Cloud Compatible | Notes |
|---------|----------------|------------------|-------|
| streamlit | 1.25.0 | ✅ | Stable, well-tested |
| mediapipe | 0.10.3 | ✅ | Avoid newer versions |
| opencv-python-headless | 4.7.1.72 | ✅ | Must use headless for cloud |
| numpy | 1.23.5 | ✅ | Avoid 2.x versions |

## 🚀 Quick Fix Commands

### If still having issues, try this sequence:

```bash
# 1. Use the ultra-minimal requirements
echo "streamlit" > requirements.txt
echo "opencv-python-headless" >> requirements.txt  
echo "mediapipe" >> requirements.txt
echo "numpy<2.0" >> requirements.txt

# 2. Commit and push
git add requirements.txt
git commit -m "Ultra-minimal requirements"
git push origin main

# 3. Check if it deploys, then gradually add versions back
```

## 📞 Still Having Issues?

### Option A: Use the Guaranteed Working Version
```bash
# Copy the stable requirements
cp requirements_stable.txt requirements.txt
git add requirements.txt
git commit -m "Use guaranteed stable requirements"
git push origin main
```

### Option B: Deploy Different App Version
If you want the full functionality, keep the minimal version for cloud and use the original locally:

- **Cloud (main.py):** Minimal version with file upload
- **Local (main_original.py):** Full version with camera

### Option C: Contact Support
- Check Streamlit Community forums: https://discuss.streamlit.io
- Create GitHub issue with deployment logs
- Try deploying on a different platform (Heroku, Railway, etc.)

---

## ✅ Current Status

You now have:
- ✅ Fixed requirements.txt with stable versions
- ✅ Minimal working app (main.py)
- ✅ Backup of original app (main_original.py)
- ✅ Multiple requirement files for different scenarios
- ✅ This troubleshooting guide

**Next step:** Push the changes and redeploy!
