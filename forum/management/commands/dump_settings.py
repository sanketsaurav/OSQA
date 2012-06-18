from pprint import pformat
from django.core.management.base import NoArgsCommand
from forum import settings
from forum.settings import BaseSetting

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        last_value_default = None
        for k in dir(settings):
            attr = getattr(settings, k)
            if not isinstance(attr, BaseSetting):
                continue
            if attr.value == attr.default:
                if not(last_value_default is None) and last_value_default == False:
                    print
                last_value_default = True
                print "# %s has default value" % k
                continue

            print
            last_value_default = False
            if attr.field_context:
                if attr.field_context.get('label', None):
                    print "'''%s'''" % unicode(attr.field_context.get('label'))
                if attr.field_context.get('help_text', None):
                    print "'''%s'''" % unicode(attr.field_context.get('help_text'))
            print "settings.%s = %s" % (k, pformat(attr.value))
