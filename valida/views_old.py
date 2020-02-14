from django.shortcuts import render

# Create your views here.


from valida.models import t_face_cnefe
from django.shortcuts import render
'''
def index(request):
    list = t_face_cnefe.objects.all()[:10]
    tmpl = loader.get_template("index.html")
    cont = Context({'t_face_cnefe': list})
    return HttpResponse(tmpl.render(cont))
'''

def index(request):
	list = t_face_cnefe.objects.all()[:15]
	return render(request, 'index.html', {'list': list})