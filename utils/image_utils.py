from PIL import Image
import io

def prepare_image(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    image.thumbnail((1800, 1800))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=88, optimize=True)
    buffer.seek(0)
    return buffer.read(), image
