from django.shortcuts import render, redirect
from .forms import RegisterWebsite
from .models import Website
from wit import Wit
import speech_recognition as sr
import webbrowser 
import requests
import urllib.parse
import re
# Create your views here.

access_token = 'OKAAWMQUOTYSPEF6XIRXOKFLNMOXSHZK'




def index(request):
    if request.method == 'POST':
        form = RegisterWebsite(request.POST)
        if form.is_valid():
            name = form.cleaned_data['site_name'].lower();
            address = form.cleaned_data['site_address'].lower()
            new_website = Website(site_name=name,
                site_address=address)
            new_website.save()
            update_entity = {'keyword':name,'synonyms':[name]}
            headers = {'authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json'}
            requests.post('https://api.wit.ai/entities/website/keywords', headers = headers,
                         json = update_entity)
    else:
        form = RegisterWebsite()

    data=".........."
    num_sites = Website.objects.all().count()
    context = {
        'num_sites': num_sites,
        'data':data,
        'form':form
    }
    return render(request, 'index.html', context=context)

def goToWebsite(request):
    import speech_recognition as sr

    # get audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        audio = r.listen(source)

    # recognize the audio as text and send it to wit.ai for response
    try:
        output = " " + r.recognize_wit(audio,access_token)
    except sr.UnknownValueError:
        output = "Could not understand audio"
    except sr.RequestError as e:
        output = "Could not request results; {0}".format(e)        
    client = Wit(access_token)
    resp = client.message(output)
    num_sites = Website.objects.all().count()
    context = {
        'num_sites': num_sites,
        'data':output,
        'form': RegisterWebsite()
    }
    # get intent from response. If it does not exist return error message.
    try:
        intent = resp['intents'][0]['name']
    except:
        context['data'] += ". Could not understand your intent or audio"
        return render(request, 'index.html', context=context )

    # analyze the intent confidence. Only act if confidence is over 70%.
    if resp['intents'][0]['confidence'] < 0.70:
       context['data'] += ". Your intent was unclear!"
       return render(request, 'index.html', context=context )
    else:     
        if intent == 'get_website':
            site_name = resp['entities']['website:website'][0]['value']

            # check if the entity is presaved
            if Website.objects.filter(site_name=site_name).exists():
                site = Website.objects.get(site_name = site_name)
                site_address = site.site_address
                webbrowser.open(site_address)
            else:
                webbrowser.open('http://'+site_name +'.com')
        elif intent == 'get_youtube_video':
            video = resp['entities']['video:video'][0]['value']
            query_string = urllib.parse.urlencode({"search_query" : video})
            youtube_search = requests.get('https://www.youtube.com/results?'+query_string)
            search_results = re.findall(r'\"videoId\"\:\"(.{11})\"', youtube_search.text)
            print("http://www.youtube.com/watch?v=" + search_results[1])
            webbrowser.open_new("http://www.youtube.com/watch?v={}".format(search_results[3]))
    
    return render(request, 'index.html', context=context )


