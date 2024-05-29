import os
import random
import shutil

import colorama
import nightcore as nc
from moviepy.editor import ImageClip AudioFileClip
colorama.init()


# take the name of the audio files in the 'ingredients' folder and returns a list
def take_audio(list_files):

    list_audio = []

    for element in list_files:
        for suffix_audio in list_suffix_audio:
            if suffix_audio in element:
                list_audio.append(element)
    return list_audio


# take an image/a random image in the 'ingredients' folder
def take_img(list_files, list_suffix_img):

    list_bgs = []
    print(list_files)

    for element in list_files:
        for suffix_img in list_suffix_img:
            if suffix_img in element:
                list_bgs.append(element)
                print(list_bgs)
    # check if the list contains more than 1 image
    # if yes pick a random one
    try:
        if len(list_bgs) > 1:
            r = random.randint(0, len(list_bgs)-1)
            bg = list_bgs[r]
            return bg

        bg = list_bgs[0]
        return bg
    except IndexError:
        pass


# create the nightcore song
def nightcorize(list_suffix_audio):
    os.chdir("ingredients")

    list_files = os.listdir()

    list_audio = take_audio(list_files)

    if not os.path.exists("done"):
        os.mkdir("done")

    # for every audio in the folder increase the tone
    for audio in list_audio:

        # increase the tone by 2 and export the song
        nc_audio = f"{audio}" @ nc.Tones(2)
        nc_audio.export(f"{audio}_nightcorized.mp3")

        # move the audio in the folder 'done'
        shutil.move(audio, "done")

        print(f"[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] {audio} nightcorized!")


# create the final video
def merge(list_suffix_img):
    print(f"\n[{colorama.Fore.YELLOW}.{colorama.Fore.WHITE}] Creating video...\n")

    # create the final directory (where the merged video will be created)
    if not os.path.exists(f"{base_dir}/final"):
        os.mkdir(f"{base_dir}/final")

    list_files = os.listdir()

    list_audio = take_audio(list_files)

    for audio in list_audio:
        bg = take_img(list_files, list_suffix_img)

        # use ffmpeg to merge image and audio
        # 'subprocess.Popen' may be better the 'os.system'
        os.system(f"ffmpeg -y -i {bg} -i {audio} -codec copy {audio}_merged.mp4")

        # move the video to the final directory
        shutil.move(f"{audio}_merged.mp4", f"{base_dir}/final")

        # remove the nightcore song (only the audio)
        os.remove(f"{audio}")

        print(f"\n[{colorama.Fore.GREEN}V{colorama.Fore.WHITE}] {audio} created!\n")


base_dir = os.getcwd()
list_suffix_img = [".png", ".jpg", ".jpeg", ".tiff", ".jfif", ".webp", ".gif"]
list_suffix_audio = [".mp3", ".wav", ".ogg", ".m4a", ".m4r"]

nightcorize(list_suffix_audio)


def create_video(image_path, audio_path, output_path, duration=None):
    # Charger l'image
    image_clip = ImageClip(image_path)

    # Charger l'audio
    audio_clip = AudioFileClip(audio_path)
    
    # Déterminer la durée de la vidéo
    video_duration = duration if duration else audio_clip.duration
    
    # Définir la durée de l'image (qui devient une vidéo)
    image_clip = image_clip.set_duration(video_duration)
    
    # Associer l'audio à la vidéo
    video_clip = image_clip.set_audio(audio_clip)
    
    # Exporter la vidéo
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

# Chemins des fichiers
audio_path = "ingredients/done/thea.mp3"
image_path = "ingredients/Rplot01.png"
output_path = "ta_video.mp4"

# Créer la vidéo
create_video(image_path, audio_path, output_path)