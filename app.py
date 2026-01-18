# app.py - Basit backend kodu
def get_user(user_id):
    """Kullanıcı bilgisini getir"""
    if user_id is None:
        return None
    return {"id": user_id, "name": "Test User"}

def process_data(data):
    """Veri işle"""
    if not data:
        return []
    return [item.upper() for item in data]

if __name__ == "__main__":
    print("Backend running...")
    def test_function():
    """Test için basit fonksiyon"""
    return "G4 testing"