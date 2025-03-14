import subprocess
import json
import os
import shutil
from wisty import download_video

DATA = "data/data.json"
extract_json_path = f"extract.json"
with open(DATA, "r") as f:
    data = json.load(f)

if not data.get("videos"):
    raise ValueError("No video data provided")


def download_video_with_wisty(video_info):
    video_id = video_info["wistia_id"]
    video_name = video_info["name"]
    print(f"Downloading video: {video_name} ({video_id}) to the current directory.")

    try:
        subprocess.run(
            ["wisty", "-i", video_id, "-n", video_name],
            capture_output=True, text=True, check=True
        )
        print(f"Download completed for {video_name}")
        downloaded_file = f"{video_name}.mp4"
        if not os.path.exists(downloaded_file):
            download_fallback(video_name)

        if os.path.exists(extract_json_path):
            os.remove(extract_json_path)
    except Exception as e:
       print(e)


def download_fallback(video_name):
    if os.path.exists(extract_json_path):
        with open(extract_json_path, 'r') as f:
            extract_data = json.load(f)
            video_url = extract_data[0].get("url")
            if video_url:
                print(f"Extracted URL from extract.json: {video_url}")
                video_filename = f"{video_name}.mp4"
                print(f"Downloading video using fallback: {video_filename}")
                download_video(video_url, video_filename)
                os.remove(extract_json_path)
            else:
                print(f"Download URL not found in extract.json for {video_name}")
    else:
        print(f"extract.json not found for {video_name}, falling back to default URL.")



def move_downloaded_videos(videos):
    for video_info in videos:
        video_name = video_info["name"]
        folder_name = video_info["folder_name"]
        downloaded_file = f"{video_name}.mp4"

        print(f"Looking for downloaded file: {downloaded_file}")

        if os.path.exists(downloaded_file):
            print(f"Moving {downloaded_file} to folder: {folder_name}")
            os.makedirs(folder_name, exist_ok=True)
            shutil.move(downloaded_file, os.path.join(folder_name, downloaded_file))
        else:
            print(f"Downloaded file {downloaded_file} not found.")
            download_fallback(video_info)



if __name__ == "__main__":
    for video in data["videos"]:
        if os.path.exists(extract_json_path):
            os.remove(extract_json_path)
        print(f"Processing video: {video['name']}")
        download_video_with_wisty(video)
        move_downloaded_videos([video])
