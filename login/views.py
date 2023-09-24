from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import User,Manager
import hashlib

# Create your views here.

def getmd5(s):
    s += 'orzyadie'
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    usr = request.POST.get('usr', '')
    psw = request.POST.get('psw', '')
    user = ''
    for x in User.objects.all():
        if x.uname == usr:
            user = x
            break
    if user == '':
        messages.error(request, '用户不存在！')
        return redirect('login')
    if user.state == False:
        messages.error(request, '用户注册尚未通过审批！请联系网站管理员。')
        return redirect('login')
    psw = getmd5(psw)
    if user.passwd != psw:
        messages.error(request, '用户名或密码错误！')
        return redirect('login')
    response = HttpResponseRedirect('/')
    response.set_cookie('user', user.unum)
    response.set_cookie('state', 'user')
    return response

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    usr = request.POST.get('usr', '')
    psw = request.POST.get('psw', '')
    pswc = request.POST.get('pswc', '')
    contact = request.POST.get('contact', '')
    address = request.POST.get('address', '')
    if psw != pswc:
        messages.error(request, '两次输入的密码不一致！')
        return redirect('register')
    if len(psw) < 6:
        messages.error(request, '密码长度至少为6！')
        return redirect('register')
    if usr=='' or psw=='' or address=='':
        messages.error(request, '请填写所有必填内容！')
        return redirect('register')
    lastnum = 0
    for x in User.objects.all():
        if usr == x.uname:
            messages.error(request, '用户名已存在！')
            return redirect('register')
        if int(x.unum[1:]) > lastnum:
            lastnum = int(x.unum[1:])
    unum = 'U' + str(lastnum + 1).zfill(4)
    user = User(unum=unum, uname=usr, passwd=getmd5(psw), contact=contact, address=address)
    user.save()
    messages.error(request, '注册成功！请等待管理员审批！')
    return HttpResponseRedirect('/login')

def logout(request):
    res = HttpResponseRedirect('/login')
    res.delete_cookie('user')
    res.delete_cookie('state')
    return res

def loginManager(request):
    if request.method == 'GET':
        return render(request, 'loginManager.html')
    num = request.POST.get('num', '')
    psw = request.POST.get('psw', '')
    user = ''
    for x in Manager.objects.all():
        if x.mnum == num:
            user = x
            break
    if user == '':
        messages.error(request, '管理员账号不存在！')
        return redirect('loginManager')
    psw = getmd5(psw)
    if user.passwd != psw:
        messages.error(request, '管理员账号或密码错误！')
        return redirect('loginManager')
    response = HttpResponseRedirect('/')
    response.set_cookie('user', user.mnum)
    response.set_cookie('state', 'manager')
    return response