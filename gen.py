from PIL import Image, ImageOps

from copy import deepcopy as DEEP

from random import randrange


class Frame:

    def __init__(self, standart, x, y, width, height, pieceFolder, extension):

        self.extension = extension

        self.pieceFolder = pieceFolder

        self.pieces = []

        self.XP, self.YP = x, y

        self.canvas = standart.resize((x * width, y * height))

    def fetchPiece(self, fileName):  # don't add the extension

        Image.open(self.pieceFolder + "/" + fileName)

    def putAPiece(self, pieceFile: str, x, y):

        coor = (x, y)

        if coor in self.pieces:
            raise Exception("the piece already exists")

        piece = Image.open(self.pieceFolder + "/" + pieceFile)

        self.pieces.append(coor)

        self.canvas.paste(piece, (((x) * piece.size[0]),  ((y) * piece.size[1])))

    @staticmethod
    def initStandart(x, y, folder) -> Image:
        piece = Image.open("blank.png")

        return Frame(piece, x, y, piece.size[0], piece.size[1],  folder, ".png")

    def nextRandomFrame(self) -> Image:

        current = DEEP(self)

        if len(self.pieces) >= (self.XP * self.YP):
            return current

        coor = (1, 1)

        while True:

            coor = (randrange(0, self.XP), randrange(0, self.YP))

            if coor not in self.pieces:

                break

        pieceName = str( (self.XP - (coor[0])) + ( (self.YP - coor[1] - 1) * self.XP)) + self.extension

        current.putAPiece(pieceName, coor[0], coor[1])

        return current

    def show(self):

        self.canvas.show()


def newPuzzle(image, target, extension, XP, YP, XL, YL):

    base = Image.open(image)

    base.resize((XP*XL, YP*YL))

    blank = Image.open("blank.png")

    blank = ImageOps.contain(blank, (XL, YL))

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


X = 32
Y = 20

newPuzzle("turkish_flag.png", "32x20", ".png", X, Y, 34, 34)

f = Frame.initStandart(X, Y, "32x20")


for i in range(X * Y):

    f = f.nextRandomFrame()

    f.canvas.save("frames/" + str(i + 1) + ".png")

