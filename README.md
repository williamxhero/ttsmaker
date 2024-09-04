# TTSMaker

TTSMaker is a Python library that allows you to interact with the TTSMaker API to convert text to speech. 

https://ttsmaker.cn/developer-api-docs

## Installation

You can install the library using pip:

```bash
pip install ttsmaker
```

## Usage

```python
from ttsmaker import TTSMaker

ttsmaker = TTSMaker()

order = ttsmaker.create_tts_order("我们来聊聊天", voice_id=1504)
order.save_audio("audio_file")
```