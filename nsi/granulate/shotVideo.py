class ShotVideo(object):


    def createHistogramBoxes( self, vetImg, frame, totalHorizontalDivisions = 2, totalVerticalDivisions = 3  ):
        '''Calcula os pontos de corte da imagem (box) e o histograma de cada um deles'''
        cropHistogram = []
        sizeBox = self.calculateSizeBox ( vetImg[frame] )
        for horizontalDivision in range( totalHorizontalDivisions ):
            for verticalDivision in range( totalVerticalDivisions ):
                x1Point = horizontalDivision * sizeBox[0]
                y1Point = verticalDivision * sizeBox[1]
                x2Point = x1Point + sizeBox[0] - 1
                y2Point = y1Point + sizeBox[1] - 1
                box = (x1Point, y1Point, x2Point, y2Point)
                cropHistogram.append( vetImg[ frame ].crop(box).convert("L").histogram() )
        return cropHistogram

    def calculateBoxesHistogramDiference( self, histogram1, histogram2 ):
        '''Calcula a diferenca (valor absoluto inteiro) dos histogramas de duas imagens'''
        diferenceHistogram = []
        for box in range(len(histogram1)):
            diferenceHistogram.append(0)
            for bin in range(0,256):#para toda tonalidade de cor do histograma
                diferenceHistogram[box] = diferenceHistogram[box] + (abs(histogram1[box][ bin ] - histogram2[box][ bin ]))
        return diferenceHistogram

    def potentialShot( self, diferenceList, sensitivity, boxesToDetectShot = 4 ):
        '''Verifica se a diferenca das partes de dois histogramas e maior do que a sensibilidade
        e, dependendo de quantas partes forem forem diferentes, retorna verdadeiro ou falso para
        transicao em potencial'''
        sensitivityBiggerBoxes = 0
        #numero minimo de partes da imagem que tem que ser diferentes para significar possivel transicao
        for box in range( len(diferenceList) ):
            if diferenceList[box] > sensitivity:
                 sensitivityBiggerBoxes = sensitivityBiggerBoxes + 1
        return sensitivityBiggerBoxes > boxesToDetectShot

    def shotDetect( self, vetImg, vetShot, sensitivity ):
        lastSaved = 0  #controla para que nao sejam gravados dois frames subsequentes
        frameAHistogram = self.createHistogramBoxes( vetImg, 0 ) #grava o histograma do frame 0 do parse corrente
        frameBHistogram = self.createHistogramBoxes( vetImg, 1) #grava o histograma do frame 1 do parse corrente
        for frame in range(2,len(vetImg)): #para todo frame armazenado no vetor
            frameCHistogram = self.createHistogramBoxes( vetImg, frame )#grava o histograma do frame atual
            if self.__verifyTransition( frameAHistogram, frameBHistogram, frameCHistogram, sensitivity):
                if ((frame-1) - lastSaved ) > 1: #se o ultimo frame gravado nao estiver ao lado
                    if self.__noiseVerify(vetImg, sensitivity, frameBHistogram, frame):
                        vetShot.append(vetImg[(frame-1)])
                        #vetImg[(frame-1)].save('./tempVet/shot_%d.jpg' % (apague))
                        lastSaved = frame-1
            frameAHistogram = frameBHistogram
            frameBHistogram = frameCHistogram
        return vetShot

    def __verifyTransition(self, frameAHistogram, frameBHistogram, frameCHistogram, sensitivity):
        backwardDiference = self.calculateBoxesHistogramDiference( frameAHistogram, frameBHistogram )#armazena a diferenca do histograma do frame corrente com o anterior
        forwardDiference = self.calculateBoxesHistogramDiference( frameBHistogram, frameCHistogram )#armazena a diferenca do histograma do frame corrente com o posterior
        #se as diferencas para o frame posterior e para o frame anterior nao forem maiores que a sensibilidade entao nao e fade
        if not(( self.potentialShot( forwardDiference, sensitivity ) ) and ( self.potentialShot( backwardDiference, sensitivity ))):
            #se a diferenca para o frame posterior ou para o anterior for maior que a sensibilidade entao possivel deteccao de frame
            if ( self.potentialShot( forwardDiference, sensitivity ) ) or ( self.potentialShot( backwardDiference, sensitivity ) ):
                return True
        return False

    def calculateSensitivity ( self, sensitivityPercentage, frame ):
        sizeBox = self.calculateSizeBox ( frame )
        totalBoxPixels = sizeBox[0] * sizeBox[1]
        sensitivity = int( totalBoxPixels * 2 * sensitivityPercentage )
        return sensitivity

    def calculateSizeBox ( self, frame, totalHorizontalDivisions = 2, totalVerticalDivisions = 3 ):
        sizeBox = [0,0]
        sizeBox[0] = frame.size[0] / totalHorizontalDivisions
        sizeBox[1] = frame.size[1] / totalVerticalDivisions
        return sizeBox

    def __noiseVerify(self, vetImg, sensitivity, frameBHistogram, frame):
        """verefica se nao foi encontrado nenhum frame indicando ruido"""
        farFrame = frame + 1 #variavel que controla os frames seguintes a serem comparados com o atual e incrementada
        save = 1 #a variavel save permanecendo com um o frame devera ser gravado
        #enquanto nao for o fim do vetor e nao forem analisados os 20 frames e o frame ainda pode ser gravado
        while (farFrame < len(vetImg)) and (farFrame < (frame + 20)) and (save == 1):
            frameDHistogram = self.createHistogramBoxes(vetImg, farFrame) #armazena o histograma do frame distante a ser comparado
            #diferenca do frame atual para o distante a ser analisado
            farDiference = self.calculateBoxesHistogramDiference(frameBHistogram, frameDHistogram)
            #se a diferenca dos histogramas dos frames for menor do que a sensibilidade nao gravar o frame
            if not self.potentialShot(farDiference, sensitivity):
                save = 0

            farFrame = farFrame + 1 #passar para o proximo frame a ser comparado

        return save

