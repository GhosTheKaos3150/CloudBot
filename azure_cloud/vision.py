import io
import os
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import azure.ai.vision as sdk

load_dotenv()
service_options = sdk.VisionServiceOptions(os.environ["VISION_ENDPOINT"],
                                           os.environ["VISION_KEY"])
file = "2c.webp"

image = f"../assets/{file}"

vision_source = sdk.VisionSource(filename=image)
print("passou")
analysis_options = sdk.ImageAnalysisOptions()

analysis_options.features = (
    sdk.ImageAnalysisFeature.OBJECTS
)

analysis_options.gender_neutral_caption = True

image_analyzer = sdk.ImageAnalyzer(service_options, vision_source, analysis_options)

result = image_analyzer.analyze()

font = ImageFont.truetype(r'C:\Users\System-Pc\Desktop\arial.ttf', 20)
img = Image.open(io.BytesIO(open(image, "rb").read()))
draw = ImageDraw.Draw(img)
color = ["red", "blue", "lightgreen", "pink", "white", "purple"]
color_count = 0
for object_ in result.objects:
    print(object_)

for object_ in result.objects:
    ul_vt = (object_.bounding_box.x,object_.bounding_box.y)
    dr_vt = (object_.bounding_box.x+object_.bounding_box.w,object_.bounding_box.y+object_.bounding_box.h)
    
    text_vt = (ul_vt[0]+1, ul_vt[1])
    text2_vt = (ul_vt[0]+1, ul_vt[1]+50)

    draw.rectangle([ul_vt, dr_vt], outline=color[color_count])
    draw.text(text_vt, object_.name, fill=color[color_count], font=font)
    draw.text(text2_vt, str(object_.confidence), fill=color[color_count], font=font)
    
    color_count += 1
    if color == len(color):
        color_count = 0
img.save("../generated/vision_azure.png", "PNG")