# Webshare Proxy Instructions

## Python API

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

Note that [referral links are used here](https://www.webshare.io/?referral_code=w0xno53eb50g) and any purchases made through these links will support this Open Source project (at no additional cost of course!), which is very much appreciated!

However, you are of course free to integrate your own proxy solution using the `GenericProxyConfig` class, if you prefer using another provider or want to implement your own solution, as covered by the following section.

## CLI

### Working around IP bans using the CLI

If you are running into `ReqestBlocked` or `IpBlocked` errors, because YouTube blocks your IP, you can work around this using residential proxies as explained in [Working around IP bans](https://pypi.org/project/youtube-transcript-api/#working-around-ip-bans-requestblocked-or-ipblocked-exception). To use [Webshare "Residential" proxies](https://www.webshare.io/?referral_code=w0xno53eb50g) through the CLI, you will have to create a [Webshare account](https://www.webshare.io/?referral_code=w0xno53eb50g) and purchase a "Residential" proxy package that suits your workload (make sure NOT to purchase "Proxy Server" or "Static Residential"!). Then you can use the "Proxy Username" and "Proxy Password" which you can find in your [Webshare Proxy Settings](https://dashboard.webshare.io/proxy/settings?referral_code=w0xno53eb50g), to run the following command:

```
youtube_transcript_api <first_video_id> <second_video_id> --webshare-proxy-username "username" --webshare-proxy-password "password"
```
