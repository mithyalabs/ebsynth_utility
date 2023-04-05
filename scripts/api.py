from fastapi import FastAPI, Body
import gradio as gr
from ebsynth_utility import ebsynth_utility_process
from custom_script import Script

# class ApiHijack(api.Api):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.add_api_route("/ebsynth/test", self.ebsynth_utility, methods=["POST"], response_model=str)

#     def ebsynth_utility(self):
#         return 'test ebsynth api'

# api.Api = ApiHijack


def ebsynth_utility_api(_:gr.Blocks, app: FastAPI):

    @app.post("/ebsynth/process")
    async def ebsynth_process(
        stage_index: int = Body(-1, title="Stage index"),
        project_dir: str = Body("none", title="Project directory"),
        original_movie_path: str = Body("none", title="Original Movie path"),
        frame_width:int = Body(-1, title="Frame width"),
        frame_height:int = Body(-1, title="Frame height"),
        st1_masking_method_index: int = Body(1, title="Stage 1 masking method index"),
        st1_mask_threshold:float = Body(0.0, title="Stage 1 mask threshold") ,
        tb_use_fast_mode:bool = Body(False, title="Use Fast mode"),
        tb_use_jit:bool = Body(False, title="Use Jit"),
        clipseg_mask_prompt:str = Body("none", title="Mask Target (e.g., girl, cats)"),
        clipseg_exclude_prompt:str = Body("none", title="Exclude Target (e.g., finger, book)"),
        clipseg_mask_threshold:int= Body(0.4, title="'Mask Threshold", ge=0, le=1),
        clipseg_mask_blur_size:int = Body(11, title="Mask Blur Kernel Size(MedianBlur)", ge=1, le=150),
        clipseg_mask_blur_size2: int = Body(11, title="Mask Blur Kernel Size(GaussianBlur)", ge=1, le=150),
        key_min_gap:int = Body(10, title="Minimum Gap between Keyframes", ge=1, le=500),
        key_max_gap:int = Body(300, title="Maximum Gap between Keyframes", ge=1, le=1000), 
        key_th:float = Body(8.5, title="Threshold of delta frame edge", ge=0, le=100),
        key_add_last_frame:bool  = Body(True) , 
        color_matcher_method:str  = Body("hm-mkl-hm", title="Color Transfer Method"),
        st3_5_use_mask:bool =  Body(True), 
        st3_5_use_mask_ref:bool  = Body(False), 
        st3_5_use_mask_org:bool  = Body(False), 
        color_matcher_ref_type:int  = Body(0),
        color_matcher_ref_image:str = Body(default=None), 
        blend_rate:float = Body(1, title="Crossfade blend Rate", ge=0, le=1), 
        export_type:str = Body("mp4", title="Export Type"), 
        bg_src:str = Body(default=None),
        bg_type:str = Body("Fit video length"), 
        mask_blur_size:int  = Body(5, title="Mask Blur Kernel Size", ge=1, le=150), 
        mask_threshold:float  = Body(0.0, title="Mask Threshold", ge=0, le=1), 
        fg_transparency:float  = Body(0.0, title="Foreground Transparency", ge=0, le=1),
        mask_mode:str  = Body("Normal")
    ):
        ebsynth_utility_process(
                    stage_index,

                    project_dir,
                    original_movie_path,

                    frame_width,
                    frame_height,
                    st1_masking_method_index,
                    st1_mask_threshold,
                    tb_use_fast_mode,
                    tb_use_jit,
                    clipseg_mask_prompt,
                    clipseg_exclude_prompt,
                    clipseg_mask_threshold,
                    clipseg_mask_blur_size,
                    clipseg_mask_blur_size2,

                    key_min_gap,
                    key_max_gap,
                    key_th,
                    key_add_last_frame,

                    color_matcher_method,
                    st3_5_use_mask,
                    st3_5_use_mask_ref,
                    st3_5_use_mask_org,
                    color_matcher_ref_type,
                    color_matcher_ref_image,

                    blend_rate,
                    export_type,

                    bg_src,
                    bg_type,
                    mask_blur_size,
                    mask_threshold,
                    fg_transparency,

                    mask_mode,
        )
        return {"success": True, "stage": stage_index, "project_dir": project_dir, "movie_path": original_movie_path}



    @app.post("/controlnet/ebsynth-utility")
    async def controlnet_ebsynth_utility(
        project_dir:str = Body("", title="Project directory"),
        generation_test:bool = Body(False, title="Generation TEST!!(Ignore Project directory and use the image and mask specified in the main UI)"),
        mask_mode:str = Body("Normal", title="Mask Mode(Override img2img Mask mode)"),
        inpaint_area:int = Body(1, title="Inpaint Area(Override img2img Inpaint area)"),
        use_depth:bool = Body(True, title="Use Depth Map If exists in /video_key_depth"),
        img2img_repeat_count:int = Body(1, title="Img2Img Repeat Count (Loop Back)", ge=1, le=30),
        inc_seed:str = Body(1, title="Add N to seed when repeating", ge=1, le=9999999),
        auto_tag_mode:str = Body("None", title="Auto Tagging"),
        add_tag_to_head:bool = Body(False, title="Add additional prompts to the head"),
        add_tag_replace_underscore:bool = Body(False, title="Replace '_' with ' '(Does not affect the function to add tokens using add_token.txt.)"),
        is_facecrop:bool = Body(False, title="use Face Crop img2img"),
        face_detection_method:str = Body("YuNet", title="Face Detection Method"),
        face_crop_resolution:int = Body(512, title="Face Crop Resolution", ge=128, le=2048),
        max_crop_size:str = Body(1024, title="Max Crop Size", ge=0, le=2048),
        face_denoising_strength:float = Body(0.5, title="Face Denoising Strength", ge=0, le=1),
        face_area_magnification:float = Body(1.5, title="Face Area Magnification", ge=0, le=10),
        enable_face_prompt:bool = Body(False, title="Enable Face Prompt"),
        face_prompt:str = Body("face close up", title="Face Prompt"),
        controlnet_weight:float = Body(0.5, title="Control Net Weight", ge=0, le=2),
        controlnet_weight_for_face:float = Body(0.5, title="Control Net Weight For Face", ge=0, le=2),
        disable_facecrop_lpbk_last_time:bool = Body(False, title="Disable at the last loopback time"),
        use_preprocess_img:bool = Body(True, title="Use Preprocess image If exists in /controlnet_preprocess"),
    ):
        
        print({
            "project_dir": project_dir,
            "generation_test": generation_test,
            "mask_mode": mask_mode,
            "inpaint_area": inpaint_area,
            "use_depth": use_depth,
            "img2img_repeat_count": img2img_repeat_count,
            "inc_seed": inc_seed,
            "auto_tag_mode": auto_tag_mode,
            "add_tag_to_head": add_tag_to_head,
            "add_tag_replace_underscore": add_tag_replace_underscore,
            "is_facecrop": is_facecrop,
            "face_detection_method": face_detection_method,
            "face_crop_resolution": face_crop_resolution,
            "max_crop_size": max_crop_size,
            "face_denoising_strength": face_denoising_strength,
            "face_area_magnification": face_area_magnification,
            "enable_face_prompt": enable_face_prompt,
            "face_prompt": face_prompt,
            "controlnet_weight": controlnet_weight,
            "controlnet_weight_for_face": controlnet_weight_for_face,
            "disable_facecrop_lpbk_last_time": disable_facecrop_lpbk_last_time,
            "use_preprocess_img": use_preprocess_img
        })

        # TODO:// get model p

        # script = Script()
        # script.run(
        #     p,
        #     project_dir,
        #     generation_test,
        #     mask_mode,
        #     inpaint_area,
        #     use_depth,
        #     img2img_repeat_count,
        #     inc_seed,
        #     auto_tag_mode,
        #     add_tag_to_head,
        #     add_tag_replace_underscore,
        #     is_facecrop,
        #     face_detection_method,
        #     face_crop_resolution,
        #     max_crop_size,
        #     face_denoising_strength,
        #     face_area_magnification,
        #     enable_face_prompt,
        #     face_prompt,
        #     controlnet_weight,
        #     controlnet_weight_for_face,
        #     disable_facecrop_lpbk_last_time,
        #     use_preprocess_img,
        # )


try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(ebsynth_utility_api)
except:
    pass