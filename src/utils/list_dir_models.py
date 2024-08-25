import os
import gradio as gr

from src.tortoise.gr_reload_button import gr_open_button_simple, gr_reload_button
from src.utils.manage_model_state import unload_model


def list_dir_models(abs_dir: str):
    try:
        return [x for x in os.listdir(abs_dir) if x not in [".gitkeep", "cache"]]
    except FileNotFoundError as e:
        print(e)
        return []


def get_models(repos, abs_dir):
    return repos + [(x, os.path.join(abs_dir, x)) for x in list_dir_models(abs_dir)]


def model_select_ui(
    repos,
    abs_dir: str,
    prefix: str,
    Component: type[gr.Radio | gr.Dropdown] = gr.Radio,
):
    models = get_models(repos, abs_dir)
    model = Component(
        choices=models,
        label="Model",
        value=models[0][1],
    )
    gr_reload_button().click(
        fn=lambda: Component(choices=get_models(repos, abs_dir)),
        outputs=[model],
        api_name=f"{prefix}_get_models",
    )
    gr_open_button_simple(abs_dir, api_name=f"{prefix}_open_model_dir")
    return model


def unload_model_button(prefix: str):
    return gr.Button(value="Unload Model").click(
        fn=lambda: unload_model(model_namespace=prefix),
        api_name=f"{prefix}_unload_model",
    )
