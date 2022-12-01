import os
os.system('cd ezocr;'
          'pip install .; cd ..')


import gradio as gr
import pandas as pd
from PIL import ImageDraw
from easyocrlite import ReaderLite
from PIL import Image
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys

# step 1. orc detection to find boxes
reader = ReaderLite(gpu=True)

# step 2. recognize ocr result according to ocr detection results
ocr_recognize = pipeline(Tasks.ocr_recognition,
                         model='damo/ofa_ocr-recognition_general_base_zh', model_revision='v1.0.0')


def get_images(img: str, reader: ReaderLite, **kwargs):
    results = reader.process(img, **kwargs)
    return results


def draw_boxes(image, bounds, color='red', width=4):
    draw = ImageDraw.Draw(image)
    for i, bound in enumerate(bounds):
        p0, p1, p2, p3 = bound
        draw.text((p0[0]+5, p0[1]+5), str(i+1), fill=color, align='center')
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    return image


def ofa_ocr_gr():
    def ocr_api(img):
        results = get_images(img, reader, max_size=4000, text_confidence=0.7, text_threshold=0.4,
                             link_threshold=0.4, slope_ths=0., add_margin=0.04)
        box_list, image_list = zip(*results)
        draw_boxes(img, box_list)

        ocr_result = []
        for i, (box, image) in enumerate(zip(box_list, image_list)):
            image = Image.fromarray(image)
            result = ocr_recognize(image)[OutputKeys.TEXT][0].replace(" ", "")
            ocr_result.append([str(i + 1), result.replace(' ', '')])

        result = pd.DataFrame(ocr_result, columns=['Box ID', 'Text'])

        return img, result

    examples = [
        "http://xingchen-data.oss-cn-zhangjiakou.aliyuncs.com/maas/ocr/qiaodaima.png",
        "http://xingchen-data.oss-cn-zhangjiakou.aliyuncs.com/maas/ocr/shupai.png",
        "http://xingchen-data.oss-cn-zhangjiakou.aliyuncs.com/maas/ocr/ocr_essay.jpg",
        "http://xingchen-data.oss-cn-zhangjiakou.aliyuncs.com/maas/ocr/chinese.jpg",
        "http://xingchen-data.oss-cn-zhangjiakou.aliyuncs.com/maas/ocr/benpao.jpeg",
        "http://xingchen-data.oss-cn-zhangjiakou.aliyuncs.com/maas/ocr/gaidao.jpeg",
    ]

    title = "<h1 align='center'>基于OFA的OCR识别的应用</h1>"
    description = 'Gradio Demo for Chinese OCR based on OFA-Base. Upload your own image ' \
                  'or click any one of the examples, and click “Submit” and then wait for the ' \
                  'generated OCR result. 中文OCR体验区。欢迎上传图片，静待检测文字返回~'

    ocr_input_image = gr.components.Image(label='image', type='pil')

    ocr_output_image = gr.components.Image(label='image')
    ocr_output_text = gr.components.Dataframe(headers=['Box ID', 'Text'])

    ocr_demo = gr.Interface(
        fn=ocr_api,
        inputs=[ocr_input_image],
        outputs=[ocr_output_image, ocr_output_text],
        title=title,
        description=description,
        allow_flagging='never',
        examples=examples,
        examples_per_page=5,
        cache_examples=True
    )

    return ocr_demo


if __name__ == "__main__":
    with gr.TabbedInterface(
            [ofa_ocr_gr()],
            ["OCR识别"],
    ) as demo:
        demo.launch(
            enable_queue=True,
        )
