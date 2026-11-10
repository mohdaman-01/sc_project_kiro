# 🚀 Deployment Checklist for Hugging Face Spaces

## Pre-Deployment Verification

### ✅ Files Present
- [x] `app.py` - Main application
- [x] `ga_scheduler.py` - Core GA logic
- [x] `requirements.txt` - Dependencies
- [x] `README.md` - Documentation

### ✅ Optional Files (Recommended)
- [x] `app_config.yaml` - Space metadata
- [x] `example_timetable.json` - Example input
- [x] `QUICKSTART.md` - User guide
- [x] `.gitignore` - Git configuration

### ✅ Local Testing Complete
- [x] Core GA tests pass (`python ga_scheduler.py`)
- [x] App tests pass (`python test_app.py`)
- [x] Full example works (`python test_full_example.py`)

---

## Deployment Steps

### Option A: Web Interface (Easiest)

1. **Create Hugging Face Account**
   - Go to https://huggingface.co
   - Sign up (free)

2. **Create New Space**
   - Click "Spaces" → "Create new Space"
   - Name: `ga-timetable-scheduler` (or your choice)
   - License: MIT
   - SDK: **Gradio**
   - SDK version: 4.0.0+
   - Visibility: Public or Private

3. **Upload Files**
   - Drag and drop or upload:
     - `app.py`
     - `ga_scheduler.py`
     - `requirements.txt`
     - `README.md`
   - Optional: `app_config.yaml`, `example_timetable.json`

4. **Wait for Build**
   - Space will build automatically (1-2 minutes)
   - Watch the "Building" indicator
   - Once complete, app will be live!

5. **Test Your Space**
   - Click on your Space
   - Try the form or JSON input
   - Generate a timetable
   - Verify everything works

### Option B: Git CLI (Advanced)

```bash
# 1. Create Space on HuggingFace.co and get repo URL

# 2. Clone the Space repo
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# 3. Copy required files
cp ../SC-Project-kiro/app.py .
cp ../SC-Project-kiro/ga_scheduler.py .
cp ../SC-Project-kiro/requirements.txt .
cp ../SC-Project-kiro/README.md .

# 4. Optional: Copy additional files
cp ../SC-Project-kiro/app_config.yaml .
cp ../SC-Project-kiro/example_timetable.json .

# 5. Commit and push
git add .
git commit -m "Initial deployment: GA Timetable Scheduler"
git push

# 6. Visit your Space URL to see it build and launch
```

---

## Post-Deployment Verification

### ✅ Functional Tests

1. **Test JSON Input**
   - [ ] Paste example JSON
   - [ ] Click "Generate Timetable"
   - [ ] Verify timetable displays
   - [ ] Check fitness chart appears
   - [ ] Confirm success message (green banner)

2. **Test Form Input**
   - [ ] Fill in simple form
   - [ ] Use default values
   - [ ] Click "Generate Timetable"
   - [ ] Verify output

3. **Test Error Handling**
   - [ ] Try invalid JSON → should show error
   - [ ] Try impossible schedule → should detect

4. **Test Parameters**
   - [ ] Adjust population size slider
   - [ ] Adjust generations slider
   - [ ] Enter a seed number
   - [ ] Verify reproducibility

### ✅ Performance Check
- [ ] Small schedule (< 20 hours): < 5 seconds
- [ ] Medium schedule (20-50 hours): < 10 seconds
- [ ] No crashes or errors

### ✅ UI Check
- [ ] Tables display correctly
- [ ] Colors are visible
- [ ] Chart renders properly
- [ ] Download works (if implemented)
- [ ] Mobile responsive (optional)

---

## Troubleshooting

### Build Fails

**Problem**: Space fails to build

**Solutions**:
1. Check `requirements.txt` syntax
2. Verify file names are correct
3. Check logs in Space settings
4. Try re-uploading files

### App Doesn't Launch

**Problem**: Build succeeds but app won't start

**Solutions**:
1. Check `app.py` has `if __name__ == "__main__": app.launch()`
2. Verify imports work
3. Check Space logs for Python errors
4. Test locally first with `python app.py`

### Slow Performance

**Problem**: App is very slow

**Solutions**:
1. Reduce default generations (300 → 100)
2. Reduce population size (100 → 50)
3. Consider upgrading to paid HF Space for more resources

### Import Errors

**Problem**: "ModuleNotFoundError"

**Solutions**:
1. Check all imports in `requirements.txt`
2. Verify exact package names
3. Pin versions if needed (e.g., `gradio==4.0.0`)

---

## Configuration Options

### `app_config.yaml` Settings

```yaml
title: GA Timetable Scheduler
emoji: 🎓
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: mit
```

**Customization**:
- `title`: Your Space name
- `emoji`: Icon for Space
- `colorFrom/colorTo`: Gradient colors
- `pinned`: True to pin to your profile

---

## Sharing Your Space

### Get Space URL
```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

### Embed in Website
```html
<iframe
  src="https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space"
  frameborder="0"
  width="850"
  height="450">
</iframe>
```

### Share on Social Media
Hugging Face generates preview cards automatically!

---

## Monitoring & Maintenance

### Check Space Health
- Visit Space regularly
- Test with new inputs
- Monitor user feedback (if public)

### Update Code
```bash
# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Make changes
# Edit files...

# Commit and push
git add .
git commit -m "Update: description of changes"
git push
```

### View Logs
- Go to Space settings
- Click "View logs"
- Check for errors

---

## Space Limits (Free Tier)

- **CPU**: Basic (sufficient for GA)
- **Memory**: 16 GB RAM
- **Storage**: 50 GB
- **Timeout**: 60 seconds per request (should be enough)

**If you need more**: Upgrade to paid Spaces

---

## Success! 🎉

Once deployed, your Space will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

Share it with:
- Schools and universities
- Teachers and administrators
- Other developers
- Education technology communities

---

## Support

- HuggingFace Docs: https://huggingface.co/docs/hub/spaces
- Gradio Docs: https://gradio.app/docs
- This project's README.md
- QUICKSTART.md for usage help

**Deployment checklist complete! Ready to go live! 🚀**
