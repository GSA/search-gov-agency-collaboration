import scrapy
import json
import csv

from metadatachecker.items import MetadatacheckerItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

class MetadatacheckerSpiderSpider(scrapy.Spider):
    name = 'metadatachecker_spider'
    start_urls = []

    with open('searchgov_domains.csv') as csvfile:    
        csvReader = csv.reader(csvfile)
        next(csvReader)
        for row in csvReader:
            start_urls.append('https://' + row[0])

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse,
                                      errback=self.errback_httpbin)

    def parse(self, response):
        item = MetadatacheckerItem() # Creating a new Item object

        item['url'] = response.url
        item['httpCode'] = response.status

        item['dc'] = response.xpath("//meta[starts-with(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.')]/@name").extract
        item['dcAgency'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.agency')]/@content").extract_first()
        item['dcContributor'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.contributor')]/@content").extract_first()
        item['dcCreator'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.creator')]/@content").extract_first()
        item['dcCreatorNamecorporate'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.creator.namecorporate')]/@content").extract_first()
        item['dcDate'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.date')]/@content").extract_first()
        item['dcDateCreated'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.date.created')]/@content").extract_first()
        item['dcDateModified'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.date.modified')]/@content").extract_first()
        item['dcDateReviewed'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.date.reviewed')]/@content").extract_first()
        item['dcDateXMetadataLastModified'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.date.x-metadatalastmodified')]/@content").extract_first()
        item['dcDescription'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.description')]/@content").extract_first()
        item['dcFormat'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.format')]/@content").extract_first()
        item['dcIdentifier'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.identifier')]/@content").extract_first()
        item['dcLanguage'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.language')]/@content").extract_first()
        item['dcModified'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.modified')]/@content").extract_first()
        item['dcPublisher'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.publisher')]/@content").extract_first()
        item['dcPublisherAddress'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.publisher.address')]/@content").extract_first()
        item['dcPublisherNamecorporate'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.publisher.namecorporate')]/@content").extract_first()
        item['dcSubject'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.subject')]/@content").extract_first()
        item['dcTitle'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.title')]/@content").extract_first()
        item['dcType'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dc.type')]/@content").extract_first()

        item['dcterms'] = response.xpath("//meta[starts-with(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.')]/@name").extract
        item['dctermsAudience'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.audience')]/@content").extract_first()
        item['dctermsContributor'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.contributor')]/@content").extract_first()
        item['dctermsCoverage'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.coverage')]/@content").extract_first()
        item['dctermsCreated'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.created')]/@content").extract_first()
        item['dctermsCreator'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.creator')]/@content").extract_first()
        item['dctermsDate'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.date')]/@content").extract_first()
        item['dctermsDateAccepted'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.dateaccepted')]/@content").extract_first()
        item['dctermsDateCreated'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.datecreated')]/@content").extract_first()
        item['dctermsDateModified'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.datemodified')]/@content").extract_first()
        item['dctermsDateReviewed'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.datereviewed')]/@content").extract_first()
        item['dctermsDescription'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.description')]/@content").extract_first()
        item['dctermsFormat'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.format')]/@content").extract_first()
        item['dctermsIdentifier'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.identifier')]/@content").extract_first()
        item['dctermsIsPartOf'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.ispartof')]/@content").extract_first()
        item['dctermsIsReferencedBy'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.isreferencedby')]/@content").extract_first()
        item['dctermsIssued'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.issued')]/@content").extract_first()
        item['dctermsKeywords'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.keywords')]/@content").extract_first()
        item['dctermsLanguage'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.language')]/@content").extract_first()
        item['dctermsModified'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.modified')]/@content").extract_first()
        item['dctermsPublisher'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.publisher')]/@content").extract_first()
        item['dctermsSource'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.source')]/@content").extract_first()
        item['dctermsSubject'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.subject')]/@content").extract_first()
        item['dctermsTitle'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.title')]/@content").extract_first()
        item['dctermsType'] = response.xpath("//meta[contains(translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),'dcterms.type')]/@content").extract_first()

        item['og'] = response.xpath("//meta[starts-with(@property,'og:')]/@property").extract
        item['ogAuthor'] = response.xpath("//meta[@property='og:author']/@content").extract_first()
        item['ogDescription'] = response.xpath("//meta[@property='og:description']/@content").extract_first()
        item['ogImage'] = response.xpath("//meta[@property='og:image']/@content").extract_first()
        item['ogImageAlt'] = response.xpath("//meta[@property='og:image:alt']/@content").extract_first()
        item['ogImageHeight'] = response.xpath("//meta[@property='og:image:height']/@content").extract_first()
        item['ogImageSecureUrl'] = response.xpath("//meta[@property='og:image:secure_url']/@content").extract_first()
        item['ogImageType'] = response.xpath("//meta[@property='og:image:type']/@content").extract_first()
        item['ogImageUrl'] = response.xpath("//meta[@property='og:image:url']/@content").extract_first()
        item['ogImageWidth'] = response.xpath("//meta[@property='og:image:width']/@content").extract_first()
        item['ogLocale'] = response.xpath("//meta[@property='og:locale']/@content").extract_first()
        item['ogLocaleAlternate'] = response.xpath("//meta[@property='og:locale:alternate']/@content").extract_first()
        item['ogSeeAlso'] = response.xpath("//meta[@property='og:see_also']/@content").extract_first()
        item['ogSitename'] = response.xpath("//meta[@property='og:site_name']/@content").extract_first()
        item['ogTitle'] = response.xpath("//meta[@property='og:title']/@content").extract_first()
        item['ogType'] = response.xpath("//meta[@property='og:type']/@content").extract_first()
        item['ogUpdatedTime'] = response.xpath("//meta[@property='og:updated_time']/@content").extract_first()
        item['ogUrl'] = response.xpath("//meta[@property='og:url']/@content").extract_first()

        for ld in response.xpath("//script[@type='application/ld+json']/text()").extract():
            schemaorg = json.loads(ld)

            self.graphsParse(item, schemaorg)

        item['twitterCard'] = response.xpath("//meta[@name='twitter:card']/@content").extract_first()
        item['twitterCreator'] = response.xpath("//meta[@name='twitter:creator']/@content").extract_first()
        item['twitterCreatorId'] = response.xpath("//meta[@name='twitter:creator:id']/@content").extract_first()
        item['twitterDescription'] = response.xpath("//meta[@name='twitter:description']/@content").extract_first()
        item['twitterImage'] = response.xpath("//meta[@name='twitter:image']/@content").extract_first()
        item['twitterImageAlt'] = response.xpath("//meta[@name='twitter:image:alt']/@content").extract_first()
        item['twitterPlayer'] = response.xpath("//meta[@name='twitter:player']/@content").extract_first()
        item['twitterPlayerHeight'] = response.xpath("//meta[@name='twitter:player:height']/@content").extract_first()
        item['twitterPlayerWidth'] = response.xpath("//meta[@name='twitter:player:stream']/@content").extract_first()
        item['twitterPlayer'] = response.xpath("//meta[@name='twitter:player:width']/@content").extract_first()
        item['twitterSite'] = response.xpath("//meta[@name='twitter:site']/@content").extract_first()
        item['twitterSiteId'] = response.xpath("//meta[@name='twitter:site:id']/@content").extract_first()
        item['twitterTitle'] = response.xpath("//meta[@name='twitter:title']/@content").extract_first()

        yield item

    def errback_httpbin(self, failure):
        item = MetadatacheckerItem() # Creating a new Item object

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            item['httpCode'] = failure.value.response.status
            item['url'] = failure.value.response.url

        elif failure.check(DNSLookupError):
            # this is the original request
            item['url'] = failure.request
            item['httpCode'] = ('DNSLookupError on %s', item['url'])

        elif failure.check(TimeoutError, TCPTimedOutError):
            item['url'] = failure.request
            item['httpCode'] = ('TimeoutError on %s', item['url'])
        
        yield item

    def graphsParse(self, item, schemaorg):
        graphs = schemaorg.get('@graph')

        if graphs:
            grp = ''
            self.schemaParse(item, grp, schemaorg)
            ct = 1
            for graph in graphs:
                grp = f'G{ct}'
                self.schemaParse(item, grp, graph)
                ct += 1
        else:
            grp = ''
            self.schemaParse(item, grp, schemaorg)

    def schemaParse(self, item, grp, schemaorg):
        item[f'schemaorg{grp}'] = schemaorg
        item[f'schemaorgAbout{grp}'] = schemaorg.get('about')
        item[f'schemaorgAddress{grp}'] = schemaorg.get('address')
        item[f'schemaorgAlternateName{grp}'] = schemaorg.get('alternateName')
        item[f'schemaorgAuthor{grp}'] = schemaorg.get('author')
        item[f'schemaorgBreadcrumb{grp}'] = schemaorg.get('breadcrumb')
        item[f'schemaorgCaption{grp}'] = schemaorg.get('caption')
        item[f'schemaorgContactPoint{grp}'] = schemaorg.get('contactPoint')
        item[f'schemaorgContentUrl{grp}'] = schemaorg.get('contentUrl')
        item[f'schemaorgContext{grp}'] = schemaorg.get('@context')
        item[f'schemaorgDatacite{grp}'] = schemaorg.get('datacite')
        item[f'schemaorgDateModified{grp}'] = schemaorg.get('dateModified')
        item[f'schemaorgDatePublished{grp}'] = schemaorg.get('datePublished')
        item[f'schemaorgDescription{grp}'] = schemaorg.get('description')
        item[f'schemaorgGeo{grp}'] = schemaorg.get('geo')
        item[f'schemaorgHeadline{grp}'] = schemaorg.get('headline')
        item[f'schemaorgHeight{grp}'] = schemaorg.get('height')
        item[f'schemaorgId{grp}'] = schemaorg.get('@id')
        item[f'schemaorgImage{grp}'] = schemaorg.get('image')
        item[f'schemaorgInLanguage{grp}'] = schemaorg.get('inLanguage')
        item[f'schemaorgItemListElement{grp}'] = schemaorg.get('itemListElement')
        item[f'schemaorgIsPartOf{grp}'] = schemaorg.get('isPartOf')
        item[f'schemaorgLatitude{grp}'] = schemaorg.get('latitude')
        item[f'schemaorgLegalName{grp}'] = schemaorg.get('legalName')
        item[f'schemaorgLogo{grp}'] = schemaorg.get('logo')
        item[f'schemaorgLongitude{grp}'] = schemaorg.get('longitude')
        item[f'schemaorgName{grp}'] = schemaorg.get('name')
        item[f'schemaorgOpeningHoursSpecification{grp}'] = schemaorg.get('openingHoursSpecification')
        item[f'schemaorgParentOrganization{grp}'] = schemaorg.get('parentOrganization')
        item[f'schemaorgPotentialAction{grp}'] = schemaorg.get('potentialAction')
        item[f'schemaorgPrimaryImageOfPage{grp}'] = schemaorg.get('primaryImageOfPage')
        item[f'schemaorgPublisher{grp}'] = schemaorg.get('publisher')
        item[f'schemaorgSameAs{grp}'] = schemaorg.get('sameAs')
        item[f'schemaorgTelephone{grp}'] = schemaorg.get('telephone')
        item[f'schemaorgType{grp}'] = schemaorg.get('@type')
        item[f'schemaorgUrl{grp}'] = schemaorg.get('url')
        item[f'schemaorgVocab{grp}'] = schemaorg.get('@vocab')
        item[f'schemaorgWidth{grp}'] = schemaorg.get('width')
    