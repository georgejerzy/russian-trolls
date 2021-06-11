import re
import emoji
from langdetect import detect, LangDetectException


class TweetsPreprocessor:
    @classmethod
    def cleaner(cls, tweet: str):
        """
        Removes tweet text artifacts: the "RT", @references, #hashtags, and links
        Args:
            tweet: tweet text

        Returns:
            claned tweet text
        """
        tweet = re.sub("RT.@[A-Za-z0-9:?]+", "", str(tweet))  # Remove TR @
        tweet = re.sub(
            r"(?:\@|http?\://|https?\://|www)\S+", "", tweet
        )  # Remove http links
        tweet = " ".join(tweet.split())
        tweet = "".join(
            c for c in tweet if c not in emoji.UNICODE_EMOJI
        )  # Remove Emojis
        tweet = tweet.replace("#", "").replace(
            "_", " "
        )  # Remove hashtag sign but keep the text
        return tweet

    @classmethod
    def detect_language_or_null(cls, x: str) -> (str or None):
        """
        Recognize language of the string or returns null.
        Wrapper on: https://pypi.org/project/langdetect/
        Args:
            x: string to recognize

        Returns:
            ISO 639-1 code of the language
        """
        if x and type(x) == str:
            try:
                return detect(x)
            except LangDetectException:
                return None
            except TypeError:
                print(x)
                print(type(x))
        else:
            return None
