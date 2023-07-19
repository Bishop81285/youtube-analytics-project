from src.channel import Channel


class Video(Channel):
    def __init__(self, video_id):
        self.__video_id: str = video_id
        self.__video_info: dict = self._fetch_video_info()
        self.__video_title: str = self.__video_info['items'][0]['snippet']['title']
        self.__view_count: int = self.__video_info['items'][0]['statistics']['viewCount']
        self.__like_count: int = self.__video_info['items'][0]['statistics']['likeCount']
        self.__comment_count: int = self.__video_info['items'][0]['statistics']['commentCount']

    def __str__(self):
        return self.__video_title

    def _fetch_video_info(self) -> dict:
        return super().youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                             id=self.__video_id
                                             ).execute()

    @property
    def url(self):
        return f'https://youtu.be/{self.__video_id}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__playlist_id: str = playlist_id
        self.__playlist_info: dict = self._fetch_playlist_info()

        video_ids = [video['contentDetails']['videoId'] for video in self.__playlist_info['items']]

        if video_id not in video_ids:
            raise ValueError('The video you selected is not in this playlist. Please provide the correct id.')

    def _fetch_playlist_info(self) -> dict:
        return super(Video, self).youtube.playlistItems().list(playlistId=self.__playlist_id,
                                                               part='contentDetails',
                                                               maxResults=50,
                                                               ).execute()
