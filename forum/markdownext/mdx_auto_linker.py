import markdown
import re, socket, logging
from forum.models import Question
from forum import settings

TLDS = ('gw', 'gu', 'gt', 'gs', 'gr', 'gq', 'gp', 'gy', 'gg', 'gf', 'ge', 'gd', 'ga', 'edu', 'va', 'gn', 'gl', 'gi',
        'gh', 'iq', 'lb', 'lc', 'la', 'tv', 'tw', 'tt', 'arpa', 'lk', 'li', 'lv', 'to', 'lt', 'lr', 'ls', 'th', 'tf',
        'su', 'td', 'aspx', 'tc', 'ly', 'do', 'coop', 'dj', 'dk', 'de', 'vc', 'me', 'dz', 'uy', 'yu', 'vg', 'ro',
        'vu', 'qa', 'ml', 'us', 'zm', 'cfm', 'tel', 'ee', 'htm', 'za', 'ec', 'bg', 'uk', 'eu', 'et', 'zw',
        'es', 'er', 'ru', 'rw', 'rs', 'asia', 're', 'it', 'net', 'gov', 'tz', 'bd', 'be', 'bf', 'asp', 'jobs', 'ba',
        'bb', 'bm', 'bn', 'bo', 'bh', 'bi', 'bj', 'bt', 'jm', 'sb', 'bw', 'ws', 'br', 'bs', 'je', 'tg', 'by', 'bz',
        'tn', 'om', 'ua', 'jo', 'pdf', 'mz', 'com', 'ck', 'ci', 'ch', 'co', 'cn', 'cm', 'cl', 'cc', 'tr', 'ca', 'cg',
        'cf', 'cd', 'cz', 'cy', 'cx', 'org', 'cr', 'txt', 'cv', 'cu', 've', 'pr', 'ps', 'fk', 'pw', 'pt', 'museum',
        'py', 'tl', 'int', 'pa', 'pf', 'pg', 'pe', 'pk', 'ph', 'pn', 'eg', 'pl', 'tk', 'hr', 'aero', 'ht', 'hu', 'hk',
        'hn', 'vn', 'hm', 'jp', 'info', 'md', 'mg', 'ma', 'mc', 'uz', 'mm', 'local', 'mo', 'mn', 'mh', 'mk', 'cat',
        'mu', 'mt', 'mw', 'mv', 'mq', 'ms', 'mr', 'im', 'ug', 'my', 'mx', 'il', 'pro', 'ac', 'sa', 'ae', 'ad', 'ag',
        'af', 'ai', 'vi', 'is', 'ir', 'am', 'al', 'ao', 'an', 'aq', 'as', 'ar', 'au', 'at', 'aw', 'in', 'ax', 'az',
        'ie', 'id', 'sr', 'nl', 'mil', 'no', 'na', 'travel', 'nc', 'ne', 'nf', 'ng', 'nz', 'dm', 'np',
        'so', 'nr', 'nu', 'fr', 'io', 'ni', 'ye', 'sv', 'kz', 'fi', 'fj', 'fm', 'fo', 'tj', 'sz', 'sy',
        'mobi', 'kg', 'ke', 'doc', 'ki', 'kh', 'kn', 'km', 'st', 'sk', 'kr', 'si', 'kp', 'kw', 'sn', 'sm', 'sl', 'sc',
        'biz', 'ky', 'sg', 'se', 'sd')

# This approach comes directly from PageDown's Markdown.Converter.js to ensure that the server behaviour is identical to the editor preview
# Any improvement to either should be made in both locations. The two exceptions are allowing for > as a starting character for a URL, by
# the time we're processing these links, there's HTML markup present and question link parsing.
URL_RE = re.compile("(^|\s|>)(https?|ftp)(:\/\/[-A-Z0-9+&@#\/%?=~_|\[\]\(\)!:,\.;]*[-A-Z0-9+&@#\/%=~_|\[\]])($|\W)", re.I);
QUESTION_LINK_RE = re.compile("(https?)(:\/\/" + settings.APP_DOMAIN + "\/questions\/)([0-9]+)", re.I);
AUTO_LINK_RE = re.compile("<((https?|ftp):[^'\">\s]+)>");

EMAIL_LINK_REPLACE_RE = re.compile("(?<= href=\")[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})(?=\")")

def replacer(m):
    url = m.group(1)
    mq = QUESTION_LINK_RE.match(url)
    if mq != None:
        id = mq.group(3)
        question = None
        try:
          question = Question.objects.get(id=id)
        except DoesNotExist:
	  logging.error("DoesNotExist exception for question id %s while autolinking" % id)
        if ( question != None ):
          title = question.title
        else:
          title = url
    else:
        title = url
    return '<a href="%s">%s</a>' % (url, title)

class AutoLinker(markdown.postprocessors.Postprocessor):

    def run(self, text):
        logging.error("Autolinker called with " + text)

        # Surround any raw links that are valid for auto-linking with <>'s
        text = URL_RE.sub(r"\1<\2\3>\4", text)

        # Substitute an anchor with a replacement title if appropriate
        text = AUTO_LINK_RE.sub(replacer, text)

	# Email substitution
        text = EMAIL_LINK_REPLACE_RE.sub(lambda m: "mailto:%s" % m.group(0), text)

        return text

class AutoLinkerExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.postprocessors['autolinker'] = AutoLinker()

def makeExtension(configs=None):
    return AutoLinkerExtension(configs=configs)


