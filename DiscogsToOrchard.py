import discogs_client
import csv
import time

def chillRequests(startTime,reqCount):

    if reqCount == 20:
        time.sleep(70)
        startTime = time.monotonic()
        reqCount = 0
    else:
        reqCount += 1
    return reqCount, startTime
    
        
    


d = discogs_client.Client('YOUR APP NAME', user_token="YOUR TOKEN")
labelMapping = {}
releaseID = []
reqCount = 0
startTime = time.monotonic()
labelCatalog = d.label(34745)
reqCount, startTime = chillRequests(startTime,reqCount)
metalanguage = 'English'
startDate = '1/1/2018'
    

for i in range(0,len(labelCatalog.releases)):

    currInfo = labelCatalog.releases[i].data
    idInt = currInfo.get('id')
    reqCount, startTime = chillRequests(startTime,reqCount)
    tracks = labelCatalog.releases[i].tracklist
    catno = currInfo.get('catno')
    if i%50 == 0:
        print(str(i)+' releases completed')
    year = currInfo.get('year')
    releaseDate = '6/6/'+str(year)
    
    releaseFormat = currInfo.get('format')
    releaseName = currInfo.get('title')
    artist = currInfo.get('artist')[0].get('name')
    genre = labelCatalog.releases[i].genres
    reqCount, startTime = chillRequests(startTime,reqCount)
    num_tracks = len(tracks)
    
    for j in range(0, num_tracks):
        idStr = str(idInt)+'-'+str(j+1)
        releaseID.append(idStr);
        labelMapping[idStr] = {}
        labelMapping[idStr]['trackNumber'] = tracks[j].data.get('position')
        title = tracks[j].data.get('title')
        labelMapping[idStr]['trackTitle'] = title
        title = title.replace(' ','')
        title = title.replace("'","")
        labelMapping[idStr]['filename'] = title+'.wav'
        labelMapping[idStr]['releaseDate']=releaseDate
        labelMapping[idStr]['startDate']=startDate
        labelMapping[idStr]['year'] = str(year) + ' Norton Records'
        labelMapping[idStr]['format'] = releaseFormat 
        labelMapping[idStr]['releaseName'] = releaseName
        labelMapping[idStr]['catno']= catno
        labelMapping[idStr]['metaLanguage'] = 'English'
        labelMapping[idStr]['genre'] = genre
        labelMapping[idStr]['id'] = idInt
        if artist == 'Various' and tracks[j].data.get('artists') is not None:
            labelMapping[idStr]['artist'] = tracks[j].data.get('artists')[0].get('name')
        else:
            labelMapping[idStr]['artist'] = artist
        songwriters = ''
        extraartists = tracks[j].data.get('extraartists')
        if extraartists:
            for k in range(0,len(extraartists)):
                if k != 0:
                    songwriters += '|'
                songwriters += extraartists[k].get('name')
        labelMapping[idStr]['songwriters'] = songwriters
    
                

fieldnames = ['releaseName','catno','trackNumber','trackTitle','releaseDate',
              'startDate','year','format','catno','metaLanguage','genre','songwriters',
              'filename', 'id','artist']
with open('names.csv', 'w') as csvfile:
    
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    for ids in releaseID:
        writer.writerow(labelMapping[ids])



def getInfo(id, whichInfo):
        return d.release(id).fetch('community').get(whichInfo);



def calcWantedness(labelMap, idString):
     wantRatio= labelMap[idString]['want']/labelMap[idStr]['have']
     return wantRatio * (labelMap[idStr]['want']+labelMap[idStr]['have'])








    
   
    