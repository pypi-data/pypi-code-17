from gnip_analysis_pipeline.enrichment.enrichment_base import BaseEnrichment

truck_keywords = ['#ProjectTitan','nissan'',#LikeATitan','#NissanTitan','@NissanTrucks','@NissanUSA',
    '@ChevyTrucks','#SilveradoStrong','#ChevyColorado','#Silverado','#ChevyPickUpLines','#GameChanger',
    '2500HD','3500HD','#ChevySalutes','@Ford','#FordTrucks','#F150','#2016F150','F-150','@ThisIsGMC',
    '#ProfessionalGrade','#ProGrade','#Sierra','#Canyon','#GMCCanyon','#GMCSierra','#WhatsInAYukon',
    '#SierraElevationEdition','#GMCYukon','#Yukon','#Ram','@RamTrucks','#RootsWingsRam','#GutsGloryRam',
    '#RamRebel','#RamLife','#RamCountry','#RamRules','#RamSalutes','#RamTrucks','#RamFan','@Toyota',
    '#Tacoma','#ToyotaTacoma','#ToyotaTundra','#Tundra']
#truck_keywords.extend(['truck','trucks','pickup'])

chipotle_keywords = ['@ChipotleTweets','@ChipotleMedia','chipotle','#chipotle']

iphone_keywords = ['iphone','#iphone','iphone6','#iphone6','iphone6s','#iphone6s','iphone7','#iphone7']

alcbev_keywords = ["Alcohol","appletini","appletinis","Booze","boozed","boozin","boozing","Champagne","daiquiri","jelloshots","Lambic","Liquer","Liquor","maitai","margarita","margaritas","martini","martinis","mimosa","mimosas","mojito","mojitos","Ogogoro","Ouzo","pinacolada","pinacoladas","Pisco","Rakia","Sake","sangria","sangrias","Shochu","thirstythursday","winetasting","#Alcohol","#AlcoholicBeverage","#AlcoholicDrink","#appletini","#appletinis","#bloodymary","#Booze","#boozed","#boozin","#boozing","#Champagne","#daiquiri","#happyhour","#irishcoffee","#irishcoffees","#jell-oshot","#jell-oshots","#jelloshot","#jelloshots","#jelloshots","#junglejuice","#Lambic","#Liquer","#Liquor","#longislandicedtea","#longislandicedteas","#maitai","#maitais","#maitai","#margarita","#margaritas","#martini","#martinis","#mimosa","#mimosas","#mojito","#mojitos","#Ogogoro","#Ouzo","#pinacolada","#pinacoladas","#pinacolada","#pinacoladas","#pinogrigio","#Pisco","#Rakia","#Sake","#sangria","#sangrias","#Shochu","#singaporesling","#thirstythursday","#thirstythursday","#tuesdayboozeday","#wastedwednesday","#wastedwednesdays","#whiterussian","#winetasting","Absinthe","Armagnac","Bourbon","Brandy","Cognac","Gin","Mezcal","Whiskey","Rum","Schnapps","Scotch","Soju","Tequila","Vodka","Vermouth","Campari","#Absinthe","#Armagnac","#Bourbon","#Brandy","#cognac","#Gin","#mezcal","#Whiskey","#Rum","#schnapps","#scotch","#Soju","#Tequila","#Vodka","#Vermouth","#Campari","Ale","Ales","Beer","Beers","Hefeweizen","Home","Ipa","india","Lager","Lagers","Homebrew","Homebrews","Lambic","Micro","Microbrews","microbrewery","Pilsner","Pilsners","Craft","#Ale","#Ales","#Beer","#Beers","#Hefeweizen","#Homebrew","#Ipa","#indiapaleale","#Lager","#Lagers","#Homebrew","#Homebrews","#Lambic","#Microbrew","#Microbrews","#microbrewery","#Pilsner","#Pilsners","#craftbeer","Breton","Cabernet","Cabernet","Chardonnay ","malbec","Merlot ","Muscat ","pino","Pinot","Pinot","prosecco","Red","Rosé","Sauvignon","Shiraz ","Steen ","Syrah","White","Wine","Zinfandel","Dessert","winetasting","#Breton","#Cabernet","#CabernetSauvignon ","#Chardonnay ","#malbec","#Merlot ","#Muscat ","#Pinot","#PinotGrigio","#PinotNoir","#prosecco","#RedWine","#rose","#SauvignonBlanc","#Shiraz ","#Steen ","#Syrah","#WhiteWine","#Wine","#Zinfandel","#dessertwine","#winetasting"]

class TruckTweetLabeler(BaseEnrichment):
    def __init__(self):
        self.keywords = truck_keywords

    def enrichment_value(self,tweet):
        return any(keyword.lower() in tweet['enrichments']['NLTKTweetTokenizeBody'] for keyword in self.keywords)

class TruckUserLabeler(BaseEnrichment):
    def __init__(self):
        self.keywords = truck_keywords

    def enrichment_value(self,tweet):
        return any(keyword.lower() in tweet['enrichments']['NLTKTweetTokenizeBio'] for keyword in self.keywords)

class IphoneTweetLabeler(BaseEnrichment):
    def __init__(self):
        self.keywords = iphone_keywords

    def enrichment_value(self,tweet):
        return any(keyword.lower() in tweet['enrichments']['NLTKTweetTokenizeBody'] for keyword in self.keywords)

class ChipotleTweetLabeler(BaseEnrichment):
    def __init__(self):
        self.keywords = chipotle_keywords

    def enrichment_value(self,tweet):
        return any(keyword.lower() in tweet['enrichments']['NLTKTweetTokenizeBody'] for keyword in self.keywords)

class AlcBevTweetLabeler(BaseEnrichment):
    def __init__(self):
        self.keywords = alcbev_keywords

    def enrichment_value(self,tweet):
        return any(keyword.lower() in tweet['enrichments']['NLTKTweetTokenizeBody'] for keyword in self.keywords)
class_list = [
        'TruckTweetLabeler',
        'TruckUserLabeler',
        'ChipotleTweetLabeler',
        'IphoneTweetLabeler',
        'AlcBevTweetLabeler',
        ]
