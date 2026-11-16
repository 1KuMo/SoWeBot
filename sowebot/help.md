requests (GET):
    requests et http methods : 
        https://www.datacamp.com/fr/tutorial/making-http-requests-in-python
    request headers : 
        https://scrapfly.io/blog/posts/python-requests-headers-guide
        https://requests.readthedocs.io/en/latest/user/quickstart/#custom-headers
        
        Accept: what response formats the client can handle.
        Authorization: credentials or a token for accessing a protected resource.

        note ; c'est a pas parce qu'on met "Accept": "application/json" que le format
               renvoyé sera en json. on informe juste le serveur que c'est notre méthode 
               'préférée' mais si il peut pas il renverra un autre format 
        
        Bearer token : 
        - https://stackoverflow.com/questions/29931671/making-an-api-call-in-python-with-an-api-that-requires-a-bearer-token
        - https://www.askpython.com/python/api-calls-bearer-token-authentication

env :
    j'ai repris un morceau de code de mon socialbot.
    pour plus d'infos ; https://pypi.org/project/python-dotenv/

json:
    structure générale du JSON :
    ( je me suis aidé de l'IA pour ce bel affichage )

    emplois_du_temps : list
    │
    └── cours : dict
        ├── id : int
        ├── name : str
        ├── date : str
        ├── start : str
        ├── end : str
        ├── type : str
        ├── evaluation : str
        ├── place : dict
        │   ├── id : int
        │   ├── name : str
        │   └── dataBeacon : None
        │
        ├── data : dict
        │   ├── bi : None
        │   ├── cfa : None
        │   ├── erp : None
        │   ├── data1 à data6 : None
        │   ├── data7 : str ### ELEARNING 
        │   ├── data8 : str
        │   ├── region : None
        │   └── dataJson : str
        │
        ├── closingDelay : int
        ├── openingDelay : int
        ├── urlValidate : None
        ├── textValidate : None
        ├── documentToSignUrlValidate : None
        └── documentToSignTextValidate : None

datetime: hell
    https://docs.python.org/3/library/datetime.html
    
    str -> date : https://www.geeksforgeeks.org/python/python-datetime-strptime-function/
                  https://www.programiz.com/python-programming/datetime/strptime

    timedelta : https://docs.python.org/3/library/datetime.html#datetime.timedelta



refresh token: hell2
    POST request : 
        https://www.geeksforgeeks.org/python/python-requests-post-request-with-headers-and-body/
    
    (1h30 pour le trouver ce bout de code ils l'ont bien caché (et jsais pas chercher) la prochaine fois j'utiliserais un paquet tracer)
                getTokenByRefresh(e) {
                return L1(
                    this.http.post(
                    `${ this.discovery }/portal/authentication/token/refresh`,
                    null,
                    {
                        headers: (new Ir).set('Authorization', `Bearer ${ e }`)
                    }
                    )
                )
                }
                getTokenFromOld(e) {
                return L1(
                    this.http.post(
                    `${ this.discovery }/portal/authentication/token/old`,
                    null,
                    {
                        headers: (new Ir).set('Authorization', `Bearer ${ e }`)
                    }
                    )
                )
                }

    dans mon ancienne structure, quand on avait une erreur 400 ou 401 on s'arrêtait.. maintenant qu'on a l'end point pour refresh le token
    on refresh le token ( bg nan ? ) :D