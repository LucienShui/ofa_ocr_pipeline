---
license: Apache License 2.0

deployspec:
  image_id: "mshub-registry.cn-zhangjiakou.cr.aliyuncs.com/modelscope-repo/studio-service:py38-1.1.0rc0-0.3.3"
  cpu: 4
  memory: 8000
  gpu: 0
  gpu_memory: 16000
  instance: 1
---
#### Clone with HTTP
```bash
 git clone https://www.modelscope.cn/studios/damo/ofa_ocr_pipeline.git
```