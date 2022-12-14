---
license: Apache License 2.0
domain:
- multi-modal
tags:
- Alibaba
- OFA
- OCR
- 光学字符识别

models:
- damo/ofa_ocr-recognition_general_base_zh
- damo/ofa_ocr-recognition_scene_base_zh
- damo/ofa_ocr-recognition_document_base_zh
- damo/ofa_ocr-recognition_handwriting_base_zh
- damo/ofa_ocr-recognition_web_base_zh

deployspec:
  image_id: "mshub-registry.cn-zhangjiakou.cr.aliyuncs.com/modelscope-repo/studio-service:py38-1.1.0rc0-0.3.3"
  cpu: 8
  memory: 20000
  gpu: 1
  gpu_memory: 8000
  instance: 1
---
# OFA文字识别PIPELINE
大部分OCR模型一般只能识别单行文字，且很多效果很好的OCR模型不支持finetune，现在OFA推出文字识别pipeline，可以有更优的体验，这里抛砖引玉，希望大家可以针对自己的场景训练出更合适的模型！

OFA(One-For-All)是通用多模态预训练模型，使用简单的序列到序列的学习框架统一模态（跨模态、视觉、语言等模态）和任务（如图片生成、视觉定位、图片描述、图片分类、文本生成等），详见我们发表于ICML 2022的论文：[OFA: Unifying Architectures, Tasks, and Modalities Through a Simple Sequence-to-Sequence Learning Framework](https://arxiv.org/abs/2202.03052)，以及我们的官方Github仓库[https://github.com/OFA-Sys/OFA](https://github.com/OFA-Sys/OFA)。


#### Clone with HTTP
```bash
 git clone https://www.modelscope.cn/studios/damo/ofa_ocr_pipeline.git
```