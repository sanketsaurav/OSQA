import os.path

from base import Setting, SettingSet
from forms import ImageFormWidget

from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import Textarea

WEB_SET = SettingSet('web', _('Web settings'), _("Web settings for the application"))

CDN_ON = Setting('CDN_ON', False, WEB_SET, dict(
label = _("Use content distribution network"),
help_text = _("Check if you want to use the Google Libraries API and CDN locations to load JavaScript libraries."),
required=False))
