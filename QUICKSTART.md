# 🚀 Quick Start Guide

## Run Locally in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the App
```bash
python app.py
```

### 3. Open Browser
The app will automatically open, or navigate to: `http://127.0.0.1:7860`

## Try It Out

### Option A: Use the Example JSON
1. Open `example_timetable.json` in a text editor
2. Copy the entire content
3. In the app, go to **"JSON Input"** tab
4. Paste the JSON
5. Click **"Generate Timetable"**

### Option B: Use the Simple Form
1. Go to **"Simple Form"** tab
2. Fill in the fields (or use defaults):
   - Days: `Monday,Tuesday,Wednesday,Thursday,Friday`
   - Periods per Day: `6`
   - Subjects: `Math,English,Science,History,PE`
   - Teachers: `Mr. Smith,Ms. Johnson,Dr. Brown,Ms. Davis,Mr. Wilson`
   - Rooms: `R1:30,R2:25,R3:20`
   - Hours per Week: `5,4,3,3,2`
3. Click **"Generate Timetable"**

## Understanding the Results

### ✅ Perfect Solution (Fitness = 0)
Green banner: "Perfect timetable generated with no conflicts!"

### ⚠️ Suboptimal Solution (Fitness < 0)
Orange banner showing penalty points. Try:
- Increasing generations (300 → 500)
- Increasing population size (100 → 150)
- Simplifying the schedule

### 📊 Fitness Chart
Watch how the algorithm improves over generations. A line reaching 0 means perfect!

## Common Issues

### "Impossible schedule" Error
**Problem**: Too many hours for available slots

**Example**: 6 classes × 5 hours = 30 hours, but only 5 days × 4 periods = 20 slots

**Solution**: 
- Reduce hours per week for some classes
- Add more days or periods
- Remove some classes

### Slow Performance
**Problem**: Large population or many generations

**Solution**: 
- Start with Pop Size=50, Generations=100 for testing
- Increase for production: Pop Size=100-200, Generations=300-500

## Next Steps

1. **Customize**: Edit the JSON or form to match your school's needs
2. **Export**: Download the generated timetable as JSON
3. **Deploy**: Upload to Hugging Face Spaces (see README.md)

## Need Help?

- Check `README.md` for detailed documentation
- Run `python ga_scheduler.py` to test the core algorithm
- Run `python test_app.py` to verify everything works

Happy scheduling! 🎓
