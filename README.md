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
- Available skills table is empty

  First run application required about 7-10 minutes to first update database.
  Give it time to update itself and refresh browser.
  
