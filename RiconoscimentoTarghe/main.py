import cv2
import pytesseract
from datetime import time

class Plate:
    def __init__(self, testo, orario_inizio, orario_fine):
        self.testo = testo
        self.orario_inizio = orario_inizio
        self.orario_fine = orario_fine

    def set_exit_time(self, orario_fine):
        self.orario_fine = orario_fine
        
    def __repr__(self):
        return f"Targa(testo={self.testo}, orario_inizio={self.orario_inizio}, orario_fine={self.orario_fine})"


# Carica il modello Haar Cascade per targhe
plate_cascade = cv2.CascadeClassifier('Model/haarcascade_russian_plate_number.xml')

def detect_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    plates = plate_cascade.detectMultiScale(gray)
    for (x, y, w, h) in plates:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        plate = frame[y:y+h, x:x+w]
        return plate
    return None

def extract_text(plate):
    gray_plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    # Usa pytesseract per il riconoscimento
    text = pytesseract.image_to_string(gray_plate, config='--psm 8')  # Configura per target piccoli
    return text.strip()

# Elenco per memorizzare tutte le targhe registrate
plates_log = []

# Dizionario per le targhe attualmente nel parcheggio
current_plates = {}

def register_entry(plate_text):
    # Controlla se la targa non è già nel parcheggio
    if plate_text not in current_plates:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Ottieni l'orario attuale
        new_plate = Plate(plate_text, current_time)  # Crea una nuova istanza di Plate
        plates_log.append(new_plate)  # Aggiungila all'elenco generale
        current_plates[plate_text] = new_plate  # Aggiungila al dizionario delle targhe correnti
        print(f"Ingresso registrato: {new_plate}")
    else:
        print(f"Targa {plate_text} già registrata come presente.")

def register_exit(plate_text):
    # Controlla se la targa è attualmente nel parcheggio
    if plate_text in current_plates:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')  # Ottieni l'orario attuale
        plate = current_plates.pop(plate_text)  # Rimuovi dal dizionario
        plate.set_exit_time(current_time)  # Imposta l'orario di uscita
        print(f"Uscita registrata: {plate}")
    else:
        print(f"Targa {plate_text} non trovata nel parcheggio.")

# Carica l'immagine da file
image_path = 'Plates/targa_automobile.jpeg'  # Percorso dell'immagine
image = cv2.imread(image_path)

# Assicurati che l'immagine sia stata caricata correttamente
if image is None:
    print(f"Errore: Impossibile caricare l'immagine da {image_path}")
else:
    plate = detect_plate(image)  # Rileva la targa
    if plate is not None:
        text = extract_text(plate)  # Estrai il testo
        print("Targa rilevata:", text)
        register_entry(text)  # Registra l'ingresso della targa
        cv2.imshow("Targa", plate)  # Mostra la targa ritagliata
        cv2.waitKey(0)  # Attendi che venga premuto un tasto
    else:
        print("Nessuna targa rilevata nell'immagine.")

# Mostra l'immagine completa con il rettangolo attorno alla targa
cv2.imshow("Immagine con targa", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Mostra il log completo delle targhe
print("\nLog delle targhe registrate:")
for plate in plates_log:
    print(plate)