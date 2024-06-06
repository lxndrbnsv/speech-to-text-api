import whisper

model = whisper.load_model("medium")


def detect_and_transcribe(filepath):
    audio = whisper.load_audio(filepath)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)

    lang = max(probs, key=probs.get)

    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    return lang, result.text