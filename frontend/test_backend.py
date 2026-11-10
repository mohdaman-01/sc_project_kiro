"""
Test script to verify the local Gradio backend and discover API structure.
"""

import json
import sys

try:
    from gradio_client import Client
except ImportError:
    print("❌ ERROR: gradio_client not installed")
    print("\nInstall it with:")
    print("  pip install gradio_client")
    sys.exit(1)


def test_backend():
    """Test the local Gradio backend and discover API structure"""
    
    print("=" * 70)
    print("TESTING LOCAL GRADIO BACKEND")
    print("=" * 70)
    
    backend_url = "http://127.0.0.1:7860"
    print(f"\nConnecting to: {backend_url}")
    
    try:
        client = Client(backend_url)
        print("✅ Connected successfully!")
    except Exception as e:
        print(f"❌ ERROR: Could not connect to backend")
        print(f"\nError details: {e}")
        print("\n" + "=" * 70)
        print("SOLUTION:")
        print("=" * 70)
        print("1. Start the backend first:")
        print("   cd c:\\Users\\tabas\\Downloads\\SC-Project-kiro")
        print("   python app.py")
        print("\n2. Wait for: 'Running on local URL: http://127.0.0.1:7860'")
        print("\n3. Then run this test script again")
        print("=" * 70)
        sys.exit(1)
    
    print("\n" + "-" * 70)
    print("DISCOVERING API ENDPOINTS")
    print("-" * 70)
    
    try:
        api_info = client.view_api()
        print("\n📋 API Information:")
        print(api_info)
    except Exception as e:
        print(f"⚠️  Could not get API info: {e}")
    
    print("\n" + "-" * 70)
    print("TESTING WITH EXAMPLE DATA")
    print("-" * 70)
    
    test_json = {
        'days': ['Monday', 'Tuesday', 'Wednesday'],
        'periods_per_day': 4,
        'rooms': [
            {'id': 'R1', 'capacity': 30},
            {'id': 'R2', 'capacity': 25}
        ],
        'teachers': [
            {'id': 'T1', 'name': 'Mr. Smith'},
            {'id': 'T2', 'name': 'Ms. Johnson'}
        ],
        'classes': [
            {'id': 'C1', 'subject': 'Math', 'teacher_id': 'T1', 'hours_per_week': 3},
            {'id': 'C2', 'subject': 'English', 'teacher_id': 'T2', 'hours_per_week': 3},
            {'id': 'C3', 'subject': 'Science', 'teacher_id': 'T1', 'hours_per_week': 2}
        ]
    }
    
    print("\n📝 Input: 3 classes, 2 teachers, 2 rooms, 3 days × 4 periods")
    print(f"⚙️  GA Parameters: pop_size=100, generations=100, seed=42")
    
    print("\n🔄 Calling backend API...")
    
    try:
        result = client.predict(
            json.dumps(test_json),
            100,
            100,
            42,
            api_name="/generate_timetable_json"
        )
        
        print("✅ API call successful!")
        
        print("\n" + "=" * 70)
        print("RESPONSE STRUCTURE")
        print("=" * 70)
        
        if isinstance(result, (list, tuple)) and len(result) >= 4:
            download_json = result[3]
            
            if download_json:
                timetable_data = json.loads(download_json)
                
                print(f"\n✅ Final Fitness: {timetable_data.get('final_fitness')}")
                print(f"✅ Generations Run: {timetable_data.get('generations_run')}")
                print(f"✅ Timetable Days: {len(timetable_data.get('timetable', []))}")
                
                if timetable_data.get('final_fitness') == 0:
                    print("\n🎉 PERFECT SOLUTION FOUND!")
                else:
                    print(f"\n⚠️  Solution has {-timetable_data.get('final_fitness')} penalty points")
        
        print("\n" + "=" * 70)
        print("TEST COMPLETE ✅")
        print("=" * 70)
        print("\nThe frontend can now connect to this backend!")
        
    except Exception as e:
        print(f"❌ ERROR calling API: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_backend()
