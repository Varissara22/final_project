import json

def save_preferences(selected_crypto, window_geometry): #save user pref in file
    try:
        prefs = {
            'selected_crypto': selected_crypto,
            'window_geometry': window_geometry
        }
        with open('dashboard_preferences.json', 'w') as f:
            json.dump(prefs, f)
        print("Preferences saved")
    except Exception as e:
        print(f"Could not save preferences: {e}")


def load_preferences():
    try:
        with open('dashboard_preferences.json', 'r') as f:
            prefs = json.load(f)
            print(f"Loaded preferences: {prefs['selected_crypto']}")
            return prefs
    except FileNotFoundError:
        print("No saved preferences found")
        return None
    except Exception as e:
        print(f"Could not load preferences: {e}")
        return None