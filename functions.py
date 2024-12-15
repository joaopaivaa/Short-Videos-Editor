from googletrans import Translator

def translate_text(text_array, lang):
    translator = Translator()
    text_array = [translator.translate(line, dest=lang).text for line in text_array] if lang != 'en' else text_array
    return text_array

def audio_process(text_array, lang):

    import pyttsx3
    from gtts import gTTS
    from moviepy.editor import AudioFileClip, vfx, concatenate_audioclips

    lang_voice = {'en': 1,
                  'es': 3,
                  'de': 5,
                  'pt': 0,
                  'fr': 4}

    timestamps = []
    last_duration = 0
    audio_clips = []
    for i in range(len(text_array)):
        audio_file_partial = f"Audios\\audio_{i}.mp3"
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        voice_id = lang_voice.get(lang)
        engine.setProperty('voice', voices[voice_id].id)
        engine.save_to_file(text_array[i], audio_file_partial)
        engine.runAndWait()
        # tts_partial = gTTS(text=text_array[i], lang=lang)
        # tts_partial.save(audio_file_partial)

        audio_partial = AudioFileClip(audio_file_partial)
        # audio_partial = audio_partial.fx(vfx.speedx, 1.2) if lang != 'pt' else audio_partial.fx(vfx.speedx, 1.6)
        actual_duration = audio_partial.duration

        timestamps.append([last_duration, last_duration + actual_duration, text_array[i]])
        last_duration = (last_duration + actual_duration)
        audio_clips.append(audio_partial)

    # Concatenar todos os clipes de áudio
    full_audio = concatenate_audioclips(audio_clips)
    full_audio.write_audiofile('Audios\\full_audio.mp3')

    return full_audio, timestamps

def video_process(video_name, audio):

    from moviepy.editor import vfx, VideoFileClip

    duracao_audio = audio.duration

    video_file = f'C:\\Users\\joaov\\Documents\\Video Editor Project\\Videos\\{video_name}'
    video = VideoFileClip(video_file)
    video = video.resize((1080, 1920))
    video = video.loop(duration=duracao_audio)
    video = video.subclip(0, duracao_audio)

    video = video.set_audio(audio)

    video = video.fx(vfx.fadeout, 1)

    return video

def subtitles_process(video, timestamps):

    from moviepy.editor import TextClip

    # Create TextClips for each subtitle segment
    subtitles = [TextClip(txt, font='Berlin-Sans-FB-Demi-Negrito', fontsize=80, color='white', size=(video.size[0]-100, video.size[1]), stroke_color = 'black', stroke_width = 4.5, method='caption')
                .set_start(start_time)
                .set_end(end_time)
                .margin(left=20, right=20)
                .set_position(('center', 'center'))
                for start_time, end_time, txt in timestamps]
    
    return subtitles