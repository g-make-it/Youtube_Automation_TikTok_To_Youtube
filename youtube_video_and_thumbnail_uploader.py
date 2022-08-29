import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.discovery import HttpError
from googleapiclient.http import MediaFileUpload
import pickle
import http.client
import httplib2
import random
import time

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)
httplib2.RETRIES = 1
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
MAX_RETRIES = 10


# This method implements an exponential backoff strategy to resume a
# failed upload.

def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print("Video id '%s' was successfully uploaded." % response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)

    return response


def authenticate():
    credentials = None

    # checking if pickle file exists
    path_to_pickle = './token.pickle'
    if os.path.exists(path_to_pickle):
        print('loading credentials from file..')
        with open(path_to_pickle, 'rb') as token:
            credentials = pickle.load(token)

    # if not cred then make new ones
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('refreshing access token...')
            credentials.refresh(Request())
        else:
            print('fetching new tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                './client_secret.json',
                scopes=['https://www.googleapis.com/auth/youtube.upload']
            )
            flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')

            credentials = flow.credentials

            with open(path_to_pickle, 'wb') as f:
                print('saving credentials for the future use...')
                pickle.dump(credentials, f)

    return credentials


def uploads_video_initialisation(video_to_upload, details):
    credentials = authenticate()
    # made this way, so you can doublecheck the details of the video
    description = details['desc']
    title = details['title']

    youtube = build('youtube', 'v3', credentials=credentials)
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": description,
                "title": title
            },
            "status": {
                "privacyStatus": "private"
            }
        },

        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload(video_to_upload, chunksize=-1, resumable=True)
    )
    # response = request.execute()
    response = resumable_upload(request)

    return response


def upload_thumbnail(image_path, video_id):
    credentials = authenticate()
    # print(response)

    youtube = build('youtube', 'v3', credentials=credentials)
    request = youtube.thumbnails().set(
        videoId=video_id,

        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload(image_path)
    )

    response = request.execute()

    print(response)


def get_uploaded_videos():
    with open('./details/uploaded_videos.txt', mode='r') as file:
        return set((file.read()).split('\n'))

def save_uploaded_video(file_name):
    with open('./details/uploaded_videos.txt', mode='+a') as file:
        file.write(file_name+'\n')

if __name__ == '__main__':
    set_of_videos_uploaded = get_uploaded_videos()
    path = './compilation_vids/'
    files = os.listdir(path)
    for file in files:
        if file in set_of_videos_uploaded:
            continue
        whole_path = path + file
        name = file.split('.')[0]
        details = {
            'desc': name.replace('_', ' ') + ' best of in 2022',
            'title' : name.replace('_', ' ')
        }
        details_on_video = uploads_video_initialisation(whole_path,details)
        id = details_on_video['id']
        thumbnail_path = f'./final_thumbnails/{name}.png'
        upload_thumbnail(thumbnail_path,video_id=id)
        save_uploaded_video(file_name=file)
        print('one video cycle completed')
