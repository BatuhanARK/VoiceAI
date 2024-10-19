import os

# Dosyaların bulunduğu dizin
base_path = r"C:\VSCode\Python\Voice\Data\Recorded"

# Yeni isimler için sayaç
counter = 0

# Dizin içindeki dosyaları al
for filename in os.listdir(base_path):
    # Dosya adının 'chunk_Batuhan_' ile başladığını kontrol et
    if filename.startswith("chunk_Batuhan_"):
        # Yeni dosya adını oluştur
        new_filename = f"Batuhan_{counter}.wav"
        
        # Eski ve yeni dosya yollarını oluştur
        old_file_path = os.path.join(base_path, filename)
        new_file_path = os.path.join(base_path, new_filename)

        # Dosyayı yeniden adlandır
        os.rename(old_file_path, new_file_path)
        
        print(f"{old_file_path} -> {new_file_path}")  # Değişikliği yazdır

        # Sayaç artır
        counter += 1

print("Tüm dosyaların isimleri başarıyla değiştirildi.")
