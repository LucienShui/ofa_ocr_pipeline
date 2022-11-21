import gradio as gr
from ofa_ocr import ofa_ocr_gr

if __name__ == "__main__":
    gr.close_all()
    with gr.TabbedInterface(
            [ofa_ocr_gr()],
            ["OFA OCR识别"],
    ) as demo:
        demo.launch()
