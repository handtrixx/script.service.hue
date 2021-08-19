import platform
import sys

import rollbar
import xbmcgui

from resources.lib.language import get_string as _
from . import ADDONVERSION, ROLLBAR_API_KEY, ADDONID, KODIVERSION, ADDONPATH


def _error_report_requested(exc):
    return xbmcgui.Dialog().yesno(heading="{} {}".format(ADDONID, _("Error")), message=_("The following error occurred:") + "\n[COLOR=red]{}[/COLOR]\n".format(exc) + _("Automatically report this error?"))


def _report_error(level):
    if "dev" in ADDONVERSION:
        env = "dev"
    else:
        env = "production"

    data = {
        'machine': platform.machine(),
        'platform': platform.system(),
        'kodi': KODIVERSION,
    }
    rollbar.init(ROLLBAR_API_KEY, capture_ip=False, code_version=ADDONVERSION, root=ADDONPATH, scrub_fields='bridgeUser', environment=env)
    rollbar.report_exc_info(sys.exc_info(), extra_data=data, level=level)


def process_exception(exc, level="critical"):
    if _error_report_requested(exc):
        _report_error(level)
