from django.core.management.base import NoArgsCommand
from forum import settings as forum_settings
from settings_osqa import SETTINGS

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for k, v in SETTINGS.dict.items():
            try:
                attr = getattr(forum_settings, k)
            except AttributeError:
                print "!!! Attribute %s not found, couldn't set it to %s" % (k, v)
                continue
            if attr.value == v:
                print "# Skipping %s, already has the correct value" % k
                continue
            if attr.value != attr.default:
                print ("!!! Attribute %s has a different value (%s) than its default (%s). " \
                    + "Won't change it to %s") % (k, attr.value, attr.default, v)
                continue
            attr.set_value(v)
            print "Updated %s" % k