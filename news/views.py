from newsapi import settings
from django.shortcuts import render
from django.http.response import HttpResponse
import requests

def home(request):
    page = request.GET.get('page',1)
    search = request.GET.get('search',None)

    if search is None or search =='top':
        #get the top news

        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format("india",1,settings.APIKEY)
    else:
        #get the search query request
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(search,"popularity",page,settings.APIKEY)

    r = requests.get(url=url)    

    data = r.json()

    if data ["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")

    data = data["articles"]
    context = {
        "success":True,
        "data":[],
        "search":search
    }
    for i in data:
        context["data"].append({
            "title":i["title"],
            "description": ""if i["description"] is None else i["description"],
            "url":i["url"],
            "image":temp_img if i["urlToImage"] is None else i["urlToImage"],
            "publishedat":i["publishedAt"]
        })
    return render(request,"index.html",context=context)