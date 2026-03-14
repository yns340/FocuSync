import firebase_admin
from firebase_admin import credentials, firestore

class DatabaseManager:
    def __init__(self, key_path="serviceAccountKey.json"):
        # Firebase uygulamasının birden fazla kez başlatılmasını engelle
        if not firebase_admin._apps:
            cred = credentials.Certificate(key_path)
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()

    def register_user(self, email, password):
        """Yeni bir kullanıcıyı manuel olarak 'Users' koleksiyonuna ekler."""
        try:
            # Otomatik ID ile yeni bir döküman referansı oluştur
            doc_ref = self.db.collection("Users").document()
            doc_ref.set({
                "email": email,
                "password": password,
                "role": "User"
            })
            return True, "Kullanıcı başarıyla kaydedildi."
        except Exception as e:
            return False, f"Kayıt hatası: {str(e)}"

    def login_user(self, email, password):
        """Veritabanında email ve şifre eşleşmesini kontrol eder."""
        try:
            users_ref = self.db.collection("Users")
            # Email ve şifreye göre filtreleme yap
            query = users_ref.where("email", "==", email).where("password", "==", password).stream()
            
            for user in query:
                # Eşleşme bulunduysa kullanıcının döküman ID'sini döndür
                return True, user.id
            
            return False, "E-posta veya şifre hatalı."
        except Exception as e:
            return False, f"Sorgu hatası: {str(e)}"