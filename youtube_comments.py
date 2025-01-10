from googleapiclient.discovery import build

def fetch_comments(video_url, api_key):
    # Ekstrak video ID dari URL
    video_id = video_url.split("v=")[-1]
    youtube = build("youtube", "v3", developerKey=api_key)

    comments = []
    try:
        # Ambil komentar dari video
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText"
        )
        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
    except Exception as e:
        print(f"Error: {e}")
    return comments
