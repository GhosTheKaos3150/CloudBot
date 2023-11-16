import io

from os import environ
from google.cloud import vision
from google.oauth2 import service_account

from PIL import Image, ImageDraw, ImageFont

async def get_vision_annotated(file):
    credentials = service_account.Credentials.from_service_account_file("cloudbot-405122-70829b67fa85.json")
    
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = vision.Image()
    
    image.content = bytes(file)
    
    response = client.object_localization(image=image).localized_object_annotations
    
    print(response)
    
    font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', 20)
    img = Image.open(io.BytesIO(bytes(file)))
    draw = ImageDraw.Draw(img)
    
    color = ["red", "green", "blue", "pink", "white", "purple"]
    color_count = 0
    for object_ in response:
        ul_vt = object_.bounding_poly.normalized_vertices[0]
        dr_vt = object_.bounding_poly.normalized_vertices[2]
        
        text_vt = ((ul_vt.x*img.width)+1, (ul_vt.y*img.height))
        ul_vt = (ul_vt.x*img.width, ul_vt.y*img.height)
        dr_vt = (dr_vt.x*img.width, dr_vt.y*img.height)
        
        draw.rectangle([ul_vt, dr_vt], outline=color[color_count])
        draw.text(text_vt, object_.name, fill=color[color_count], font=font)
        
        color_count += 1
        if color == len(color):
            color_count = 0
    
    img.save("generated/vision.png", "PNG")