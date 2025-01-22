from moviepy.editor import CompositeVideoClip
import os
import nltk
from googletrans import Translator
from random import randint 
from functions import translate_text, audio_process, video_process, subtitles_process
import re
import asyncio

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

languages = {#'english':['en', '#Quora #Reddit #ForYou #FYP #TrendingNow #2025'],
            'spanish':['es', '#Quora #Reddit #ForYou #FYP #TrendingNow #2025']}
            #'portuguese':['pt', '#Quora #Reddit #ForYou #FYP #TrendingNow #2025']
            #  'german':['de', '#Quora #Reddit #German #Germany #ForYou #FYP #TrendingNow #TikTok #Entdecken #TrendsDeutschland #2024'],
            #  'french':['fr', '#Quora #Reddit #French #France #FYP #TrendingNow #Découverte #TendancesFrance #TikTok #2024 #Canada']}

# Listar todos os arquivos na pasta
video_files = os.listdir('C:\\Users\\joaov\\Documents\\Video Editor Project\\Videos')

# Listar todos os arquivos na pasta
text_files = os.listdir('C:\\Users\\joaov\\Documents\\Video Editor Project\\Texts')

for text_file in text_files:

    # text_array = []
    
    with open(f'C:\\Users\\joaov\\Documents\\Video Editor Project\\Texts\\{text_file}', 'r', encoding='utf-8') as file:
        full_text = file.read()
        full_text = full_text.replace('\n', ' ')
        text_array = re.split(r'(?<=[.,!?])', full_text)
        text_array = [sentence.strip() for sentence in text_array if sentence.strip()]

    #     for line in file:
    #         text_array.append(line.strip())
    # full_text = " ".join(text_array)

    i = 0
    translator = Translator()
    for language in list(languages):

        try:
            
            lang = languages.get(language)[0]

            text_array = asyncio.run(translate_text(text_array, lang))

            audio, timestamps = audio_process(text_array, lang)

            video_name = video_files[randint(0, 1)]

            if audio.duration > 60:
                parts = round(audio.duration / 60)
            else:
                parts = 1
            part_size = round(len(text_array) / parts)
            text_arrays = [text_array[i:i + part_size] for i in range(0, len(text_array), part_size)]

            for i in range(parts):

                if language == 'english':
                    complement_phrase = f" (Part {i+1} of {parts})"
                elif language == 'spanish' or language == 'portuguese':
                    complement_phrase = f" (Parte {i+1} de {parts})"
                
                if parts > 1:
                    if i == 0:
                        first_phrase = text_arrays[i][0]
                        text_arrays[i][0] += complement_phrase
                    else:
                        text_arrays[i].insert(0, first_phrase + complement_phrase)

                if i < parts-1:
                    if language == 'english':
                        end_phrase = f"Continues in part {i+2}"
                    elif language == 'spanish':
                        end_phrase = f"Continúa en la parte {i+2}"
                    elif language == 'portuguese':
                        end_phrase = f"Continua na parte {i+2}"
                    text_arrays[i].append(end_phrase)

                else:
                    if language == 'english':
                        end_phrase =  f"Leave a like and follow for more!"
                    elif language == 'spanish':
                        end_phrase =  f"¡Deja un like y sigue para más!"
                    elif language == 'portuguese':
                        end_phrase =  f"Deixe um like e siga para mais!"
                    text_arrays[i].append(end_phrase)
                
                audio, timestamps = audio_process(text_arrays[i], lang)

                video = video_process(video_name, audio)

                subtitles = subtitles_process(video, timestamps)

                # 6. Combine image and subtitles
                video = CompositeVideoClip([video] + subtitles)

                # 7. Export as video
                video_file = f"C:\\Users\\joaov\\Documents\\Video Editor Project\\Finished\\{text_array[0][:-1]} {complement_phrase}. {languages.get(language)[1]}.mp4"
                video.write_videofile(video_file, fps=24)

        except Exception as e:
            print(f"Erro no idioma {language} e arquivo {text_file}: {e}")
