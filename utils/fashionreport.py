import asyncio
import re

FASHION_REPORT_TWEETER_NAME = "KaiyokoStar"


def _get_latest(api):
    timeline = api.GetUserTimeline(screen_name=FASHION_REPORT_TWEETER_NAME, count=50,
                                   include_rts=False, exclude_replies=True)
    latest = next(t for t in timeline if re.match(r"Fashion Report Week \d+ - Full Details", t.text))
    return latest


async def get_latest(bot):
    return await asyncio.get_running_loop().run_in_executor(None, _get_latest, bot.twitter)
