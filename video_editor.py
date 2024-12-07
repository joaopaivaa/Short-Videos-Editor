from gtts import gTTS
from moviepy.editor import AudioFileClip, TextClip, CompositeVideoClip, vfx, VideoFileClip, concatenate_videoclips, concatenate_audioclips
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from googletrans import Translator
from random import randint 

from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

import tempfile

temp_dir = tempfile.mkdtemp()
change_settings({"TEMP_DIR": temp_dir})

# Baixar os recursos do NLTK necessários (apenas na primeira vez)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

languages = {'english':['en', ['English','USA','UK','ForYou','FYP','TrendingNow','TikTokUSA','ExplorePage','Explore','TikTok','2024']],
             'spanish':['es', ['Spanish','Spain','Europe','ParaTi','ForYou','FYP','TrendingNow','Descubre','Tendencias','TikTok','2024']],
             'german':['de', ['German','Germany','ForYou','FYP','TrendingNow','TikTok','Entdecken','TrendsDeutschland','2024']],
             'portuguese':['pt', ['Portugues','Portuguese','Brazil','Brasil','FYP','TrendingNow','Descubra','TikTok','2024']],
             'french':['fr', ['French','France','Paris','FYP','TrendingNow','Découverte','TendancesFrance','TikTok','2024','Canada']]}

from PIL import Image
# Substituindo ANTIALIAS por LANCZOS
Image.ANTIALIAS = Image.Resampling.LANCZOS

#subtitles_option = 'Each Word'
subtitles_option = 'Each Phrase'

# Listar todos os arquivos na pasta
video_files = os.listdir('C:\\Users\\joaov\\Documents\\Video Editor Project\\Videos')

# Listar todos os arquivos na pasta
text_files = os.listdir('C:\\Users\\joaov\\Documents\\Video Editor Project\\Texts')

for text_file in text_files:

    text_array = []
    with open(f'C:\\Users\\joaov\\Documents\\Video Editor Project\\Texts\\{text_file}', 'r', encoding='utf-8') as file:
        for line in file:
            text_array.append(line.strip())
    full_text = " ".join(text_array)
    
    if subtitles_option == 'Each Word':
        text_array = full_text.split(' ')

    i = 0
    translator = Translator()
    for language in list(languages):

        try:

            # full_text = translator.translate(full_text, dest=languages.get(language)[0]).text if language != 'english' else full_text

            #  = word_tokenize(full_text.lower())

            # stop_words = set(stopwords.words(language))

            # cleaned_words = [word for word in words if word.isalnum() and word not in stop_words]

            # frequency = Counter(cleaned_words)

            # keywords = frequency.most_common(5)

            # keywords = [keyword.title() for keyword, freq in keywords]

            # text_array = [translator.translate(line, dest=languages.get(language)[0]).text for line in text_array] if language != 'english' else text_array

            #keywords = keywords + ['Quora','Reddit'] + languages.get(language)[1]
            keywords = ['Quora','Reddit'] + languages.get(language)[1]
            keywords.sort()

            keywords_final = ''
            for i in range(len(keywords)):
                keywords_final = keywords_final + ' #' + keywords[i] if i != 0 else keywords_final + '#' + keywords[i]

            lang = languages.get(language)[0]

            timestamps = []
            last_duration = 0
            audio_clips = []
            for i in range(len(text_array)):
                tts_partial = gTTS(text=text_array[i], lang=lang)
                audio_file_partial = f"Audios\\audio_{i}.mp3"
                tts_partial.save(audio_file_partial)
                audio_partial = AudioFileClip(audio_file_partial)
                audio_partial = audio_partial.fx(vfx.speedx, 1.4) if language != 'portuguese' else audio_partial.fx(vfx.speedx, 1.6)
                actual_duration = audio_partial.duration

                timestamps.append([last_duration, last_duration + actual_duration, text_array[i]])
                last_duration = (last_duration + actual_duration)
                audio_clips.append(audio_partial)

            # Concatenar todos os clipes de áudio
            full_audio = concatenate_audioclips(audio_clips)
            full_audio.write_audiofile('Audios\\full_audio.mp3')

            # 2. Load the audio and get its duration automatically
            audio = AudioFileClip('Audios\\full_audio.mp3')
            duracao_audio = audio.duration  # Audio duration in seconds

            video_name = video_files[randint(0, 6)]
            video_file = f'C:\\Users\\joaov\\Documents\\Video Editor Project\\Videos\\{video_name}'
            video = VideoFileClip(video_file)
            video = video.resize((1080, 1920))
            video = video.loop(duration=duracao_audio)
            video = video.subclip(0, duracao_audio)

            video = video.set_audio(audio)
        
            # Create TextClips for each subtitle segment
            subtitles = [TextClip(txt, font='Berlin-Sans-FB-Demi-Negrito', fontsize=80, color='white', size=(video.size[0]-100, video.size[1]), stroke_color = 'black', stroke_width = 4.5, method='caption')
                        .set_start(start_time)
                        .set_end(end_time)
                        .margin(left=20, right=20)
                        .set_position(('center', 'center'))
                        for start_time, end_time, txt in timestamps]

            # 6. Combine image and subtitles
            video = CompositeVideoClip([video] + subtitles)

            video = video.fx(vfx.fadeout, 1)

            # 7. Export as video
            video_file = f"{text_file.split('.')[0]} - {language} - {video_name.split('.')[0]}. {keywords_final}.mp4"
            video.write_videofile(video_file, fps=24)

        except Exception as e:
            print(f"Erro no idioma {language} e arquivo {text_file}: {e}")
