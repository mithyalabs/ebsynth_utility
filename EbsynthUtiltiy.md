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