from django.shortcuts import render
from django.http import JsonResponse
import requests
from codeSearch.models import SearchResults


# Create your views here.
def getRawFile(request):
    response1 = requests.get(request.GET['objectUrl'])

    response2 = requests.get(response1.json()['download_url'])

    elements = SearchResults.objects.filter(fileUrl=response1.json()['download_url'],searchTerm=request.GET['searchTerm'])
    if not (elements):
        newSearch = SearchResults(searchTerm=request.GET['searchTerm'],fileUrl=response1.json()['download_url'])
        newSearch.save()
    
    olderSearchTerms = (SearchResults.objects.filter(fileUrl=response1.json()['download_url']).all())

    return JsonResponse({'code':response2.text,'url':response1.json()['download_url'],'olderSearchTerms':list(map(lambda x:x.searchTerm,olderSearchTerms))})

def getPrevOpenedFiles(request):
    elements = SearchResults.objects.values('fileUrl').distinct()

    return JsonResponse({'prev':list(elements)})

def getRawFileFromHistory(request):
    response = requests.get(request.GET['url'])

    olderSearchTerms = (SearchResults.objects.filter(fileUrl=request.GET['url']))

    return JsonResponse({'code':response.text,'url':request.GET['url'],'olderSearchTerms':list(map(lambda x:x.searchTerm,olderSearchTerms))})


def searchGit(request):
    requestHeaders = {}
    requestHeaders['q'] = request.GET['searchTerms']
    requestHeaders['in']='file'
    requestHeaders['page'] = request.GET['page']

    requestHeaders['per_page'] = 10
    if(request.GET['language']!='null') and (request.GET['language']!=''):
        requestHeaders['q'] = requestHeaders['q'] + ' language:'+ request.GET['language']

    if(request.GET['owner']!='null') and (request.GET['owner']!=''):
        requestHeaders['q'] = requestHeaders['q'] + ' user:' + request.GET['owner']

    if(request.GET['repo']!='null') and ((request.GET['repo']!='')):
        requestHeaders['q'] = requestHeaders['q'] + ' repo:' + request.GET['repo']
    
    print(requestHeaders)

    response = requests.get('https://api.github.com/search/code',requestHeaders,headers={'Accept':'application/vnd.github.v3.text-match+json'},auth=(username,password))

    return JsonResponse(response.json())
