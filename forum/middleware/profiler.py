# Simple profiling middleware that replaces the response with cProfile output
# http://djangosnippets.org/snippets/727/
import sys
from cStringIO import StringIO
from django.conf import settings

try:
    import cProfile
    ENABLE_PROFILER = True
except ImportError:
    ENABLE_PROFILER = False

class ProfilerMiddleware(object):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if ENABLE_PROFILER and settings.DEBUG and 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if ENABLE_PROFILER and settings.DEBUG and 'prof' in request.GET:
            p = self.profiler
            p.create_stats()
            out = StringIO()
            old_stdout, sys.stdout = sys.stdout, out

            p.print_stats('cumulative')
            p.print_stats('time')
            p.print_stats('name')

            sys.stdout = old_stdout
            response.content = '<pre>%s</pre>' % out.getvalue()
        return response

