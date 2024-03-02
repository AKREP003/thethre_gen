from PIL import Image, ImageOps

from copy import deepcopy as DEEP

from random import randrange

import __main__


class Frame:

    def __init__(self, standart, x, y, width, height, pieceFolder, extension):

        self.extension = extension

        self.pieceFolder = pieceFolder

        self.pieces = []

        self.XP, self.YP = x, y

        self.canvas = standart

    def fetchPiece(self, fileName):  # don't add the extension

        Image.open(self.pieceFolder + "/" + fileName)

    def putARegularPiece(self, pieceFile: str, x, y):

        coor = (x, y)

        if coor in self.pieces:
            raise Exception("the piece already exists")

        piece = Image.open(self.pieceFolder + "/" + pieceFile)

        self.pieces.append(coor)

        self.canvas.paste(piece, (((x) * piece.size[0]),  ((y) * piece.size[1])))

    @staticmethod
    def initStandart(x, y, folder) -> Image:
        piece = Image.open("x.png")



        return Frame(piece, x, y, piece.size[0], piece.size[1],  folder, ".png")

    def nextRandomFrame(self):

        coor = (1, 1)

        while True:

            coor = (randrange(0, self.XP), randrange(0, self.YP))

            if coor not in self.pieces:
                break
        return coor

    def completePiece(self, coor) -> Image:
        current = DEEP(self)
        if len(self.pieces) >= (self.XP * self.YP):
            return current

        pieceName = str(abs((self.XP - (coor[0])) + ((self.YP - coor[1] - 1) * self.XP))) + self.extension

        current.putARegularPiece(pieceName, coor[0], coor[1])

        return current

    def show(self):

        self.canvas.show()


def newPuzzle(image, target, extension, XP, YP):

    base = Image.open(image)

    blank = Image.open("blank.png")

    blank = ImageOps.fit(blank, (base.width // XP, base.height // YP))

    print((base.width // XP, base.height // YP))

    print(blank.size)

    blank.save("blank.png")

    width = base.width // XP
    height = base.height // YP


    for yth in range(0,YP):


        for xth in range(0,XP):


            x = xth * width
            y = yth * height

            piecePosition = (x, y, x + width, y + height)

            piece = base.crop(piecePosition)

            piece.save(f"{target}/{(XP * YP) - (xth + (yth * XP)) }{extension}")


def ordered():
    X = 9
    Y = 1

    # newPuzzle("turkish_flag.png", "flag_pieces_9x1", ".png", X, Y)

    f = Frame.initStandart(X, Y, "flag_pieces_9x1")

    optimalPlacing = [(8, 0), (0, 0), (7, 0), (1, 0), (6, 0), (2, 0), (5, 0), (3, 0), (4, 0)]

    counter = 0

    for i in optimalPlacing:
        c = i

        print(c)

        f = f.completePiece(c)

        f.canvas.save("frames_9x1/" + str(counter + 1) + ".png")

        counter += 1
