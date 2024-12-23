from moviepy.editor import CompositeVideoClip
import os
import nltk
from googletrans import Translator
from random import randint 
from functions import translate_text, audio_process, video_process, subtitles_process
import math

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

import tempfile
temp_dir = tempfile.mkdtemp()
change_settings({"TEMP_DIR": temp_dir})

# Baixar os recursos do NLTK necessários (apenas na primeira vez)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

from PIL import Image
# Substituindo ANTIALIAS por LANCZOS
Image.ANTIALIAS = Image.Resampling.LANCZOS

languages = {'english':['en', '#Quora #Reddit #English #USA #ForYou #FYP #TrendingNow #TikTokUSA #ExplorePage #Explore #TikTok #2024']}
            #  'spanish':['es', '#Quora #Reddit #Spanish #Spain #ParaTi #ForYou #FYP #TrendingNow #Descubre #Tendencias #TikTok #2024'],
            #  'german':['de', '#Quora #Reddit #German #Germany #ForYou #FYP #TrendingNow #TikTok #Entdecken #TrendsDeutschland #2024'],
            #  'portuguese':['pt', '#Quora #Reddit #Portugues #Portuguese #Brazil #Brasil #FYP #TrendingNow #Descubra #TikTok #2024'],
            #  'french':['fr', '#Quora #Reddit #French #France #FYP #TrendingNow #Découverte #TendancesFrance #TikTok #2024 #Canada']}

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

    i = 0
    translator = Translator()
    for language in list(languages):

        try:

            lang = languages.get(language)[0]

            text_array = translate_text(text_array, lang)

            audio, timestamps = audio_process(text_array, lang)

            video_name = video_files[randint(0, 6)]

            if audio.duration > 60:
                parts = round(audio.duration / 60)
            else:
                parts = 1
            part_size = round(len(text_array) / parts)
            text_arrays = [text_array[i:i + part_size] for i in range(0, len(text_array), part_size)]

            for i in range(parts):
                
                if parts > 1:

                    if i == 0:
                        first_phrase = text_arrays[i][0]
                        text_arrays[i][0] += f" (Part {i+1} of {parts})"
                    else:
                        text_arrays[i].insert(0, first_phrase + f" (Part {i+1} of {parts})")

                if i < parts-1:
                    text_arrays[i].append(f"Continues in part {i+2}")
                else:
                    text_arrays[i].append(f"Leave a like and follow for more!")
                
                audio, timestamps = audio_process(text_arrays[i], lang)

                video = video_process(video_name, audio)

                subtitles = subtitles_process(video, timestamps)

                # 6. Combine image and subtitles
                video = CompositeVideoClip([video] + subtitles)

                # 7. Export as video
                video_file = f"C:\\Users\\joaov\\Documents\\Video Editor Project\\Finished\\{text_file.split('.')[0]} - {language} - Part {i+1} of {parts} - {video_name.split('.')[0]}. {languages.get(language)[1]}.mp4"
                video.write_videofile(video_file, fps=24)

        except Exception as e:
            print(f"Erro no idioma {language} e arquivo {text_file}: {e}")
