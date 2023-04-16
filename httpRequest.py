import requests

"""
r = requests.get('https://xkcd.com/1906/')
r.status_code
r.headers['Content-Type']


ploads = {'Username':'healthclient','Password':'HealthclientAPI$'}
r = requests.get('https://httpbin.org/get',params=ploads)
"""


#r = requests.post('http://197.159.136.241:1936/healthclient/api/Token', json= {"Username":"healthclient","Password":"HealthclientAPI$"})
#print(r.json()['token'])

r = requests.get('https://apps.mnotify.net/smsapi?key=XxUJ7EtoUwCZFl8vCM7Lv1hSV&to=233544875339&msg=pataipan&sender_id=Ahene Group',params="")

print(r.json())

"""
query = {'lat':'45', 'lon':'180'}
response = requests.get('http://api.open-notify.org/iss-pass.json', params=query)
print(response.json())
# to download image and save
"""

#receive = requests.get('https://imgs.xkcd.com/comics/making_progress.png')
#with open(r'C:\Users\Dell\Desktop\comics\image5.png','wb') as f:
 #   f.write(receive.content)