from PIL import Image


class Cutter:

    @staticmethod
    def cut(image, width, height):
        return image.resize((width, height))

    @staticmethod
    def open(filename):
        return Image.open(f'media/{filename}.jpg')

    def run(self, file, width, height):
        # image = self.open(file)
        return self.cut(file, width, height)
