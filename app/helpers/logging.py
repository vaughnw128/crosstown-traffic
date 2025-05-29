"""__init__

Just handles some logging stuff, mostly

Made with love and care by Vaughn Woerpel
"""

# built-in
import logging
import sys

# external
import coloredlogs

logger = logging.getLogger("CrosstownTraffic")

format_string = "%(asctime)s - %(levelname)s : [%(module)s] %(message)s"
log_format = logging.Formatter(format_string)

# Sets colored logs formatting
coloredlogs.DEFAULT_LEVEL_STYLES = {
    **coloredlogs.DEFAULT_LEVEL_STYLES,
    "trace": {"color": 246},
    "critical": {"background": "red"},
    "debug": coloredlogs.DEFAULT_LEVEL_STYLES["info"],
}
coloredlogs.DEFAULT_LOG_FORMAT = format_string
coloredlogs.install(level=5, logger=logger, stream=sys.stdout)

# Sets module log levels
logger.setLevel(logging.INFO)
logging.getLogger("discord").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.INFO)
