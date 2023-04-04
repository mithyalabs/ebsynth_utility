from fastapi import FastAPI, Body
import gradio as gr
from modules.api import api


def ebsynth_utility(self):
    return 'test ebsynth api'

class ApiHijack(api.Api):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_api_route("/ebsynth/test", self.ebsynth_utility, methods=["POST"], response_model=str)

    def ebsynth_utility(self):
    return 'test ebsynth api'

api.Api = ApiHijack


# def controlnet_api(_: gr.Blocks, app: FastAPI):

# try:
#     import modules.script_callbacks as script_callbacks

#     script_callbacks.on_app_started(controlnet_api)
# except:
#     pass