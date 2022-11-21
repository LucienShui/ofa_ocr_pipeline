import gradio as gr
import numpy as np
import urllib
import cv2
from PIL import Image
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys


def ofa_ocr_gr():
    def ocr_api(image):
        # step 1. orc detection to find boxes
        ocr_detection = pipeline(Tasks.ocr_detection,
                                 model='damo/cv_resnet18_ocr-detection-line-level_damo')
        result = ocr_detection(image)[OutputKeys.POLYGONS]

        # step 2. recognize ocr result according to ocr detection results
        ocr_recognize = pipeline(Tasks.ocr_recognition,
                                 model='damo/ofa_ocr-recognition_scene_base_zh')

        # OCR文字识别流程
        def ocr_pip(image_in, boxes):
            boxes = np.asarray(sorted(boxes.tolist(), key=lambda x: x[1]))
            if isinstance(image_in, str):
                req = urllib.request.urlopen(image_in)  # 读图片
                arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                img = cv2.imdecode(arr, -1)  # 'Load it as it is'
            elif isinstance(image_in, (Image.Image, np.ndarray)):
                img = image_in
            else:
                raise Exception(f'unsupported type of input image found[{type(image_in)}]!')
            img_return = img.copy()
            ret_l = list()
            index = 1
            for box in boxes:  # 因为检测结果是四边形，所以用透视变化转为长方形
                post1 = box.reshape((4, 2)).astype(np.float32)
                # draw rectangle & index for detection results
                p1, p2 = (int(np.min(post1[:, 0])), int(np.min(post1[:, 1]))), \
                         (int(np.max(post1[:, 0])), int(np.max(post1[:, 1])))
                # draw rectangle
                cv2.rectangle(img_return, p1, p2, (0, 0, 255), 4)

                p_text = p1[0] + 8 if p1[0] + 8 < p2[0] else p2[0], \
                         p1[1] + 25 if p1[1] + 25 < p2[1] else p2[1]
                # draw index
                cv2.putText(img_return, str(index), p_text, cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 0, 255), 2)

                width = box[4] - box[0]
                height = box[5] - box[1]
                post2 = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
                M = cv2.getPerspectiveTransform(post1, post2)
                new_img = cv2.warpPerspective(img, M, (width, height))
                new_img_pil = Image.fromarray(cv2.cvtColor(new_img, cv2.COLOR_BGR2RGB))
                # 开启文字识别
                ocr = ocr_recognize(new_img_pil)[OutputKeys.TEXT][0].replace(" ", "")
                ret_l.append([index, ocr])
                index += 1

            return img_return, ret_l

        return ocr_pip(image, result)

    examples = [
    ]

    title = "<h1 align='center'>基于OFA的OCR识别的应用</h1>"
    description = 'Gradio Demo for Chinese OCR based on OFA-Base. Upload your own image ' \
                  'or click any one of the examples, and click “Submit” and then wait for the ' \
                  'generated OCR result. 中文OCR体验区。欢迎上传图片，静待检测文字返回~'

    ocr_input_image = gr.components.Image(label='image')

    ocr_output_image = gr.components.Image(label='image')
    ocr_output_text = gr.components.Dataframe(headers=['Box ID', 'Text'])

    ocr_demo = gr.Interface(
        fn=ocr_api,
        inputs=[ocr_input_image],
        outputs=[ocr_output_image, ocr_output_text],
        title=title,
        description=description,
        allow_flagging='never',
        examples=examples
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
