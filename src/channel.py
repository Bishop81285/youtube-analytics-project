import json
import os

from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    __youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__channel_info = self._fetch_channel_info()
        self.__title = self.__channel_info['items'][0]['snippet']['title']
        self.__description = self.__channel_info['items'][0]['snippet']['description']
        self.__subscriptions = self.__channel_info['items'][0]['statistics']['subscriberCount']
        self.__video_count = self.__channel_info['items'][0]['statistics']['videoCount']
        self.__view_count = self.__channel_info['items'][0]['statistics']['viewCount']

    @property
    def url(self):
        return f'https://www.youtube.com/channel/{self.__channel_id}'

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def subscriptions(self):
        return self.__subscriptions

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__view_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel_info, indent=2, ensure_ascii=False))

    def _fetch_channel_info(self):
        return Channel.__youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    @classmethod
    def get_service(cls):
        """
        Класс-метод, возвращающий объект для работы с YouTube API
        """
        return cls.__youtube

    def to_json(self, filename: str) -> None:
        """
        Метод сохраняющий в файл значения атрибутов экземпляра Channel
        """
        with open(filename, 'w') as file:
            data_dict = self.__dict__
            del data_dict['_Channel__channel_info']
            data_dict['_Channel__url'] = self.url

            json.dump(data_dict, file, ensure_ascii=False)
