from moviepy.editor import *
import os
import random

class CreateCompilation():

    def run(self, target_string):
        search_term = target_string
        # search_term = "Can't You See Me?"
        chars = "\\`*_{}[]()>#+-.!$?�"
        for c in chars:
            search_term = search_term.replace(c,'')

        path = './videos/'
        total_path = path+search_term+'/'
        files = os.listdir(total_path)

        dictionary_of_video_video_length = {}
        for file in files:
            full_path = total_path+file
            try:
                video = VideoFileClip(full_path)
            except Exception as e:
                print(e, ' video failed to load')
                continue
            print('file loaded temporary', file)
            dictionary_of_video_video_length[file] = video.duration

        global_list_of_video_used = []

        for _ in range(4):
            # because time needs to be in seconds
            time_of_total_video = 10 * 60
            current_total_time = 0
            list_of_videos_to_use_index = []

            while(time_of_total_video > current_total_time):
                index_value = random.randint(0, len(files)-1 )
                if index_value in global_list_of_video_used:
                    if len(global_list_of_video_used) > len(dictionary_of_video_video_length)-2:
                        global_list_of_video_used = []
                    continue

                list_of_videos_to_use_index.append(index_value)
                global_list_of_video_used.append(index_value)

                file_name = files[index_value]
                duration = dictionary_of_video_video_length[file_name]
                current_total_time += duration




            list_of_final_videos_to_use = []
            lowest_frame_rate = 1000000000

            for index in list_of_videos_to_use_index:
                file_name = files[index]
                full_path = total_path + file_name
                try:
                    video = VideoFileClip(full_path)
                except Exception as e:
                    print(e, ' video failed to load')
                    continue


                frame_rate_current = video.fps
                if frame_rate_current < lowest_frame_rate:
                    lowest_frame_rate = frame_rate_current
                list_of_final_videos_to_use.append(video)


            result = concatenate_videoclips(list_of_final_videos_to_use, method='compose')
            result.write_videofile(f"./compilation_vids/tiktok_{search_term}_compilation_{_}.mp4", fps=lowest_frame_rate)


            print('stop')


if __name__ == '__main__':
    cc = CreateCompilation()
    target_string = "Dance"
    cc.run(target_string)

