# Recruitment_Centre
Application Recruitment_Centre is a django server application which scrape (scrapy, splash) forum https://forums.eveonline.com/c/marketplace/character-bazaar and https://skillboard.eveisesi.space/,
looking for the pilots on sale and adds them to the database.

After about one minute from the start of the application, the first scrapy work begins. 
Database is updating every one hour. 

Application share own api:

- /Api/PostRecruits/
- /Api/PostRecruit/\<int:pk>
- /Api/Recruits/
- /Api/Recruit/\<int:pk>
- /Api/GroupedSkillzs/
- /Api/GroupedSkillz/\<int:pk>
- /Api/Skills/
- /Api/Skill/\<int:pk>
- /Api/AllSkills/
- /Api/Search/


It also has a built-in pilot search engine on default server adress 127.0.0.1:8000

## Requirements: 
- Tested on Docker Desktop 4.13.1 and below - probably are some problems with newer versions
- .env file in Recruitment_Centre folder

  example .env file:
  ```sh
  DEBUG=1
  SECRET_KEY=0i(%))rq+!gch!45rhg=o-5a1ev)=jlu=anzg%!a4jvv*ylpq
  DJANGO_ALLOWED_HOSTS=*
  DB_NAME=postgres
  DB_USER=postgres
  DB_PASSWORD=postgresPassword
  ```

## Run:

```sh
docker-compose up --build
```

## Known problems:
- "./run.sh now such file or directory"

  It should use Unix-style line endings instead of Windows. 
  This problem occurs for me as well on Windows 10.
  You should run the following command before cloning the repository:
  ```
  git config --global core.autocrlf false
  ```
  Then clone the repository and proceed

- Available skills table is empty

  First run application required about 7-10 minutes to first update database.
  Give it time to update itself and refresh browser.
  
- {"error": 502, "type": "RenderError", "description": "Error rendering page", "info": {"type": "Network", "code": 6, "text": "SSL handshake failed", "url": "..."}}
  
  Problem appears for me on Docker Desktop 4.14 and above, versions 4.13.1 and below working properly
  https://github.com/scrapinghub/splash/issues/1172
  
