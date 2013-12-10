from django.views.generic.edit import FormView,View
from core.forms import FieldTypeForm,ProfileForm
from django.shortcuts import render
class ProfileView(View):
	def get(self, request):		
		return render(request,'modelform.html',dict(form=ProfileForm()))
	def post(self,request):
		form=ProfileForm(request.POST)
		if form.is_valid():
			return HttpResponse('success')#Redirect(reverse('profile'))
		return render(request,'modelform.html',{'form':form})

class HomeView(FormView):
    template_name = "simpleform.html"
    form_class = FieldTypeForm
    success_url = '/'