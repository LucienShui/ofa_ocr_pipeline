import gradio as gr
from ofa_ocr import ofa_ocr_gr

if __name__ == "__main__":
    gr.close_all()
    ocr_demo = ofa_ocr_gr()
    ocr_demo.launch(
        enable_queue=True,
    )
