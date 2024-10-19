import os
import librosa
import numpy as np
from pydub import AudioSegment
from scipy.io.wavfile import write

# Ses dosyalarının yolu
base_path = r"C:\VSCode\Python\Voice\Data\Recorded"
text_wav = os.path.join(base_path, "Batuhan_Text.wav")
voice_wav = os.path.join(base_path, "Batuhan_Voices.wav")

# İşlem yapacak fonksiyon
def process_audio(input_wav, output_no_silence_wav, chunks_output_dir):
    # 1. Ses dosyasını yükle
    audio, sr = librosa.load(input_wav, sr=None)

    # 2. Sessizlikleri kaldırmak için sesin enerjisine bakalım
    # Enerjiyi hesapla
    energy = librosa.feature.rms(y=audio)[0]  # RMS enerjisi
    threshold = 0.03  # Enerji eşiği (ayarlanabilir)

    # Sessiz kısımlar
    non_silent_indices = np.where(energy > threshold)[0]

    # Başlangıç ve bitiş indekslerini bul
    if len(non_silent_indices) > 0:  # Eğer sessiz kısımlar yoksa
        non_silent_audio = audio[non_silent_indices[0] * 512: non_silent_indices[-1] * 512]

        # Sessiz kısımlar kaldırıldıktan sonra yeni ses dosyası
        write(output_no_silence_wav, sr, (non_silent_audio * 32767).astype(np.int16))

        # 3. Ses dosyasını 1.5 saniyelik parçalara ayırma
        # Pydub kullanarak ses dosyasını yükle
        sound = AudioSegment.from_wav(output_no_silence_wav)

        # 1.5 saniye = 1500 milisaniye
        chunk_length_ms = 1500

        # Parçaları oluştur
        chunks = [sound[i:i + chunk_length_ms] for i in range(0, len(sound), chunk_length_ms)]

        # 4. Parçaları kaydetme
        for i, chunk in enumerate(chunks):
            chunk.export(os.path.join(chunks_output_dir, f"chunk_{os.path.basename(input_wav)}_{i}.wav"), format="wav")

        print(f"{os.path.basename(input_wav)} için duraksamalar kaldırıldı ve dosya 1.5 saniyelik parçalara bölündü.")
    else:
        print(f"{os.path.basename(input_wav)} için sessiz kısımlar bulunamadı.")

# Çıkış dizinini oluştur
chunks_output_dir = os.path.join(base_path, "Chunks")
os.makedirs(chunks_output_dir, exist_ok=True)

# İşlemi Batuhan_Text.wav ve Batuhan_Voices.wav için uygula
process_audio(voice_wav, os.path.join(base_path, "Batuhan_Voices_no_silence.wav"), chunks_output_dir)
process_audio(text_wav, os.path.join(base_path, "Batuhan_Text_no_silence.wav"), chunks_output_dir)
