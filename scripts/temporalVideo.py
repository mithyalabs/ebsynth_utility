import os
import glob
import requests
import json
from pprint import pprint
import base64
from io import BytesIO


# Replace with the actual path to your image file and folder
x_path = "./init.png"
y_folder = "./Input_Images"

output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

def get_image_paths(folder):
    image_extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    files = []
    for ext in image_extensions:
        files.extend(glob.glob(os.path.join(folder, ext)))
    return sorted(files)

y_paths = get_image_paths(y_folder)

def send_request(last_image_path, temp_path,current_image_path):
    url = "http://localhost:7860/sdapi/v1/img2img"

    with open(last_image_path, "rb") as f:
        last_image = base64.b64encode(f.read()).decode("utf-8")

    with open(current_image_path, "rb") as b:
        current_image = base64.b64encode(b.read()).decode("utf-8")

    data = {
        "init_images": [current_image],
        "inpainting_fill": 0,
        "inpaint_full_res": True,
        "inpaint_full_res_padding": 1,
        "inpainting_mask_invert": 1,
        "resize_mode": 0,
        "denoising_strength": 0.45,
        "prompt": "pop art, painting, highly detailed,",
        "negative_prompt": "(ugly:1.3), (fused fingers), (too many fingers), (bad anatomy:1.5), (watermark:1.5), (words), letters, untracked eyes, asymmetric eyes, floating head, (logo:1.5), (bad hands:1.3), (mangled hands:1.2), (missing hands), (missing arms), backward hands, floating jewelry, unattached jewelry, floating head, doubled head, unattached head, doubled head, head in body, (misshapen body:1.1), (badly fitted headwear:1.2), floating arms, (too many arms:1.5), limbs fused with body, (facial blemish:1.5), badly fitted clothes, imperfect eyes, untracked eyes, crossed eyes, hair growing from clothes, partial faces, hair not attached to head",
        "alwayson_scripts": {
            "ControlNet":{
                "args": [
                    {
                        "input_image": current_image,
                        "module": "hed",
                        "model": "control_hed-fp16 [13fee50b]",
                        "weight": 1.5,
                        "guidance": 1,
                   },
                    {
                        "input_image": last_image,
                        "model": "diff_control_sd15_temporalnet_fp16 [adc6bd97]",
                        "module": "none",
                        "weight": 0.7,
                        "guidance": 1,
                    }
                  
                ]
            }
        },
        "seed": 3189343382,
        "subseed": -1,
        "subseed_strength": -1,
        "sampler_index": "Euler a",
        "batch_size": 1,
        "n_iter": 1,
        "steps": 20,
        "cfg_scale": 6,
        "width": 512,
        "height": 512,
        "restore_faces": True,
        "include_init_images": True,
        "override_settings": {},
        "override_settings_restore_afterwards": True
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.content
    else:
        try:
            error_data = response.json()
            print("Error:")
            print(str(error_data))
            
        except json.JSONDecodeError:
            print(f"Error: Unable to parse JSON error data.")
        return None

output_images = []
output_images.append(send_request(x_path,y_folder, y_paths[0]))
output_paths = []

for i in range(1, len(y_paths)):
     result_image = output_images[i-1]
     temp_image_path = os.path.join(output_folder, f"temp_image_{i}.png")
     data = json.loads(result_image)
     encoded_image = data["images"][0]
     with open(temp_image_path, "wb") as f:
         f.write(base64.b64decode(encoded_image))
     output_paths.append(temp_image_path)
     result = send_request(temp_image_path, y_folder, y_paths[i])
     output_images.append(result)
     print(f"Written data for frame {i}:")