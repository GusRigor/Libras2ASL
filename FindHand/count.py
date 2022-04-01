import cv2
import time
import handTrackingModule as dtm


captura = cv2.VideoCapture(0)
tac = 0

detector = dtm.detectorMaos()

idPontaDedos = [4, 8, 12, 16, 20]

while True:
    successo, imagem = captura.read()
    imagem = detector.encontrarMaos(imagem)
    listaPntRef = detector.encontrarPosicao(imagem, desenhar=False)

    if len(listaPntRef) != 0:
        Dedos = []

        # Dedão
        if listaPntRef[idPontaDedos[0]][1] > listaPntRef[idPontaDedos[0] - 1][1]:
            Dedos.append(1)
        else:
            Dedos.append(0)

        # 4 Dedos
        for id in range(1, 5):
            if listaPntRef[idPontaDedos[id]][2] < listaPntRef[idPontaDedos[id] - 2][2]:
                Dedos.append(1)
            else:
                Dedos.append(0)

        totalDedos = Dedos.count(1)
        print(totalDedos)

        cv2.rectangle(imagem, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(imagem, str(totalDedos), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    tic = time.time()
    fps = 1 / (tic - tac)
    tac = tic

    cv2.putText(imagem, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", imagem)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
