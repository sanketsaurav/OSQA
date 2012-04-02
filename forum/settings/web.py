import os.path

from base import Setting, SettingSet
from forms import ImageFormWidget

from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import Textarea

WEB_SET = SettingSet('web', _('Web settings'), _("Web settings for the application"))

CDN_ON = Setting('CDN_ON', True, WEB_SET, dict(
label = _("Use content distribution network"),
help_text = _("Check if you want to use the Google Libraries API and CDN locations to load JavaScript libraries. Google hosted CSS files are not minified and jQuery resources take one extra request, however this is offset by location and serving key resource files from a different hostname."),
required=False))

CSS_SPRITES = Setting('CSS_SPRITES', True, WEB_SET, dict(
label = _("Use CSS sprites"),
help_text = _("Check if you want to use use CSS sprites instead of individual images."),
required=False))

ENDLESS_PAGINATION = Setting('ENDLESS_PAGINATION', True, WEB_SET, dict(
label = _("Use endless pagination"),
help_text = _("Check if you want to use endless, automatically loading pagination instead of legacy paging (experimental)."),
required=False))

USE_PJAX = Setting('USE_PJAX', True, WEB_SET, dict(
label = _("Use PJAX page loading"),
help_text = _("Check if you want to use PJAX for smooth, inline AJAX/history push based page loads (experimental)."),
required=False))

PJAX_TIMEOUT = Setting('PJAX_TIMEOUT', 1500, WEB_SET, dict(
label = _("PJAX request timeout"),
help_text = _("Value in milliseconds used to determine how long PJAX will wait for an RPC request before falling back to a standard request."),
required=False))
