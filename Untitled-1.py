import cv2

# Inicializa a captura de vídeo (0 para webcam padrão)
cap = cv2.VideoCapture(0)

# Cria o objeto de subtração de fundo
backSub = cv2.createBackgroundSubtractorMOG2()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao capturar o vídeo.")
        break

    # Aplica a subtração de fundo para obter a máscara de movimento
    fgMask = backSub.apply(frame)

    # Opcional: Aplicar operações de dilatação para preencher buracos
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_DILATE, kernel)

    # Encontrar contornos na máscara
    contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Filtrar contornos pequenos
        if cv2.contourArea(contour) < 500:
            continue

        # Obter o retângulo delimitador do contorno
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Exibir o quadro original com retângulos
    cv2.imshow('Frame', frame)
    # Exibir a máscara de movimento
    

    # Sair do loop quando a tecla 'q' for pressionada
    if cv2.waitKey(30) & 0xFF == ord('q'):
        print("Saindo do programa...")
        break

# Liberar os recursos
cap.release()
cv2.destroyAllWindows()
