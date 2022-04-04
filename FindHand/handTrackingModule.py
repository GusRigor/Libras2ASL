import cv2
import mediapipe as mp 
import time


class detectorMaos():
    def __init__(self, modo=False, maxMaos=2, confDetec=1, confRastreio=0.5):
        self.modo = modo
        self.maxMaos = maxMaos
        self.confDetec = confDetec
        self.confRastreio = confRastreio

        self.mpMaos = mp.solutions.hands
        self.maos   = self.mpMaos.Hands(self.modo, self.maxMaos, self.confDetec, self.confRastreio)
        self.mpDesenho = mp.solutions.drawing_utils

    def encontrarMaos(self, imagem, desenhar=True):
        imagemRGB = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        self.resultados = self.maos.process(imagemRGB)

        if self.resultados.multi_hand_landmarks:
            for maosPntRef in self.resultados.multi_hand_landmarks:
                if desenhar:
                    self.mpDesenho.draw_landmarks(imagem, maosPntRef, self.mpMaos.HAND_CONNECTIONS)
        return imagem

    def encontrarPosicao(self, imagem, numMao=0, desenhar=True):
        imagem = self.encontrarMaos(imagem, desenhar)
        listaPntRef = []
        if self.resultados.multi_hand_landmarks:
            minhaMao = self.resultados.multi_hand_landmarks[numMao]
            for id, pntRef in enumerate(minhaMao.landmark):
                altura, largura, _ = imagem.shape
                px, py = int(pntRef.x * largura), int(pntRef.y * altura)
                listaPntRef.append([id, px, py])
                if desenhar:
                    cv2.circle(imagem, (px,py), 15, (0,255,0), cv2.FILLED)
        return listaPntRef

def main():
    camera = cv2.VideoCapture(0)
    detector = detectorMaos()
    tic = 0
    tac = 0

    while True:
        sucesso, imagem = camera.read()
        imagem = detector.encontrarMaos(imagem)
        listaPntRef = detector.encontrarPosicao(imagem)
        if len(listaPntRef) != 0:
            print(listaPntRef[4])

        tac = time.time()
        fps = 1/(tac-tic)
        tic = tac

        cv2.putText(imagem, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

        cv2.imshow("Câmera", imagem)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()
