import cv2
import time
import handTrackingModule as dtm
from enum import Enum

class posicaoMao(Enum):
    Inicial = 1
    Abaixada = 2
    Levantada = 3
    Abaixada_2 = 4
    Final = 5


class eat_libras():
    def __init__(self, detectorMaos = dtm.detectorMaos(), posicao = posicaoMao.Inicial):
        self.detectorMaos = detectorMaos
        self.posicao = posicao
        self.idPontaDedos = [8, 12, 16, 20]

    def maoLevantada(self, imagem):
        listaPontos = self.detectorMaos.encontrarPosicao(imagem, desenhar=False)
        dedo_levantado = []
        if len(listaPontos) != 0:
            for i in self.idPontaDedos:
                if listaPontos[i][2] < listaPontos[i-1][2]:
                    dedo_levantado.append(True)
        if len(dedo_levantado) != 0:
            self.proxima_posicao()
            return True
        return False

    def maoAbaixada(self, imagem):
        listaPontos = self.detectorMaos.encontrarPosicao(imagem, desenhar=False)
        dedo_Abaixado = []
        if len(listaPontos) != 0:
            for i in self.idPontaDedos:
                if listaPontos[i][2] > listaPontos[i-1][2]:
                    dedo_Abaixado.append(True)
        if len(dedo_Abaixado) != 0:
            self.proxima_posicao()
            return True
        return False

    def proxima_posicao(self):
        if self.posicao == posicaoMao.Inicial:
            self.posicao = posicaoMao.Abaixada
        elif self.posicao == posicaoMao.Abaixada:
            self.posicao = posicaoMao.Levantada
        elif self.posicao == posicaoMao.Levantada:
            self.posicao = posicaoMao.Abaixada_2
        elif self.posicao == posicaoMao.Abaixada_2:
            self.posicao = posicaoMao.Final


def mostrar_eat():
    cap = cv2.VideoCapture('eat.mp4')
    while True:
        sucesso, frame = cap.read()
        cv2.imshow('eat',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
         break
    cap.release()
    cv2.destroyAllWindows()

def main():
    camera = cv2.VideoCapture(0)
    detector = eat_libras()
    tic = 0
    tac = 0

    while True:
        sucesso, imagem = camera.read()
        #imagem = detector.encontrarMaos(imagem)
        if detector.posicao == posicaoMao.Inicial or detector.posicao == posicaoMao.Levantada:
            detector.maoLevantada(imagem)
            cv2.putText(imagem, "Levante os dedos", (10,120), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
        if detector.posicao == posicaoMao.Abaixada or detector.posicao == posicaoMao.Abaixada_2:
            detector.maoAbaixada(imagem)
            cv2.putText(imagem, "Abaixe os dedos", (10,120), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
        if detector.posicao == posicaoMao.Final:
            cv2.putText(imagem, "Voce fez comer, Mostrar em ASL", (10,120), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
        

        tac = time.time()
        fps = 1/(tac-tic)
        tic = tac

        cv2.putText(imagem, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

        cv2.imshow("Câmera", imagem)
        if cv2.waitKey(1) & 0xFF == ord('q') or detector.posicao == posicaoMao.Final:
            camera.release()
            cv2.destroyAllWindows()
            break
    mostrar_eat()

if __name__ == "__main__":
    main()



    


