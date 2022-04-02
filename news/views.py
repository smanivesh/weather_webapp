from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import xml
from bs4 import BeautifulSoup
import requests
from .forms import CustomUserCreationForm
# Create your views here.





def loginPage(request):
    page ='login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')


    return render(request, 'news/login_register.html',{'page': page})


def logoutUser(request):
    logout(request)
    return redirect('main')    

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('home')

    context = {'form': form, 'page': page}
    return render(request,'news/login_register.html',context)








@login_required(login_url='login')
def homePage(request):
    r=requests.get("https://www.jagran.com/news/national-news-hindi.html?itm_medium=national&itm_source=dsktp&itm_campaign=navigation")
    soup=BeautifulSoup(r.content,'lxml')
    heading=soup.find_all('div',{'class':'h3'})
    
    
    heading=heading[1:11]
    

    News=[]
    for news in heading:
      News.append(news.text)

    

    if "state-name" in request.GET:
        state=request.GET.get('state-name')

        url=f"https://www.jagran.com/state/{state}"   #formattable strings

# GEtting news from Times of India
        r1=requests.get(url)
    
        soup1 = BeautifulSoup(r1.content, 'html5lib')

        heading1 = soup1.find_all('div',{'class':'h3'})
        image=soup1.find_all('img',{'class':'lazy'})

# removing footers
        heading1=heading1[1:11]
        image=image[0:10]
  
        News=[]
       

        for con in heading1:
            News.append(con.text)
        
        Image=[]
        base_url="https:"
        for img in image:
          Image.append(base_url+img.attrs['data-src'])


        return render(request, 'news/index.html', {'state':state, 'Image':Image, 'News': News})


    return render(request, 'news/index.html', {'News': News})




