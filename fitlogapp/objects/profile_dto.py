from ..models import CustomUser, Profile
from dataclasses import dataclass


@dataclass
class ProfileDto:
    """プロフィール情報を画面表示するための情報"""

    username: str = None
    user_id: str = None
    image_url: str = None
    bio: str = None
    followers_count: int = None
    following_count: int = None

    def __init__(self, user: CustomUser):
        """ユーザー情報を元に、画面表示のプロフィール情報を生成"""
        profile = Profile.objects.get(user=user)
        self.user_id = user.pk
        self.username = user.custom_username
        if profile.profile_image:
            self.image_url = profile.profile_image.url
        self.bio = profile.bio
        self.following_count = user.following.count()
        self.followers_count = user.followers.count()

    def to_dict(self):
        """インスタンスを辞書型に変換"""
        return self.__dict__
