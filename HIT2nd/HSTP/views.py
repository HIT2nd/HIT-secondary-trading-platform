# -*- coding: utf-8 -*-
from django.template import Context
#from django import forms
from django.shortcuts import render_to_response
from models import *
from django import forms
from django.http import HttpResponse
import ImageFile 


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)   
    file = forms.FileField() 
    
class UploadImageForm(forms.Form):
    imagefile = forms.ImageField(required=False)    
    
def register(request):
    flag = -1
    if request.POST:
        post = request.POST
        new_client = Client(
          email = post["email"],
          password = post["password"])
        password2 = post["password2"]
        password = post["password"]
        l = len(Client.objects.filter(email = post["email"]))
          #验证密码是否相同以及Email是否注册过
        if (password == password2) and (l == 0):
            new_client.save()
            flag = 1#可以通过
        elif(password != password2) and (l == 0):
            flag = 2#密码错误
        elif(l != 0):
            flag = 3#邮箱已经被注册
    if flag == 1:
        return render_to_response("login.html")
    else:
        c = Context({"flag":flag})
        return render_to_response("register.html",c)
def login(request):
    errors = {"email":"","password":""}
    if request.POST:
        post = request.POST
        user = Client.objects.filter(email = post["email"])
        if len(user):
            user_real = Client.objects.get(email = post["email"])
            if user_real.password == post["password"]:
                request.session["email"] = user_real.email
                c = Context({"email":user_real.email}) 
                return render_to_response("index2.html", c)
            else:
                errors["password"] = '密码错误,请检查后重新输入！'
        else:
		 errors["email"] = '用户不存在，请点此'
    return render_to_response("login.html",{"errors":errors})
def logout(request):
    del request.session["email"]
    return render_to_response("index.html")
def is_online(fn):
    def check(request,*args):																												
        if "email" in request.session:
            return fn(request,*args)
        else:
            return render_to_response("login.html")
    return check	
    
def return_login(request):
    return render_to_response("login.html")

@is_online
def finish_user(request):
    e = request.GET["email"]
    client = Client.objects.get(email = e)

    if request.POST:
        post = request.POST
        client.studnetID = post["studentID"]
        client.IDcard = post["IDcard"]
        client.telephone = post["telephone"]
        client.realname = post["realname"]
        client.nickname = post["nickname"]
        client.major = post["major"]
        client.grade = post["grade"]
        client.sex = post["sex"]
        client.is_lonly_dog = post["is_lonly_dog"]
        
        form = UploadImageForm(request.POST,request.FILES)
        if form.is_valid():
            client.image = form.cleaned_data["imagefile"]
        
        client.save()
        return render_to_response("index2.html")
        
    return render_to_response("add_inf.html")

#def addPicture(request):  
#    if request.method == 'POST':  
#        form = UploadImageForm(request.POST, request.FILES)  
#        if form.is_valid():  
#            f = request.FILES["imagefile"]  
#            parser = ImageFile.Parser()  
#            for chunk in f.chunks():  
#                parser.feed(chunk)  
#            img = parser.close()  
#            # 在img被保存之前，可以进行图片的各种操作，在各种操作完成后，在进行一次写操作  
#            img.save()

#class UserForm(forms.Form):
#    email = forms.EmailField(required=False,label='email:')
#    password = forms.CharField(required=False,max_length=6,label='password:',widget=forms.PasswordInput())

#def register(request):
#    if request.method == 'POST':
#        uf = UserForm(request.POST)
#        if uf.is_valid():
#            email = uf.cleaned_data['email']
#            password = uf.cleaned_data['password']
#            
#            client = Client()
#            client.email = email
#            client.password = password
#            client.save()
#            return HttpResponseRedirect("/login/")
#    else:
#        uf = UserForm()
#    return render_to_response("html/register.html", {
#        'uf': uf,
#    })