# EasyOCR Lite

从EasyOCR提取文本定位有关代码，进一步适配中文，修正缺陷

## 安装

Python版本至少为3.8。


首先按照PyTorch官方说明安装PyTorch。

```
pip install -e .
```

## 使用

``` python3
from easyocrlite import ReaderLite

reader = ReaderLite()
results = reader.process('my_awesome_handwriting.png')
```

返回的内容为边界框和对应的图像区域的列表。
其它说明见[demo](./demo.ipynb)。


## 致谢

基于[EasyOCR](https://github.com/JaidedAI/EasyOCR)修改实现。以下为EasyOCR致谢：

This project is based on research and code from several papers and open-source repositories.

All deep learning execution is based on [Pytorch](https://pytorch.org). :heart:

Detection execution uses the CRAFT algorithm from this [official repository](https://github.com/clovaai/CRAFT-pytorch) and their [paper](https://arxiv.org/abs/1904.01941) (Thanks @YoungminBaek from [@clovaai](https://github.com/clovaai)). We also use their pretrained model. Training script is provided by [@gmuffiness](https://github.com/gmuffiness).

The recognition model is a CRNN ([paper](https://arxiv.org/abs/1507.05717)). It is composed of 3 main components: feature extraction (we are currently using [Resnet](https://arxiv.org/abs/1512.03385)) and VGG, sequence labeling ([LSTM](https://www.bioinf.jku.at/publications/older/2604.pdf)) and decoding ([CTC](https://www.cs.toronto.edu/~graves/icml_2006.pdf)). The training pipeline for recognition execution is a modified version of the [deep-text-recognition-benchmark](https://github.com/clovaai/deep-text-recognition-benchmark) framework. (Thanks [@ku21fan](https://github.com/ku21fan) from [@clovaai](https://github.com/clovaai)) This repository is a gem that deserves more recognition.

Beam search code is based on this [repository](https://github.com/githubharald/CTCDecoder) and his [blog](https://towardsdatascience.com/beam-search-decoding-in-ctc-trained-neural-networks-5a889a3d85a7). (Thanks [@githubharald](https://github.com/githubharald))

Data synthesis is based on [TextRecognitionDataGenerator](https://github.com/Belval/TextRecognitionDataGenerator). (Thanks [@Belval](https://github.com/Belval))

And a good read about CTC from distill.pub [here](https://distill.pub/2017/ctc/).


## 许可证 (注意！)
Apache 2.0