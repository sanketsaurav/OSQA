import logging

from django.template import RequestContext
from django.shortcuts import render_to_response


# Replacement for django shortcuts.render_to_response including handling of endless pagination and PJAX
def render_response(template, context=None, request=None, parent_template=None, pjax_parent=None, page_template=None):
    context['parent_template'] = _resolve_parent(request, parent_template, pjax_parent)
    render_template = _resolve_template(context, request, template, page_template)

    return render_to_response(render_template, context, context_instance=RequestContext(request))

def _resolve_parent(request, parent_template, pjax_parent):
    resolved_parent = None

    # Allow parent templates to be configured in the context
    if parent_template is None:
        resolved_parent = 'base_content.html'
    else:
        resolved_parent = parent_template

    # PJAX. Provide pjaxtend style template extension. Assume pjax.html is parent template for PJAX requests unless a parent is specified
    isPJAX = request.META.get('HTTP_X_PJAX', False)
    if isPJAX:
        if pjax_parent is not None:
            resolved_parent = pjax_parent
        else:
            # TODO implement proper fallback
            if parent_template == 'base.html':
                resolved_parent = 'base_pjax.html'
            else:
                resolved_parent = 'base_content_pjax.html'

    return resolved_parent


def _resolve_template(context, request, template, page_template):
    # Endless pagination. If a pagination template is configured add it to the context here and check if it should be rendered directly
    resolved_template = context.pop('template', template)
    if page_template is not None:
        context['page_template'] = page_template

    isPJAX = request.META.get('HTTP_X_PJAX', False)
    if request.is_ajax() and not isPJAX:
        resolved_template = page_template

    return resolved_template

