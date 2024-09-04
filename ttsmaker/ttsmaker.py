import requests
import json

class TTSError(Exception):
	"""自定义异常类，用于处理TTS订单中的错误"""
	pass

class TTSOrder:
	def __init__(self, tts_data):
		"""
		初始化 TTSOrder 类。
		:param tts_data: dict, 包含生成的 TTS 订单的相关信息。
		"""
		self.status = tts_data.get('status')
		self.error_details = tts_data.get('error_details')
		self.audio_file_url = tts_data.get('audio_file_url')
		self.audio_file_type = tts_data.get('audio_file_type')
		self.tts_data = tts_data

	def save_audio(self, filename):
		"""
		保存音频文件到本地。
		:param filename: str, 文件名，不需要提供扩展名，扩展名将使用音频文件类型。
		"""
		if self.status != 'success':
			raise TTSError(f"Cannot save audio. TTS generation failed: {self.error_details}")

		audio_format = self.audio_file_type
		filepath = f"{filename}.{audio_format}"
		
		# 下载音频文件
		response = requests.get(self.audio_file_url)
		if response.status_code == 200:
			with open(filepath, 'wb') as f:
				f.write(response.content)
			print(f"Audio file saved as {filepath}")
		else:
			raise TTSError(f"Failed to download audio file from URL: {self.audio_file_url}")


class TTSMaker:
	def __init__(self, token='ttsmaker_demo_token'):
		"""
		初始化 TTSMaker 类，提供开发者 Token。
		:param token: str, 开发者Token，用于验证API请求，默认值为 'ttsmaker_demo_token'。
		"""
		self.token = token or 'ttsmaker_demo_token'
		self.base_url = "https://api.ttsmaker.cn/v1/"


	def get_voice_list(self, language='zh'):
		"""
		获取可用语言和语音的列表。
		:param language: str, 可选参数，默认值为 'zh'，指定支持的语言。可选值：["en", "zh", "es", "ja", "ko", "de", "fr", "it", "ru", "pt", "tr", "ms", "th", "vi", "id", "he"]。
		                如果None，则获取所有可用语音列表。
		:return: dict, 包含语音列表的 JSON 响应。
		"""
		url = f"{self.base_url}get-voice-list"
		params = {'token': self.token}
		if language:
			params['language'] = language
		response = requests.get(url, params=params)
		return response.json()


	def create_tts_order(self, text, voice_id, audio_format='mp3', audio_speed=1.0, audio_volume=0, text_paragraph_pause_time=0):
		"""
		创建 TTS 订单，将文本转换为语音，并生成可下载的音频文件URL。
		
		:param text: str, 需要转换为语音的文本，必填项。
		             该文本会被语音合成引擎转换为音频文件，支持中文、英文及其他多种语言。
		:param voice_id: int, 语音 ID，必填项。需要选择一个可用的语音 ID（可以通过 get_voice_list 方法获取）。
		:param audio_format: str, 音频格式，可选参数。支持的格式包括 'mp3', 'ogg', 'aac', 'opus'。默认值为 'mp3'。
		:param audio_speed: float, 音频速度，可选参数。范围为 0.5 至 2.0，表示语速的百分比。例如：0.5 表示语速为50%，2.0 表示语速为200%。默认值为 1.0。
		:param audio_volume: float, 音频音量，可选参数。范围为 0 至 10，表示音量增加的百分比。例如：1 表示音量+10%，8 表示音量+80%，10 表示音量+100%。默认值为 0，不调整音量。
		:param text_paragraph_pause_time: int, 段落暂停时间，可选参数。用于在段落之间自动插入暂停，单位为毫秒。范围为 500 至 5000 毫秒，最多可以插入 50 次暂停。超过50次将会被自动取消。默认值为 0，不插入暂停。
		
		:return: TTSOrder, 包含 TTS 订单结果的对象。如果订单失败，将抛出 TTSError 异常。
		"""
		url = f"{self.base_url}create-tts-order"
		headers = {'Content-Type': 'application/json; charset=utf-8'}
		data = {
			'token': self.token,
			'text': text,
			'voice_id': voice_id,
			'audio_format': audio_format,
			'audio_speed': audio_speed,
			'audio_volume': audio_volume,
			'text_paragraph_pause_time': text_paragraph_pause_time
		}

		response = requests.post(url, headers=headers, data=json.dumps(data))
		tts_data = response.json()

		if tts_data['status'] != 'success':
			raise TTSError(f"TTS generation failed: {tts_data.get('error_details', 'Unknown error')}")

		return TTSOrder(tts_data)


	def get_token_status(self):
		"""
		查看开发者 Token 的配额字符、已使用字符、配额重置日期等信息。
		
		:param 无
		:return: dict, 返回包含Token状态的 JSON 响应。返回的内容包括总配额字符数、已使用字符数、剩余字符数及下次配额重置日期等信息。
		"""
		url = f"{self.base_url}get-token-status"
		params = {'token': self.token}
		response = requests.get(url, params=params)
		return response.json()
