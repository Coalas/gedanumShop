from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.template import TemplateDoesNotExist
from django.views.generic.simple import direct_to_template

def example(request):
    ctx = RequestContext(request, {})
    return render_to_response('localsite/example.html', context_instance=ctx)

def static_page(request, page):
    ctx = RequestContext(request, {})
    return render_to_response("%s.html" % page, context_instance=ctx)
    
     
    


#return direct_to_template(request, template="localsite/%s.html" % page)