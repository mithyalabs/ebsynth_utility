import os
import glob
import requests
import json
import base64

def get_image_paths(folder):
    image_extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp")
    files = []
    for ext in image_extensions:
        files.extend(glob.glob(os.path.join(folder, ext)))
    return sorted(files)


def send_request(last_image_path, current_image_path, options = {}):
    url = "http://localhost:7860/sdapi/v1/img2img"

    with open(last_image_path, "rb") as f:
        last_image = base64.b64encode(f.read()).decode("utf-8")

    with open(current_image_path, "rb") as b:
        current_image = base64.b64encode(b.read()).decode("utf-8")

    options.alwayson_scripts.ControlNet.args[0].input_image = current_image
    options.alwayson_scripts.ControlNet.args[1].input_image = last_image

    response = requests.post(url, json=options)
    if response.status_code == 200:
        return json.loads(response.content).images[0]
    else:
        try:
            error_data = response.json()
            print("Error:")
            print(str(error_data))
            
        except json.JSONDecodeError:
            print(f"Error: Unable to parse JSON error data.")
        return None

def temporal(init_image_path, input_images_folder, output_images_folder, options):
    input_images = get_image_paths(input_images_folder)
    last_image = send_request(init_image_path, input_images[0], options)

    for i in range(1, len(input_images)):
        output_image_path = os.path.join(output_images_folder, f"{i}.png".rjust(9, '0'))
        with open(output_image_path, "wb") as f:
            f.write(base64.b64decode(last_image))
        last_image = send_request(output_image_path, input_images_folder, input_images[i])
        print(f"Written data for frame {i}:")
