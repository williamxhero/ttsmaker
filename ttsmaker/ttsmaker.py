import requests
import json

class TTSError(Exception):
	"""Custom exception class for handling errors in TTS orders"""
	pass

class TTSOrder:
	def __init__(self, tts_data):
		"""
		Initialize the TTSOrder class.
		:param tts_data: dict, contains relevant information about the generated TTS order.
		"""
		self.status = tts_data.get('status')
		self.error_details = tts_data.get('error_details')
		self.audio_file_url = tts_data.get('audio_file_url')
		self.audio_file_type = tts_data.get('audio_file_type')
		self.tts_data = tts_data

	def save_audio(self, filename):
		"""
		Save the audio file to local storage.
		:param filename: str, file name, extension is not required as the audio file type will be used.
		"""
		if self.status != 'success':
			raise TTSError(f"Cannot save audio. TTS generation failed: {self.error_details}")

		audio_format = self.audio_file_type
		filepath = f"{filename}.{audio_format}"
		
		# Download the audio file
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
		Initialize the TTSMaker class with the developer token.
		:param token: str, developer token for API request authentication, default value is 'ttsmaker_demo_token'.
		"""
		self.token = token or 'ttsmaker_demo_token'
		self.base_url = "https://api.ttsmaker.cn/v1/"


	def get_voice_list(self, language='zh'):
		"""
		Get the list of available languages and voices.
		:param language: str, optional parameter, default is 'zh', specifies the supported language. 
		                 Available options: ["en", "zh", "es", "ja", "ko", "de", "fr", "it", "ru", "pt", "tr", "ms", "th", "vi", "id", "he"].
		                 If None, retrieves the full list of available voices.
		:return: dict, the JSON response containing the voice list.
		"""
		url = f"{self.base_url}get-voice-list"
		params = {'token': self.token}
		if language:
			params['language'] = language
		response = requests.get(url, params=params)
		return response.json()


	def create_tts_order(self, text, voice_id, audio_format='mp3', audio_speed=1.0, audio_volume=0, text_paragraph_pause_time=0):
		"""
		Create a TTS order to convert text to speech and generate a downloadable audio file URL.
		
		:param text: str, the text to be converted into speech, required field.
		             This text will be processed by the speech synthesis engine to generate an audio file, supporting Chinese, English, and other languages.
		:param voice_id: int, voice ID, required field. A valid voice ID must be selected (retrieved through the get_voice_list method).
		:param audio_format: str, audio format, optional parameter. Supported formats include 'mp3', 'ogg', 'aac', 'opus'. Default is 'mp3'.
		:param audio_speed: float, audio speed, optional parameter. Range is from 0.5 to 2.0, indicating the percentage of speech speed. 
		                    For example, 0.5 means 50% speed, 2.0 means 200% speed. Default is 1.0.
		:param audio_volume: float, audio volume, optional parameter. Range is from 0 to 10, indicating the percentage of volume increase. 
		                     For example, 1 means +10% volume, 8 means +80%, and 10 means +100%. Default is 0, no volume adjustment.
		:param text_paragraph_pause_time: int, paragraph pause time, optional parameter. 
		                                  Used to insert pauses between paragraphs automatically, in milliseconds. Range is from 500 to 5000 ms. 
		                                  A maximum of 50 pauses can be inserted; if exceeded, the pauses will be automatically canceled. Default is 0, no pause insertion.
		
		:return: TTSOrder, an object containing the TTS order result. If the order fails, a TTSError exception will be raised.
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
		Check the quota characters, used characters, quota reset date, and other information for the developer token.
		
		:param None
		:return: dict, returns the JSON response containing the token status. Includes total quota characters, used characters, remaining characters, and next reset date.
		"""
		url = f"{self.base_url}get-token-status"
		params = {'token': self.token}
		response = requests.get(url, params=params)
		return response.json()
