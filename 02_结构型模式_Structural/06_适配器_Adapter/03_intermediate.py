"""
适配器模式 - 中级示例
"""

class Player:
    def play(self):
        pass


class VideoPlayer(Player):
    def play(self):
        return "播放视频"


class AudioPlayer(Player):
    def play(self):
        return "播放音频"


class MediaAdapter:
    def __init__(self, format_type):
        if format_type == "video":
            self.player = VideoPlayer()
        else:
            self.player = AudioPlayer()
    
    def play(self):
        return self.player.play()


if __name__ == "__main__":
    adapter = MediaAdapter("video")
    print(adapter.play())
