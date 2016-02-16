'''
	database initialization
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Catalog, CatalogItem, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create 'admin' user
admin = User(name="admin", email="admin@catalog.com")
session.add(admin)
session.commit()

### Add initial entries ###

# First catalog
catalog = Catalog(user=admin, name="Baseball")
session.add(catalog)
session.commit()

catalogItem = CatalogItem(user=admin, name="Chicago White Sox",
	description="The Chicago White Sox are an American professional baseball team based in the South Side of Chicago, Illinois.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Cleveland Indians",
	description="The Cleveland Indians are an American professional baseball team based in Cleveland, Ohio, that competes in Major League Baseball.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Detroit Tigers",
	description="The Detroit Tigers are an American professional baseball team based in Detroit, Michigan.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Kansas City Royals",
	description="The Kansas City Royals are an American professional baseball team, founded in 1969 and based in Kansas City, Missouri.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Minnesota Twins",
	description="The Minnesota Twins are a Major League Baseball (MLB) team based in Minneapolis, Minnesota.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

# Second catalog
catalog = Catalog(user=admin, name="Basketball")
session.add(catalog)
session.commit()

catalogItem = CatalogItem(user=admin, name="Chicago Bulls",
	description="The Chicago Bulls are an American professional basketball team based in Chicago, Illinois.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Cleveland Cavaliers",
	description="The Cleveland Cavaliers, also known as the Cavs, are an American professional basketball team based in Cleveland, Ohio.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Detroit Pistons",
	description="The Detroit Pistons are an American professional basketball team based in Auburn Hills, Michigan, a suburb of Detroit.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Indiana Pacers",
	description="The Indiana Pacers are a professional basketball team based in Indianapolis, Indiana.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Milwaukee Bucks",
	description="The Milwaukee Bucks are an American professional basketball franchise based in Milwaukee, Wisconsin.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

# Third catalog
catalog = Catalog(user=admin, name="Football")
session.add(catalog)
session.commit()

catalogItem = CatalogItem(user=admin, name="Chicago Bears",
	description="The Chicago Bears are a professional American football team in Chicago, Illinois.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Detroit Lions",
	description="The Detroit Lions are a professional American football team based in Detroit, Michigan.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Green Bay Packers",
	description="The Green Bay Packers are a professional American football team based in Green Bay, Wisconsin, that competes in the National Football League (NFL).",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Minnesota Vikings",
	description="The Minnesota Vikings are a professional American football team based in Minneapolis, Minnesota.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

# Fourth catalog
catalog = Catalog(user=admin, name="Hockey")
session.add(catalog)
session.commit()

catalogItem = CatalogItem(user=admin, name="Chicago Blackhawks",
	description="The Chicago Blackhawks (spelled Black Hawks before 1986, and known colloquially as the Hawks) are a professional ice hockey team based in Chicago, Illinois.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Colorado Avalanche",
	description="The Colorado Avalanche are a professional ice hockey franchise based in Denver, Colorado.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Dallas Stars",
	description="The Dallas Stars are a professional ice hockey team based in Dallas, Texas.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Minnesota Wild",
	description="The Minnesota Wild are a professional ice hockey team based in St. Paul, Minnesota, United States.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Nashville Predators",
	description="The Nashville Predators are a professional ice hockey team based in Nashville, Tennessee.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="St. Louis Blues",
	description="The St. Louis Blues are a professional ice hockey team in St. Louis, Missouri.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Winnipeg Jets",
	description="The Winnipeg Jets are a professional ice hockey team based in Winnipeg, Manitoba.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

# Fifth catalog
catalog = Catalog(user=admin, name="Soccer")
session.add(catalog)
session.commit()

catalogItem = CatalogItem(user=admin, name="Chicago Fire",
	description="Chicago Fire Soccer Club is an American professional soccer club based in the Chicago suburb of Bridgeview, Illinois, United States.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Columbus Crew SC",
	description="Columbus Crew SC is a professional soccer club based in Columbus, Ohio, United States, which competes in Major League Soccer (MLS) in the Eastern Conference of the league.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="D.C. United",
	description="D.C. United is an American professional soccer club based in Washington, D.C.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Montreal Impact",
	description="The Montreal Impact (French: Impact de Montreal) is a Canadian professional soccer team based in Montreal, Quebec that competes in the Eastern Conference of Major League Soccer (MLS).",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="New England Revolution",
	description="The New England Revolution is an American professional soccer club based in the Greater Boston area that competes in Major League Soccer (MLS), in the Eastern Conference of the league.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="New York City FC",
	description="New York City Football Club is an American professional soccer team based in New York City that competes in Major League Soccer (MLS) in the Eastern Conference of the league.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="New York Red Bulls",
	description="The New York Red Bulls are an American professional soccer team based in Harrison, New Jersey.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Orlando City SC",
	description="Orlando City Soccer Club is an American professional soccer club based in Orlando, Florida that competes in the Eastern Conference of Major League Soccer (MLS).",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Philadelphia Union",
	description="The Philadelphia Union is an American professional soccer team based in Chester, Pennsylvania which competes in Major League Soccer (MLS) in the Eastern Conference of the league.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

catalogItem = CatalogItem(user=admin, name="Toronto FC",
	description="Toronto FC (TFC) is a Canadian professional soccer club based in Toronto, Ontario that competes in Major League Soccer (MLS), in the Eastern Conference of the league.",
	catalog=catalog)
session.add(catalogItem)
session.commit()

print "Database initialized!"
