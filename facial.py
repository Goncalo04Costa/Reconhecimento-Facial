# Gonçalo Costa
# Data: 2025-07-09
# goncalocosta522@gmail.com
# Reconhecimento facial com webcam e base de dados

import cv2
from deepface import DeepFace
import pyodbc

# Conectar a base de dados
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=GONCALO;DATABASE=pessoas_reconhecimentofacial;Trusted_Connection=yes;'
)
cursor = conn.cursor()

# Carregamento  das imagens e criação de  embeddings
cursor.execute("SELECT Nome, CaminhoFoto FROM Pessoas")
registos = cursor.fetchall()

base_embeddings = []
for nome, caminho in registos:
    try:
        caminho = caminho.strip()
        img = cv2.imread(caminho)
        if img is None:
            print(f"Imagem não encontrada: {caminho}")
            continue
        emb = DeepFace.represent(img, enforce_detection=False)[0]["embedding"]
        base_embeddings.append((nome, emb))
    except Exception as e:
        print(f"Erro ao processar {caminho}: {e}")

# Inicialização a webcam
cap = cv2.VideoCapture(0)
frame_count = 0
analyze_interval = 7
result = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % analyze_interval == 0:
        try:
            result = DeepFace.analyze(frame, actions=["age", "emotion"], enforce_detection=False)
        except Exception:
            result = None

    if result:
        try:
            age = result[0]['age']
            emotion = result[0]['dominant_emotion']
            region = result[0]['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']

            face_img = frame[y:y+h, x:x+w]
            if face_img.size == 0:
                continue

            emb_captured = DeepFace.represent(face_img, enforce_detection=False)[0]["embedding"]

            nome_encontrado = "Desconhecido"
            menor_distancia = float("inf")

            for nome_bd, emb_bd in base_embeddings:
                dist = sum((e1 - e2)**2 for e1, e2 in zip(emb_captured, emb_bd))**0.5
                if dist < 1.3 and dist < menor_distancia:
                    menor_distancia = dist
                    nome_encontrado = nome_bd

            # Cores baseadas na emoção
            if emotion == "happy":
                color = (0, 255, 0)
            elif emotion in ["sad", "angry", "fear"]:
                color = (255, 0, 0)
            elif emotion == "neutral":
                color = (0, 0, 255)
            else:
                color = (255, 255, 255)

            # Desenho do retângulo e texto
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"Nome: {nome_encontrado}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, f"Idade: {int(age)}", (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(frame, f"Sentimento: {emotion}", (x, y - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        except Exception as e:
            print("Erro ao processar rosto:", e)

    cv2.imshow("Reconhecimento Facial com BD", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cap.release()
cv2.destroyAllWindows()
