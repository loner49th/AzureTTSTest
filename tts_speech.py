import azure.cognitiveservices.speech as speechsdk
import os
from typing import Optional
from dotenv import load_dotenv


class AzureTTS:
    def __init__(self, speech_key: str, service_region: str):
        """
        Azure Text-to-Speech クラスの初期化
        
        Args:
            speech_key: Azure Speech Service のAPIキー
            service_region: サービスリージョン (例: "japaneast")
        """
        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key, 
            region=service_region
        )
        
    def text_to_speech(
        self, 
        text: str, 
        voice_name: str = "ja-JP-NanamiNeural",
        output_file: Optional[str] = None,
        rate: Optional[str] = None,
        pitch: Optional[str] = None,
        volume: Optional[str] = None
    ) -> bool:
        """
        テキストを音声に変換
        
        Args:
            text: 音声合成するテキスト
            voice_name: 使用する音声 (デフォルト: 日本語女性音声)
            output_file: 出力ファイルパス (Noneの場合はスピーカーから再生)
            rate: 話速 (例: "slow", "medium", "fast", "0.5", "1.5")
            pitch: ピッチ (例: "low", "medium", "high", "-50Hz", "+50Hz")
            volume: 音量 (例: "silent", "soft", "medium", "loud", "50%")
            
        Returns:
            成功したかどうか
        """
        self.speech_config.speech_synthesis_voice_name = voice_name
        
        if output_file:
            audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
        else:
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
            
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config,
            audio_config=audio_config
        )
        
        try:
            # SSMLパラメータがある場合はSSMLを使用、そうでなければプレーンテキスト
            if rate or pitch or volume:
                ssml_text = self._create_ssml(text, voice_name, rate, pitch, volume)
                result = synthesizer.speak_ssml_async(ssml_text).get()
            else:
                result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                if output_file:
                    print(f"音声ファイルが保存されました: {output_file}")
                else:
                    print("音声の再生が完了しました")
                return True
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                print(f"音声合成がキャンセルされました: {cancellation_details.reason}")
                if cancellation_details.error_details:
                    print(f"エラー詳細: {cancellation_details.error_details}")
                return False
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return False
            
        return False
    
    def get_available_voices(self) -> list:
        """
        利用可能な音声一覧を取得
        
        Returns:
            音声情報のリスト
        """
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
        voices_result = synthesizer.get_voices_async().get()
        
        if voices_result.reason == speechsdk.ResultReason.VoicesListRetrieved:
            return [voice for voice in voices_result.voices]
        else:
            print("音声一覧の取得に失敗しました")
            return []
    
    def _create_ssml(
        self, 
        text: str, 
        voice_name: str,
        rate: Optional[str] = None,
        pitch: Optional[str] = None,
        volume: Optional[str] = None
    ) -> str:
        """
        SSMLテキストを生成
        
        Args:
            text: 音声合成するテキスト
            voice_name: 使用する音声
            rate: 話速
            pitch: ピッチ
            volume: 音量
            
        Returns:
            SSML形式のテキスト
        """
        prosody_attrs = []
        
        if rate:
            prosody_attrs.append(f'rate="{rate}"')
        if pitch:
            prosody_attrs.append(f'pitch="{pitch}"')
        if volume:
            prosody_attrs.append(f'volume="{volume}"')
        
        if prosody_attrs:
            prosody_start = f'<prosody {" ".join(prosody_attrs)}>'
            prosody_end = '</prosody>'
            prosody_text = f'{prosody_start}{text}{prosody_end}'
        else:
            prosody_text = text
        
        ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="ja-JP">
    <voice name="{voice_name}">
        {prosody_text}
    </voice>
</speak>'''
        
        return ssml


def main():
    """
    メイン関数 - 使用例
    """
    # .envファイルから環境変数を読み込み
    load_dotenv()
    
    # 環境変数から認証情報を取得
    speech_key = os.getenv('AZURE_SPEECH_KEY')
    service_region = os.getenv('AZURE_SPEECH_REGION', 'japaneast')
    
    if not speech_key:
        print("AZURE_SPEECH_KEY環境変数を設定してください")
        return
    
    # TTSインスタンスを作成
    tts = AzureTTS(speech_key, service_region)
    
    # テキストを音声に変換
    text = "こんにちは。Azure Text-to-Speechのテストです。"

    tts.text_to_speech(text)
    

    # 日本語の他の音声を使用
    print("男性音声で再生します...")
    tts.text_to_speech(text, voice_name="ja-JP-KeitaNeural")
    
    print("複数のパラメータを組み合わせて再生します...")
    tts.text_to_speech(text, rate="1.5", pitch="+50Hz", volume="loud",output_file="output.wav")


if __name__ == "__main__":
    main()