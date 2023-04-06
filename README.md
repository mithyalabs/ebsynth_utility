# ebsynth_utility

## Overview
#### AUTOMATIC1111 UI extension for creating videos using img2img and ebsynth.
#### This extension allows you to output edited videos using ebsynth.(AE is not required)


##### With [Controlnet](https://github.com/Mikubill/sd-webui-controlnet) installed, I have confirmed that all features of this extension are working properly!  
##### [Controlnet](https://github.com/Mikubill/sd-webui-controlnet) is a must for video editing, so I recommend installing it.  
##### Multi ControlNet("canny" + "normal map") would be suitable for video editing.  


## Example
- The following sample is raw output of this extension.  
#### sample 1 mask with [clipseg](https://github.com/timojl/clipseg)  
- first from left : original  
- second from left : masking "cat" exclude "finger"  
- third from left : masking "cat head"  
- right : color corrected with [color-matcher](https://github.com/hahnec/color-matcher) (see stage 3.5)  
- Multiple targets can also be specified.(e.g. cat,dog,boy,girl)  
<div><video controls src="https://user-images.githubusercontent.com/118420657/223008549-167beaee-1453-43fa-85ce-fe3982466c26.mp4" muted="false"></video></div>

#### sample 2 blend background
- person : masterpiece, best quality, masterpiece, 1girl, masterpiece, best quality,anime screencap, anime style  
- background : cyberpunk, factory, room ,anime screencap, anime style  
- It is also possible to blend with your favorite videos.  
<div><video controls src="https://user-images.githubusercontent.com/118420657/214592811-9677634f-93bb-40dd-95b6-1c97c8e7bb63.mp4" muted="false"></video></div>

#### sample 3 auto tagging
- left : original  
- center : apply the same prompts in all keyframes  
- right : apply auto tagging by deepdanbooru in all keyframes  
- This function improves the detailed changes in facial expressions, hand expressions, etc.  
  In the sample video, the "closed_eyes" and "hands_on_own_face" tags have been added to better represent eye blinks and hands brought in front of the face.  
<div><video controls src="https://user-images.githubusercontent.com/118420657/218247502-6c8e04fe-859b-4739-8c9d-0bf459d04e3b.mp4" muted="false"></video></div>

#### sample 4 auto tagging (apply lora dynamically)
- left : apply auto tagging by deepdanbooru in all keyframes  
- right : apply auto tagging by deepdanbooru in all keyframes + apply "anyahehface" lora dynamically  
- Added the function to dynamically apply TI, hypernet, Lora, and additional prompts according to automatically attached tags.  
  In the sample video, if the "smile" tag is given, the lora and lora trigger keywords are set to be added according to the strength of the "smile" tag.  
  Also, since automatically added tags are sometimes incorrect, unnecessary tags are listed in the blacklist.  
  [Here](sample/) is the actual configuration file used. placed in "Project directory" for use.  
<div><video controls src="https://user-images.githubusercontent.com/118420657/218247633-ab2b1e6b-d81c-4f1d-af8a-6a97df23be0e.mp4" muted="false"></video></div>

<br>

## Installation
- Install [ffmpeg](https://ffmpeg.org/) for your operating system
  (https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/)
- Install [Ebsynth](https://ebsynth.com/)
- Use the Extensions tab of the webui to [Install from URL]

<br>
<br>

## Usage
- Go to [Ebsynth Utility] tab.
- Create an empty directory somewhere, and fill in the "Project directory" field.
- Place the video you want to edit from somewhere, and fill in the "Original Movie Path" field.
  Use short videos of a few seconds at first.
- Select stage 1 and Generate.
- Execute in order from stage 1 to 7.
  Progress during the process is not reflected in webui, so please check the console screen.
  If you see "completed." in webui, it is completed.  
(In the current latest webui, it seems to cause an error if you do not drop the image on the main screen of img2img.  
Please drop the image as it does not affect the result.)  

<br>
<br>

## Note 1
For reference, here's what I did when I edited a 1280x720 30fps 15sec video based on
#### Stage 1
There is nothing to configure.  
All frames of the video and mask images for all frames are generated.  
  
#### Stage 2
In the implementation of this extension, the keyframe interval is chosen to be shorter where there is a lot of motion and longer where there is little motion.  
If the animation breaks up, increase the keyframe, if it flickers, decrease the keyframe.  
First, generate one time with the default settings and go straight ahead without worrying about the result.  

  
#### Stage 3
Select one of the keyframes, throw it to img2img, and run [Interrogate DeepBooru].  
Delete unwanted words such as blur from the displayed prompt.  
Fill in the rest of the settings as you would normally do for image generation.  
  
Here is the settings I used.  
- Sampling method : Euler a  
- Sampling Steps : 50  
- Width : 960  
- Height : 512  
- CFG Scale : 20  
- Denoising strength : 0.2  
  
Here is the settings for extension.  
- Mask Mode(Override img2img Mask mode) : Normal
- Img2Img Repeat Count (Loop Back) : 5  
- Add N to seed when repeating : 1
- use Face Crop img2img : True  
- Face Detection Method : YuNet  
- Max Crop Size : 1024  
- Face Denoising Strength : 0.25  
- Face Area Magnification : 1.5 (The larger the number, the closer to the model's painting style, but the more likely it is to shift when merged with the body.)  
- Enable Face Prompt : False  
  
Trial and error in this process is the most time-consuming part.  
Monitor the destination folder and if you do not like results, interrupt and change the settings.  
[Prompt][Denoising strength] and [Face Denoising Strength] settings when using Face Crop img2img will greatly affect the result.  
For more information on Face Crop img2img, check [here](https://github.com/s9roll7/face_crop_img2img)
  
If you have lots of memory to spare, increasing the width and height values while maintaining the aspect ratio may greatly improve results.  
  
This extension may help with the adjustment.  
https://github.com/s9roll7/img2img_for_all_method  

<br>

**The information above is from a time when there was no controlnet.  
When controlnet are used together (especially multi-controlnets),
Even setting "Denoising strength" to a high value works well, and even setting it to 1.0 produces meaningful results.  
If "Denoising strength" is set to a high value, "Loop Back" can be set to 1.**  

<br>

#### Stage 4
Scale it up or down and process it to exactly the same size as the original video.  
This process should only need to be done once.  
  
- Width : 1280  
- Height : 720  
- Upscaler 1 : R-ESRGAN 4x+  
- Upscaler 2 : R-ESRGAN 4x+ Anime6B  
- Upscaler 2 visibility : 0.5  
- GFPGAN visibility : 1  
- CodeFormer visibility : 0  
- CodeFormer weight : 0  
  
#### Stage 5
There is nothing to configure.  
.ebs file will be generated.  
  
#### Stage 6
Run the .ebs file.  
I wouldn't change the settings, but you could adjust the .ebs settings.  

#### Stage 7
Finally, output the video.  
In my case, the entire process from 1 to 7 took about 30 minutes.  
  
- Crossfade blend rate : 1.0  
- Export type : mp4  

<br>
<br>

## Note 2 : How to use multi-controlnet together  
#### in webui setting  
![controlnet_setting](imgs/controlnet_setting.png "controlnet_setting")
<br>
#### In controlnet settings in img2img tab(for controlnet 0)  
![controlnet_0](imgs/controlnet_0.png "controlnet_0")
<br>
#### In controlnet settings in img2img tab(for controlnet 1)  
![controlnet_1](imgs/controlnet_1.png "controlnet_1")
<br>
#### In ebsynth_utility settings in img2img tab  
**Warning : "Weight" in the controlnet settings is overridden by the following values**
![controlnet_option_in_ebsynthutil](imgs/controlnet_option_in_ebsynthutil.png "controlnet_option_in_ebsynthutil")

<br>
<br>

## Note 3 : How to use clipseg  
![clipseg](imgs/clipseg.png "How to use clipseg")




#Setup

##Stage 1 (Extract frames and mask)
To extract frames from video at `/home/ubuntu/elephant.mp4`
```sh
curl -X 'POST' \
  'http://192.18.143.57/ebsynth/process' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "stage_index": 0,
    "project_dir": "/home/ubuntu/ebs-out",
    "original_movie_path": "/home/ubuntu/elephant.mp4",
    "frame_width": -1,
    "frame_height": -1,
    "st1_masking_method_index": 0,
    "st1_mask_threshold": 0,
    "tb_use_fast_mode": false,
    "tb_use_jit": false,
    "clipseg_mask_prompt": "",
    "clipseg_exclude_prompt": "",
    "clipseg_mask_threshold": 0.4,
    "clipseg_mask_blur_size": 11,
    "clipseg_mask_blur_size2": 11,
    "key_min_gap": 10,
    "key_max_gap": 300,
    "key_th": 8.5,
    "key_add_last_frame": true,
    "color_matcher_method": "hm-mkl-hm",
    "st3_5_use_mask": true,
    "st3_5_use_mask_ref": false,
    "st3_5_use_mask_org": false,
    "color_matcher_ref_type": 0,
    "color_matcher_ref_image": null,
    "blend_rate": 1,
    "export_type": "mp4",
    "bg_src": "",
    "bg_type": "Fit video length",
    "mask_blur_size": 5,
    "mask_threshold": 0,
    "fg_transparency": 0,
    "mask_mode": "Normal"
}'
```
This will put extracted frames at `/home/ubuntu/ebs-out/video-frame/%05d.png` and mask frames at `/home/ubuntu/ebs-out/video-mask/%05d.png`

##Stage 2 (Select Key Frames)
```sh
curl -X 'POST' \
  'http://192.18.143.57/ebsynth/process' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "stage_index": 1,
    "project_dir": "/home/ubuntu/ebs-out",
    "original_movie_path": "/home/ubuntu/elephant.mp4",
    "frame_width": -1,
    "frame_height": -1,
    "st1_masking_method_index": 0,
    "st1_mask_threshold": 0,
    "tb_use_fast_mode": false,
    "tb_use_jit": false,
    "clipseg_mask_prompt": "",
    "clipseg_exclude_prompt": "",
    "clipseg_mask_threshold": 0.4,
    "clipseg_mask_blur_size": 11,
    "clipseg_mask_blur_size2": 11,
    "key_min_gap": 10,
    "key_max_gap": 300,
    "key_th": 8.5,
    "key_add_last_frame": true,
    "color_matcher_method": "hm-mkl-hm",
    "st3_5_use_mask": true,
    "st3_5_use_mask_ref": false,
    "st3_5_use_mask_org": false,
    "color_matcher_ref_type": 0,
    "color_matcher_ref_image": null,
    "blend_rate": 1,
    "export_type": "mp4",
    "bg_src": "",
    "bg_type": "Fit video length",
    "mask_blur_size": 5,
    "mask_threshold": 0,
    "fg_transparency": 0,
    "mask_mode": "Normal"
}'
```
This will create a folder `/home/ubuntu/ebs-out/video-key/%05d.png` with key frame images

##Stage 3 (Controlnet Image to image)
TBD


##Stage 4 (Upscale)
```sh
curl -X 'POST' \
  'http://192.18.143.57/sdapi/v1/extra-batch-images' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "resize_mode": 1,
  "show_extras_results": true,
  "gfpgan_visibility": 0,
  "codeformer_visibility": 0,
  "codeformer_weight": 0,
  "upscaling_resize": 2,
  "upscaling_resize_w": 1024,
  "upscaling_resize_h": 576,
  "upscaling_crop": true,
  "upscaler_1": "R-ESRGAN 4x+",
  "upscaler_2": "R-ESRGAN 4x+",
  "extras_upscaler_2_visibility": 0,
  "upscale_first": false,
  "imageList": [
    {
      "data": "<BASE_64_IMAGE>",
      "name": "firstimage"
    }
  ]
}'
```

Response
```json
{
  "resize_mode": 1,
  "show_extras_results": true,
  "gfpgan_visibility": 0,
  "codeformer_visibility": 0,
  "codeformer_weight": 0,
  "upscaling_resize": 2,
  "upscaling_resize_w": 1024,
  "upscaling_resize_h": 576,
  "upscaling_crop": true,
  "upscaler_1": "R-ESRGAN 4x+",
  "upscaler_2": "R-ESRGAN 4x+",
  "extras_upscaler_2_visibility": 0,
  "upscale_first": false,
  "imageList": [
    {
      "data": "<BASE_64_UPSCALED_IMAGE>",
      "name": "firstimage"
    }
  ]
}
```

Place these images at `/home/ubuntu/ebs-out/img2img_upscale_key/%05d.png`

##Stage 5, 6 (Ebsynth)
Run ebsynth for keyframes
`00001.png`  `00023.png`  `00039.png`  `00057.png`  `00075.png`  `00089.png`  `00122.png`  `00153.png`  `00203.png`  `00253.png`  `00302.png`

![Ebsynth](https://pub-706bf4a189d94a6b8bfe844e4aaf385a.r2.dev/ebsynth_image.png)

##stage 7 (Crossfading)
```sh
curl -X 'POST' \
  'http://192.18.143.57/ebsynth/process' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "stage_index": 7,
    "project_dir": "/home/ubuntu/ebs-out",
    "original_movie_path": "/home/ubuntu/elephant.mp4",
    "frame_width": -1,
    "frame_height": -1,
    "st1_masking_method_index": 0,
    "st1_mask_threshold": 0,
    "tb_use_fast_mode": false,
    "tb_use_jit": false,
    "clipseg_mask_prompt": "",
    "clipseg_exclude_prompt": "",
    "clipseg_mask_threshold": 0.4,
    "clipseg_mask_blur_size": 11,
    "clipseg_mask_blur_size2": 11,
    "key_min_gap": 10,
    "key_max_gap": 300,
    "key_th": 8.5,
    "key_add_last_frame": true,
    "color_matcher_method": "hm-mkl-hm",
    "st3_5_use_mask": true,
    "st3_5_use_mask_ref": false,
    "st3_5_use_mask_org": false,
    "color_matcher_ref_type": 0,
    "color_matcher_ref_image": null,
    "blend_rate": 1,
    "export_type": "mp4",
    "bg_src": "",
    "bg_type": "Fit video length",
    "mask_blur_size": 5,
    "mask_threshold": 0,
    "fg_transparency": 0,
    "mask_mode": "Normal"
}'
```

Ouput video will be placed at `/home/ubuntu/ebs-out/20230406-155729_with_snd.mp4`