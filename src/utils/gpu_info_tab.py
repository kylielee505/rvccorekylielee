import gradio as gr
import torch


def gpu_info_tab():
    with gr.Tab("GPU Info"):
        gpu_info = gr.Markdown(render_gpu_info(get_gpu_info()))

        gr.Button("Refresh").click(
            fn=refresh_gpu_info, outputs=gpu_info, api_name="refresh_gpu_info"
        )

        gr.Button("API_GET_GPU_INFO", visible=False).click(
            fn=get_gpu_info, api_name="get_gpu_info"
        )


def get_gpu_info():
    if torch.cuda.is_available():
        vram = torch.cuda.get_device_properties(0).total_memory / 1024**2
        name = torch.cuda.get_device_properties(0).name
        cuda_capabilities = torch.cuda.get_device_capability(0)
        used_vram = torch.cuda.memory_allocated(0) / 1024**2
        used_vram_total = (
            torch.cuda.mem_get_info(0)[1] - torch.cuda.mem_get_info(0)[0]
        ) / 1024**2
        return {
            "vram": vram,
            "name": name,
            "cuda_capabilities": cuda_capabilities,
            "used_vram": used_vram,
            "used_vram_total": used_vram_total,
        }
    else:
        return "No GPU with CUDA support detected by PyTorch"


def render_gpu_info(gpu_info):
    if isinstance(gpu_info, dict):
        return f"VRAM: {gpu_info['vram']} MB\n\nUsed VRAM: {gpu_info['used_vram']} MB\n\nTotal Used VRAM: {gpu_info['used_vram_total']} MB\n\nName: {gpu_info['name']}\n\nCUDA Capabilities: {gpu_info['cuda_capabilities']}"
    else:
        return gpu_info


def refresh_gpu_info():
    return render_gpu_info(get_gpu_info())
