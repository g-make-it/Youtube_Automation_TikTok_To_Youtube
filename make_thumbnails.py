import os
import random
from PIL import Image
from moviepy.editor import *
import os
import random

class BuildThumbnail():

    def run(self, target_string):
        self.create_snapshots_from_videos(target_string)
        self.joining_thumbnails(target_string)

    # creating 'snapshots' from final compiled video
    def create_snapshots_from_videos(self, target_string):
        search_term = target_string
        # search_term = "Can't You See Me?"
        chars = "\\`*_{}[]()>#+-.!$?�"
        for c in chars:
            search_term = search_term.replace(c, '')

        path_compliation_images = './compliation_vids_images/'
        compliation_vids_path = './compilation_vids/'
        thumbnails_made_path = './final_thumbnails/'
        thumbnails_made = set(os.listdir(thumbnails_made_path))

        compliation_vids_file_names = os.listdir(compliation_vids_path)

        for file in compliation_vids_file_names:

            # tiktok_compliation_<number> . mp4
            filename = file.split('.')[0]
            if filename in thumbnails_made:
                continue
            folder_of_a_single_compliation_image_folder = path_compliation_images + filename
            if not os.path.exists(folder_of_a_single_compliation_image_folder):
                os.makedirs(folder_of_a_single_compliation_image_folder)

            single_video_clip = compliation_vids_path + file
            video = VideoFileClip(single_video_clip)

            total_time = video.duration
            for _ in range(3):
                full_path_for_image = folder_of_a_single_compliation_image_folder + '/' + filename + f'_{_}.png'
                # e.g. 10 * 1/4
                interval = (total_time * ((_ + 1) / 4.0))
                video.save_frame(full_path_for_image, t=interval)

        print('snapshots complete')

    # making final thumbnails
    def joining_thumbnails(self, target_string):
        search_term = target_string
        # search_term = "Can't You See Me?"
        chars = "\\`*_{}[]()>#+-.!$?�"
        for c in chars:
            search_term = search_term.replace(c,'')

        path_compliation_images = './compliation_vids_images/'
        path_thumbnails = './final_thumbnails/'
        thumbnails_made = set(os.listdir(path_thumbnails))

        list_of_folders_of_images_compilation = os.listdir(path_compliation_images)

        for folder in list_of_folders_of_images_compilation:
            # making sure made thumbnails are not remade again
            converted_to_file = folder + '.png'
            if converted_to_file in thumbnails_made:
                continue
            # making sure thumbnails are not remade

            full_path_to_single_compilation_folder = path_compliation_images+folder
            list_of_images_for_single_folder = os.listdir(full_path_to_single_compilation_folder)

            images = []
            for image in list_of_images_for_single_folder:
                full_path_to_single_image_for_single_compilation = full_path_to_single_compilation_folder+'/'+image
                images.append(Image.open(full_path_to_single_image_for_single_compilation))

            '''each image needs to be 
            1280/3 = x
            720 = y
            '''

            total_width = 1280
            total_height = 720
            new_image = Image.new('RGB', (total_width, total_height))
            x_offset = 0

            sub_x = int(total_width/3)
            sub_y = 720
            for image in images:

                x_image,y_image = image.size
                center_x = x_image/2.0
                center_y = y_image/2.0
                left = int(center_x - sub_x/2.0)
                top = int(center_y - sub_y/2.0)
                right = int(center_x + sub_x/2.0)
                bottom = int(center_y + sub_y/2.0)

                im1 = image.crop((left, top, right, bottom))
                newsize = (sub_x, sub_y)
                im1 = im1.resize(newsize)
                # useful to maintaining the aspect ratio
                # image.thumbnail((sub_x, sub_y), Image.ANTIALIAS)
                new_image.paste(im1, (x_offset,0))
                x_offset += sub_x

            tiktok_logo = Image.open('./tiktok_logo/tiktok-logo-white.png')
            tiktok_logo = tiktok_logo.rotate(-45,expand=True)
            tiktok_logo.thumbnail((300, 300), Image.ANTIALIAS)
            whole_image = Image.new('RGB', (total_width, total_height))
            whole_image.paste(new_image)
            # puts the tiktok sign in the top right
            # whole_image.paste(tiktok_logo, (400,-70), mask=tiktok_logo)
            total_x_space = total_width-tiktok_logo.size[0]
            total_y_space = total_height-tiktok_logo.size[1]

            whole_image.paste(tiktok_logo, ( random.randint(0, total_x_space), random.randint(-70, total_y_space) ), mask=tiktok_logo)
            # whole_image.show()
            whole_image.save(f'./final_thumbnails/{folder}.png')

            print('thumbnail complete')

# testing
if __name__ == '__main__':
    bt = BuildThumbnail()
    target_string = "As It Was"
    bt.run(target_string)