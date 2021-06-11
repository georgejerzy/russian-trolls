import re
import emoji
import nltk
from langdetect import detect, LangDetectException


class TweetsPreprocessor:
    def __init__(self):
        nltk.download("words")
        self.words = set(nltk.corpus.words.words())

    def cleaner(self, tweet: str):
        """
        Removes tweet text artifacts: the "RT", @references, #hashtags, and links
        taken from:
        https://stackoverflow.com/questions/64719706/cleaning-twitter-data-pandas-python

        Args:
            tweet: tweet text

        Returns:
            claned tweet text
        """
        tweet = re.sub("@[A-Za-z0-9:?]+", "", str(tweet))  # Remove @ sign #todo: review
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

        # todo: remove that:
        tweet = " ".join(
            w
            for w in nltk.wordpunct_tokenize(tweet)
            if w.lower() in self.words or not w.isalpha()
        )
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
