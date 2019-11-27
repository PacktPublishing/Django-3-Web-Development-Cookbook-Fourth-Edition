from pilkit.lib import Image


class WatermarkOverlay(object):
    def __init__(self, watermark_image):
        self.watermark_image = watermark_image

    def process(self, img):
        original = img.convert('RGBA')
        overlay = Image.open(self.watermark_image)
        img = Image.alpha_composite(original, overlay).convert('RGB')
        return img
