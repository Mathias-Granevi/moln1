Jag använder inte lägre python scriptet q_to_sql.py då detta bara var ett script för att testa att föra över data från storage queue till min sql databas.
Nu går den processen automatiskt med hjälp av Azure Logic apps (se logic_apps.png).
I Logic apps så har jag en process som kontrollerar ifall det finns meddelanden i min storage queue. Om det finns det så körs det en parse json som läser json-strängen och omvandlar den så att den kan insertas i sql databasen. Därefter så tas meddelandet bort och processen börjar om.
