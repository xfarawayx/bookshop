from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
import hashlib

from .models import Book, Order
from login.models import User

def booklist(request):
    if 'state' not in request.COOKIES:
        return HttpResponseRedirect('/login')
    if request.COOKIES['state'] == 'manager':
        return HttpResponseRedirect('/bookManage')
    if request.COOKIES['state'] != 'user':
        return HttpResponseRedirect('/login')
    
    user = User.objects.get(unum=request.COOKIES['user'])
    books = Book.objects.all()
    
    if request.method == 'POST':
        if 'buy' in request.POST:
            selected_books = request.POST.getlist('selected_books')
            if len(selected_books) == 0:
                return redirect('booklist')
            book = Book.objects.get(bnum=selected_books[0])
            if book.overplus == 0:
                messages.error(request, '图书已售罄，请购买别的图书！')
                return redirect('booklist')
            lastnum = 0
            for x in Order.objects.all():
                if int(x.onum[1:]) > lastnum:
                    lastnum = int(x.onum[1:])
            onum = 'O' + str(lastnum + 1).zfill(5)
            order = Order(onum=onum, bnum=book, unum=user)
            order.save()
            book.overplus -= 1
            book.save()
            messages.error(request, '购买成功！')
        else:
            search_type = request.POST.get('search_type')
            if search_type == 'name':
                book_name = request.POST.get('book_name')
                if book_name:
                    books = books.filter(bname__icontains=book_name)
            elif search_type == 'price':
                min_price = request.POST.get('min_price')
                max_price = request.POST.get('max_price')
                if min_price and max_price:
                    books = books.filter(price__gte=min_price, price__lte=max_price)
                elif min_price:
                    books = books.filter(price__gte=min_price)
                elif max_price:
                    books = books.filter(price__lte=max_price)
    
    return render(request, 'booklist.html', {'books': books, 'username': user.uname})

def orderlist(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'user' :
        return HttpResponseRedirect('/login')
    user = User.objects.get(unum=request.COOKIES['user'])
    orders = Order.objects.filter(unum=user.unum)
    return render(request, 'orderlist.html', {'orders': orders, 'username': user.uname})

def profile(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'user' :
        return HttpResponseRedirect('/login')
    user = User.objects.get(unum=request.COOKIES['user'])
    return render(request, 'profile.html', {'usernum': user.unum, 'username': user.uname, 'contact': user.contact, 'address': user.address})

def getmd5(s):
    s += 'orzyadie'
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()

def modify(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'user' :
        return HttpResponseRedirect('/login')
    user = User.objects.get(unum=request.COOKIES['user'])
    if request.method == 'GET':
        return render(request, 'modify.html', {'username': user.uname})
    usr = request.POST.get('usr', '')
    psw = request.POST.get('psw', '')
    npsw = request.POST.get('npsw', '')
    npswc = request.POST.get('npswc', '')
    contact = request.POST.get('contact', '')
    address = request.POST.get('address', '')
    if getmd5(psw) != user.passwd:
        messages.error(request, '原密码输入错误！')
        return redirect('modify')
    if npsw != npswc:
        messages.error(request, '两次输入的密码不一致！')
        return redirect('modify')
    if len(npsw) < 6:
        messages.error(request, '密码长度至少为6！')
        return redirect('modify')
    if usr != '':
        for x in User.objects.all():
            if usr == x.uname:
                messages.error(request, '用户名已存在！')
                return redirect('modify')
        user.uname = usr
    if npsw != '':
        user.passwd = getmd5(npsw)
    if contact != '':
        user.contact = contact
    if address != '':
        user.address = address
    user.save()
    messages.error(request, '修改成功！')
    return HttpResponseRedirect('/profile')