from fastapi import FastAPI, Body
import gradio as gr
from ebsynth_utility import ebsynth_utility_process

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
        key_min_gap:int = Body(),
        key_max_gap:int = Body(), 
        key_th:float = Body(),
        key_add_last_frame:bool  = Body() , 
        color_matcher_method:str  = Body(),
        st3_5_use_mask:bool =  Body(), 
        st3_5_use_mask_ref:bool  = Body(), 
        st3_5_use_mask_org:bool  = Body(), 
        color_matcher_ref_type:int  = Body(),
        color_matcher_ref_image:Image = Body(), 
        blend_rate:float = Body(), 
        export_type:str = Body(), 
        bg_src:str = Body(),
        bg_type:str = Body(), 
        mask_blur_size:int  = Body(), 
        mask_threshold:float  = Body(), 
        fg_transparency:float  = Body(),
        mask_mode:str  = Body()
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

try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_app_started(ebsynth_utility_api)
except:
    pass