from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages

from main.models import Book, Order, User
from login.models import Manager
import hashlib

def getmd5(s):
    s += 'orzyadie'
    md = hashlib.md5()
    md.update(s.encode('utf-8'))
    return md.hexdigest()

def bookManage(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    books = Book.objects.all()
    if request.method == 'POST':
        if 'search' in request.POST:
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
            elif search_type == 'combined':
                min_overplus = request.POST.get('min_overplus')
                min_price = request.POST.get('min_price')
                max_price = request.POST.get('max_price')
                if not min_overplus:
                    messages.error(request, '请输入图书余量！')
                    return redirect('booklist')
                if min_price and max_price:
                    books = books.filter(overplus__gte=min_overplus, price__gte=min_price, price__lte=max_price)
                elif min_price:
                    books = books.filter(overplus__gte=min_overplus, price__gte=min_price)
                elif max_price:
                    books = books.filter(overplus__gte=min_overplus, price__lte=max_price)
        else:
            selected_books = request.POST.getlist('selected_books')
            if len(selected_books) == 0:
                return redirect('bookManage')
            book = Book.objects.get(bnum=selected_books[0])
            return HttpResponseRedirect('/bookEdit/' + book.bnum)
    return render(request, 'bookManage.html', {'books': books})

def bookEdit(request, bnum):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    book = Book.objects.get(bnum=bnum)
    if request.method == 'GET':
        return render(request, 'bookEdit.html', {'book': book})
    book.btype = request.POST.get('btype', '')
    book.bname = request.POST.get('name', '')
    book.price = request.POST.get('price', '')
    book.overplus = request.POST.get('overplus', '')
    if int(book.overplus) < 0:
        messages.error(request, '图书余量不能小于0！')
        return redirect('/bookEdit/' + bnum)
    messages.error(request, '修改成功！')
    book.save()
    return redirect('bookManage')

def bookAdd(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    if request.method == 'GET':
        return render(request, 'bookAdd.html')
    book = Book()
    book.bnum = request.POST.get('bnum', '')
    book.btype = request.POST.get('btype', '')
    book.bname = request.POST.get('name', '')
    book.price = request.POST.get('price', '')
    book.overplus = request.POST.get('overplus', '')
    if int(book.overplus) < 0:
        messages.error(request, '图书余量不能小于0！')
        return redirect('/bookAdd')
    messages.error(request, '创建图书成功！')
    book.save()
    return redirect('bookManage')

def bookDelete(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    bnum = request.GET.get('bnum')
    book = get_object_or_404(Book, bnum=bnum)
    book.delete()
    messages.error(request, '删除图书成功！')
    return redirect('bookManage')

def userOrder(request, num):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    user = User.objects.get(unum=num)
    orders = Order.objects.filter(unum=user)
    return render(request, 'userOrder.html', {'orders': orders})

def userReset(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    unum = request.GET.get('unum')
    user = User.objects.get(unum=unum)
    user.passwd = getmd5('123456')
    user.save()
    messages.error(request, '密码已重置为123456！')
    return redirect('userManage')

def userManage(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    users = User.objects.all()
    if request.method == 'POST':
        selected_users = request.POST.getlist('selected_users')
        if len(selected_users) == 0:
            return redirect('userManage')
        user = selected_users[0]
        if 'view' in request.POST:
            return HttpResponseRedirect('userOrder/' + user)
        if 'edit' in request.POST:
            return HttpResponseRedirect('userEdit/' + user)
    return render(request, 'userManage.html', {'users': users})

def userEdit(request, num):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    if request.method == 'POST':
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        state = request.POST.get('state') == 'on'
        user = User.objects.get(unum=num)
        user.uname = name
        user.contact = contact
        user.address = address
        user.state = state
        user.save()
        messages.error(request, '保存成功')
        return redirect('userManage')
    
    user = User.objects.get(unum=num)
    return render(request, 'userEdit.html', {'user': user})

def userVerify(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    users = User.objects.filter(state=False)
    if request.method == 'GET':
        return render(request, 'userVerify.html', {'users': users})
    selected_users = request.POST.getlist('selected_users')
    for num in selected_users:
        user = User.objects.get(unum=num)
        user.state = True
        user.save()
    messages.error(request, '已通过选定用户')
    return redirect('userManage')

def selfModify(request):
    if 'state' not in request.COOKIES or request.COOKIES['state'] != 'manager' :
        return HttpResponseRedirect('/loginManager')
    manager = Manager.objects.get(mnum=request.COOKIES['user'])
    if request.method == 'GET':
        return render(request, 'selfModify.html')
    psw = request.POST.get('psw', '')
    npsw = request.POST.get('npsw', '')
    npswc = request.POST.get('npswc', '')
    if getmd5(psw) != manager.passwd:
        messages.error(request, '原密码输入错误！')
        return redirect('selfModify')
    if npsw != npswc:
        messages.error(request, '两次输入的密码不一致！')
        return redirect('selfModify')
    if len(npsw) < 6:
        messages.error(request, '密码长度至少为6！')
        return redirect('selfModify')
    manager.passwd = getmd5(npsw)
    manager.save()
    messages.error(request, '修改成功！')
    return redirect('bookManage')