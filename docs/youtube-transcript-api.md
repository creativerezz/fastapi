Title: youtube-transcript-api

URL Source: https://pypi.org/project/youtube-transcript-api/

Markdown Content:
[![Image 1: Donate](https://pypi-camo.freetls.fastly.net/1c6b48d4ac9b582dbc400aa2bd53b809f2f2b394/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d50617950616c2d677265656e2e737667)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=BAENLEW8VUJ6G&source=url)[![Image 2: Build Status](https://pypi-camo.freetls.fastly.net/b39ecb4c7beecb89858b6f8a8780d44626389923/68747470733a2f2f6769746875622e636f6d2f6a6465706f69782f796f75747562652d7472616e7363726970742d6170692f616374696f6e732f776f726b666c6f77732f63692e796d6c2f62616467652e7376673f6272616e63683d6d6173746572)](https://github.com/jdepoix/youtube-transcript-api/actions)[![Image 3: Coverage Status](https://pypi-camo.freetls.fastly.net/a7bf0a1d15416697f0d95df8d6d5c1aee2afb421/68747470733a2f2f636f766572616c6c732e696f2f7265706f732f6769746875622f6a6465706f69782f796f75747562652d7472616e7363726970742d6170692f62616467652e7376673f6272616e63683d6d6173746572)](https://coveralls.io/github/jdepoix/youtube-transcript-api?branch=master)[![Image 4: MIT license](https://pypi-camo.freetls.fastly.net/5bce10e8e48e6c0a122e9f07c0b94cad805796fb/687474703a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d627269676874677265656e2e7376673f7374796c653d666c6174)](http://opensource.org/licenses/MIT)[![Image 5: Current Version](https://pypi-camo.freetls.fastly.net/e7af95451a576f7e85a13cf0abef769b89b1eef7/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f796f75747562652d7472616e7363726970742d6170692e737667)](https://pypi.org/project/youtube-transcript-api/)[![Image 6: Supported Python Versions](https://pypi-camo.freetls.fastly.net/23dd0e8810d6afa579aa9bbff1759ab79c6ef75c/68747470733a2f2f696d672e736869656c64732e696f2f707970692f707976657273696f6e732f796f75747562652d7472616e7363726970742d6170692e737667)](https://pypi.org/project/youtube-transcript-api/)

**This is a python API which allows you to retrieve the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles, supports translating subtitles and it does not require a headless browser, like other selenium based solutions do!**

Maintenance of this project is made possible by all the [contributors](https://github.com/jdepoix/youtube-transcript-api/graphs/contributors) and [sponsors](https://github.com/sponsors/jdepoix). If you'd like to sponsor this project and have your avatar or company logo appear below [click here](https://github.com/sponsors/jdepoix). 💖

[![Image 7: SearchAPI](https://pypi-camo.freetls.fastly.net/20e742ddb54c2bf046dedd2a88d33ea2851b08ad/68747470733a2f2f7777772e7365617263686170692e696f2f70726573732f76312f7376672f7365617263686170695f6c6f676f5f626c61636b5f682e737667)](https://www.searchapi.io/)[![Image 8: supadata](https://pypi-camo.freetls.fastly.net/ccf20ea172ba1860b2889e968b6794dbdb7fc0a9/68747470733a2f2f73757061646174612e61692f6c6f676f2d6c696768742e737667)](https://supadata.ai/)[![Image 9: Dumpling AI](https://pypi-camo.freetls.fastly.net/b2c6961172f71a99c54d80b8e6be5ccf5839134e/68747470733a2f2f7777772e64756d706c696e6761692e636f6d2f6c6f676f732f6c6f676f2d6c696768742e737667)](https://www.dumplingai.com/)

Install
-------

It is recommended to [install this module by using pip](https://pypi.org/project/youtube-transcript-api/):

```
pip install youtube-transcript-api
```

You can either integrate this module [into an existing application](https://pypi.org/project/youtube-transcript-api/#api) or just use it via a [CLI](https://pypi.org/project/youtube-transcript-api/#cli).

API
---

The easiest way to get a transcript for a given video is to execute:

from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
ytt_api.fetch(video_id)

> **Note:** By default, this will try to access the English transcript of the video. If your video has a different language, or you are interested in fetching a transcript in a different language, please read the section below.

> **Note:** Pass in the video ID, NOT the video URL. For a video with the URL `https://www.youtube.com/watch?v=12345` the ID is `12345`.

This will return a `FetchedTranscript` object looking somewhat like this:

FetchedTranscript(
    snippets=[
        FetchedTranscriptSnippet(
            text="Hey there",
            start=0.0,
            duration=1.54,
        ),
        FetchedTranscriptSnippet(
            text="how are you",
            start=1.54,
            duration=4.16,
        ),
        # ...
    ],
    video_id="12345",
    language="English",
    language_code="en",
    is_generated=False,
)

This object implements most interfaces of a `List`:

ytt_api = YouTubeTranscriptApi()
fetched_transcript = ytt_api.fetch(video_id)

# is iterable
for snippet in fetched_transcript:
    print(snippet.text)

# indexable
last_snippet = fetched_transcript[-1]

# provides a length
snippet_count = len(fetched_transcript)

If you prefer to handle the raw transcript data you can call `fetched_transcript.to_raw_data()`, which will return a list of dictionaries:

[
    {
        'text': 'Hey there',
        'start': 0.0,
        'duration': 1.54
    },
    {
        'text': 'how are you',
        'start': 1.54
        'duration': 4.16
    },
    # ...
]

### Retrieve different languages

You can add the `languages` param if you want to make sure the transcripts are retrieved in your desired language (it defaults to english).

YouTubeTranscriptApi().fetch(video_id, languages=['de', 'en'])

It's a list of language codes in a descending priority. In this example it will first try to fetch the german transcript (`'de'`) and then fetch the english transcript (`'en'`) if it fails to do so. If you want to find out which languages are available first, [have a look at `list()`](https://pypi.org/project/youtube-transcript-api/#list-available-transcripts).

If you only want one language, you still need to format the `languages` argument as a list

YouTubeTranscriptApi().fetch(video_id, languages=['de'])

### Preserve formatting

You can also add `preserve_formatting=True` if you'd like to keep HTML formatting elements such as `<i>` (italics) and `<b>` (bold).

YouTubeTranscriptApi().fetch(video_ids, languages=['de', 'en'], preserve_formatting=True)

### List available transcripts

If you want to list all transcripts which are available for a given video you can call:

ytt_api = YouTubeTranscriptApi()
transcript_list = ytt_api.list(video_id)

This will return a `TranscriptList` object which is iterable and provides methods to filter the list of transcripts for specific languages and types, like:

transcript = transcript_list.find_transcript(['de', 'en'])

By default this module always chooses manually created transcripts over automatically created ones, if a transcript in the requested language is available both manually created and generated. The `TranscriptList` allows you to bypass this default behaviour by searching for specific transcript types:

# filter for manually created transcripts
transcript = transcript_list.find_manually_created_transcript(['de', 'en'])

# or automatically generated ones
transcript = transcript_list.find_generated_transcript(['de', 'en'])

The methods `find_generated_transcript`, `find_manually_created_transcript`, `find_transcript` return `Transcript` objects. They contain metadata regarding the transcript:

print(
    transcript.video_id,
    transcript.language,
    transcript.language_code,
    # whether it has been manually created or generated by YouTube
    transcript.is_generated,
    # whether this transcript can be translated or not
    transcript.is_translatable,
    # a list of languages the transcript can be translated to
    transcript.translation_languages,
)

and provide the method, which allows you to fetch the actual transcript data:

transcript.fetch()

This returns a `FetchedTranscript` object, just like `YouTubeTranscriptApi().fetch()` does.

### Translate transcript

YouTube has a feature which allows you to automatically translate subtitles. This module also makes it possible to access this feature. To do so `Transcript` objects provide a `translate()` method, which returns a new translated `Transcript` object:

transcript = transcript_list.find_transcript(['en'])
translated_transcript = transcript.translate('de')
print(translated_transcript.fetch())

### By example

from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()

# retrieve the available transcripts
transcript_list = ytt_api.list('video_id')

# iterate over all available transcripts
for transcript in transcript_list:

    # the Transcript object provides metadata properties
    print(
        transcript.video_id,
        transcript.language,
        transcript.language_code,
        # whether it has been manually created or generated by YouTube
        transcript.is_generated,
        # whether this transcript can be translated or not
        transcript.is_translatable,
        # a list of languages the transcript can be translated to
        transcript.translation_languages,
    )

    # fetch the actual transcript data
    print(transcript.fetch())

    # translating the transcript will return another transcript object
    print(transcript.translate('en').fetch())

# you can also directly filter for the language you are looking for, using the transcript list
transcript = transcript_list.find_transcript(['de', 'en'])  

# or just filter for manually created transcripts 
transcript = transcript_list.find_manually_created_transcript(['de', 'en'])  

# or automatically generated ones 
transcript = transcript_list.find_generated_transcript(['de', 'en'])

Working around IP bans (`RequestBlocked` or `IpBlocked` exception)
------------------------------------------------------------------

Unfortunately, YouTube has started blocking most IPs that are known to belong to cloud providers (like AWS, Google Cloud Platform, Azure, etc.), which means you will most likely run into `RequestBlocked` or `IpBlocked` exceptions when deploying your code to any cloud solutions. Same can happen to the IP of your self-hosted solution, if you are doing too many requests. You can work around these IP bans using proxies. However, since YouTube will ban static proxies after extended use, going for rotating residential proxies provide is the most reliable option.

There are different providers that offer rotating residential proxies, but after testing different offerings I have found [Webshare](https://www.webshare.io/?referral_code=w0xno53eb50g) to be the most reliable and have therefore integrated it into this module, to make setting it up as easy as possible.

### Using [Webshare](https://www.webshare.io/?referral_code=w0xno53eb50g)

Once you have created a [Webshare account](https://www.webshare.io/?referral_code=w0xno53eb50g) and purchased a "Residential" proxy package that suits your workload (make sure NOT to purchase "Proxy Server" or "Static Residential"!), open the [Webshare Proxy Settings](https://dashboard.webshare.io/proxy/settings?referral_code=w0xno53eb50g) to retrieve your "Proxy Username" and "Proxy Password". Using this information you can initialize the `YouTubeTranscriptApi` as follows:

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username="<proxy-username>",
        proxy_password="<proxy-password>",
    )
)

# all requests done by ytt_api will now be proxied through Webshare
ytt_api.fetch(video_id)

Using the `WebshareProxyConfig` will default to using rotating residential proxies and requires no further configuration.

You can also limit the pool of IPs that you will be rotating through to those located in specific countries. By choosing locations that are close to the machine that is running your code, you can reduce latency. Also, this can be used to work around location-based restrictions.

ytt_api = YouTubeTranscriptApi(
    proxy_config=WebshareProxyConfig(
        proxy_username="<proxy-username>",
        proxy_password="<proxy-password>",
        filter_ip_locations=["de", "us"],
    )
)

# Webshare will now only rotate through IPs located in Germany or the United States!
ytt_api.fetch(video_id)

You can find the full list of available locations (and how many IPs are available in each location) [here](https://www.webshare.io/features/proxy-locations?referral_code=w0xno53eb50g).

Note that [referral links are used here](https://www.webshare.io/?referral_code=w0xno53eb50g) and any purchases made through these links will support this Open Source project (at no additional cost of course!), which is very much appreciated! 💖😊🙏💖

However, you are of course free to integrate your own proxy solution using the `GenericProxyConfig` class, if you prefer using another provider or want to implement your own solution, as covered by the following section.

### Using other Proxy solutions

Alternatively to using [Webshare](https://pypi.org/project/youtube-transcript-api/#using-webshare), you can set up any generic HTTP/HTTPS/SOCKS proxy using the `GenericProxyConfig` class:

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig

ytt_api = YouTubeTranscriptApi(
    proxy_config=GenericProxyConfig(
        http_url="http://user:pass@my-custom-proxy.org:port",
        https_url="https://user:pass@my-custom-proxy.org:port",
    )
)

# all requests done by ytt_api will now be proxied using the defined proxy URLs
ytt_api.fetch(video_id)

Be aware that using a proxy doesn't guarantee that you won't be blocked, as YouTube can always block the IP of your proxy! Therefore, you should always choose a solution that rotates through a pool of proxy addresses, if you want to maximize reliability.

Overwriting request defaults
----------------------------

When initializing a `YouTubeTranscriptApi` object, it will create a `requests.Session` which will be used for all HTTP(S) request. This allows for caching cookies when retrieving multiple requests. However, you can optionally pass a `requests.Session` object into its constructor, if you manually want to share cookies between different instances of `YouTubeTranscriptApi`, overwrite defaults, set custom headers, specify SSL certificates, etc.

from requests import Session

http_client = Session()

# set custom header
http_client.headers.update({"Accept-Encoding": "gzip, deflate"})

# set path to CA_BUNDLE file
http_client.verify = "/path/to/certfile"

ytt_api = YouTubeTranscriptApi(http_client=http_client)
ytt_api.fetch(video_id)

# share same Session between two instances of YouTubeTranscriptApi
ytt_api_2 = YouTubeTranscriptApi(http_client=http_client)
# now shares cookies with ytt_api
ytt_api_2.fetch(video_id)

Cookie Authentication
---------------------

Some videos are age restricted, so this module won't be able to access those videos without some sort of authentication. Unfortunately, some recent changes to the YouTube API have broken the current implementation of cookie based authentication, so this feature is currently not available.

Using Formatters
----------------

Formatters are meant to be an additional layer of processing of the transcript you pass it. The goal is to convert a `FetchedTranscript` object into a consistent string of a given "format". Such as a basic text (`.txt`) or even formats that have a defined specification such as JSON (`.json`), WebVTT (`.vtt`), SRT (`.srt`), Comma-separated format (`.csv`), etc...

The `formatters` submodule provides a few basic formatters, which can be used as is, or extended to your needs:

*   JSONFormatter
*   PrettyPrintFormatter
*   TextFormatter
*   WebVTTFormatter
*   SRTFormatter

Here is how to import from the `formatters` module.

# the base class to inherit from when creating your own formatter.
from youtube_transcript_api.formatters import Formatter

# some provided subclasses, each outputs a different string format.
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api.formatters import WebVTTFormatter
from youtube_transcript_api.formatters import SRTFormatter

### Formatter Example

Let's say we wanted to retrieve a transcript and store it to a JSON file. That would look something like this:

# your_custom_script.py

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

ytt_api = YouTubeTranscriptApi()
transcript = ytt_api.fetch(video_id)

formatter = JSONFormatter()

# .format_transcript(transcript) turns the transcript into a JSON string.
json_formatted = formatter.format_transcript(transcript)

# Now we can write it out to a file.
with open('your_filename.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_formatted)

# Now should have a new JSON file that you can easily read back into Python.

**Passing extra keyword arguments**

Since JSONFormatter leverages `json.dumps()` you can also forward keyword arguments into `.format_transcript(transcript)` such as making your file output prettier by forwarding the `indent=2` keyword argument.

json_formatted = JSONFormatter().format_transcript(transcript, indent=2)

### Custom Formatter Example

You can implement your own formatter class. Just inherit from the `Formatter` base class and ensure you implement the `format_transcript(self, transcript: FetchedTranscript, **kwargs) -> str` and `format_transcripts(self, transcripts: List[FetchedTranscript], **kwargs) -> str` methods which should ultimately return a string when called on your formatter instance.

class MyCustomFormatter(Formatter):
    def format_transcript(self, transcript: FetchedTranscript, **kwargs) -> str:
        # Do your custom work in here, but return a string.
        return 'your processed output data as a string.'

    def format_transcripts(self, transcripts: List[FetchedTranscript], **kwargs) -> str:
        # Do your custom work in here to format a list of transcripts, but return a string.
        return 'your processed output data as a string.'

CLI
---

Execute the CLI script using the video ids as parameters and the results will be printed out to the command line:

```
youtube_transcript_api <first_video_id> <second_video_id> ...
```

The CLI also gives you the option to provide a list of preferred languages:

```
youtube_transcript_api <first_video_id> <second_video_id> ... --languages de en
```

You can also specify if you want to exclude automatically generated or manually created subtitles:

```
youtube_transcript_api <first_video_id> <second_video_id> ... --languages de en --exclude-generated
youtube_transcript_api <first_video_id> <second_video_id> ... --languages de en --exclude-manually-created
```

If you would prefer to write it into a file or pipe it into another application, you can also output the results as json using the following line:

```
youtube_transcript_api <first_video_id> <second_video_id> ... --languages de en --format json > transcripts.json
```

Translating transcripts using the CLI is also possible:

```
youtube_transcript_api <first_video_id> <second_video_id> ... --languages en --translate de
```

If you are not sure which languages are available for a given video you can call, to list all available transcripts:

```
youtube_transcript_api --list-transcripts <first_video_id>
```

If a video's ID starts with a hyphen you'll have to mask the hyphen using `\` to prevent the CLI from mistaking it for a argument name. For example to get the transcript for the video with the ID `-abc123` run:

```
youtube_transcript_api "\-abc123"
```

### Working around IP bans using the CLI

If you are running into `ReqestBlocked` or `IpBlocked` errors, because YouTube blocks your IP, you can work around this using residential proxies as explained in [Working around IP bans](https://pypi.org/project/youtube-transcript-api/#working-around-ip-bans-requestblocked-or-ipblocked-exception). To use [Webshare "Residential" proxies](https://www.webshare.io/?referral_code=w0xno53eb50g) through the CLI, you will have to create a [Webshare account](https://www.webshare.io/?referral_code=w0xno53eb50g) and purchase a "Residential" proxy package that suits your workload (make sure NOT to purchase "Proxy Server" or "Static Residential"!). Then you can use the "Proxy Username" and "Proxy Password" which you can find in your [Webshare Proxy Settings](https://dashboard.webshare.io/proxy/settings?referral_code=w0xno53eb50g), to run the following command:

```
youtube_transcript_api <first_video_id> <second_video_id> --webshare-proxy-username "username" --webshare-proxy-password "password"
```

If you prefer to use another proxy solution, you can set up a generic HTTP/HTTPS proxy using the following command:

```
youtube_transcript_api <first_video_id> <second_video_id> --http-proxy http://user:pass@domain:port --https-proxy https://user:pass@domain:port
```

### Cookie Authentication using the CLI

To authenticate using cookies through the CLI as explained in [Cookie Authentication](https://pypi.org/project/youtube-transcript-api/#cookie-authentication) run:

```
youtube_transcript_api <first_video_id> <second_video_id> --cookies /path/to/your/cookies.txt
```

Warning
-------

This code uses an undocumented part of the YouTube API, which is called by the YouTube web-client. So there is no guarantee that it won't stop working tomorrow, if they change how things work. I will however do my best to make things working again as soon as possible if that happens. So if it stops working, let me know!

Contributing
------------

To setup the project locally run the following (requires [poetry](https://python-poetry.org/docs/) to be installed):

poetry install --with test,dev

There's [poe](https://github.com/nat-n/poethepoet?tab=readme-ov-file#quick-start) tasks to run tests, coverage, the linter and formatter (you'll need to pass all of those for the build to pass):

poe test
poe coverage
poe format
poe lint

If you just want to make sure that your code passes all the necessary checks to get a green build, you can simply run:

poe precommit

Donations
---------

If this project makes you happy by reducing your development time, you can make me happy by treating me to a cup of coffee, or become a [Sponsor of this project](https://github.com/sponsors/jdepoix) :)

[![Image 10: Donate](https://pypi-camo.freetls.fastly.net/ac49730821d272ac3a4d4e7608ed886a10858e1b/68747470733a2f2f7777772e70617970616c6f626a656374732e636f6d2f656e5f55532f692f62746e2f62746e5f646f6e61746543435f4c472e676966)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=BAENLEW8VUJ6G&source=url)

