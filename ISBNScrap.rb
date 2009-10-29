#!/usr/bin/env ruby

#
# ISBN screen scrapping
# shows how to use Hpricot to
# scrap book info from two sellers.
# Hpricot uses XPath notation to get to
# (x)HTML elements, so we may not 
# rely only on regexps 
# we're after book title, author name, price and a synopsis if avaliable.
# 2007-10-28
# updated code. original at: http://zenmachine.wordpress.com/scraping-with-hpricot-and-ruby/

require 'rubygems'
require 'open-uri'
require 'hpricot'

class ISBNScrap 
	def initialize (isbn)
		@urlAmazon="http://www.amazon.com/s/&url=search-alias=stripbooks?field-keywords=#{isbn}"
		@urlBamm="http://www.booksamillion.com/ncom/books?id=3935697140159&isbn=#{isbn}"
		@amazonInfoLabels=%w['price', 'pages', 'publisher', 'language', 'isbn-10', 'isbn-15', 'rank', 'review']
	end
	
	def searchAmazon
		begin
			doc = Hpricot(open(@urlAmazon))
			# firebug's XPath: /html/body/div[2]/form/table[3]/tbody/tr/td/div/table/tbody/tr[2]/td[2]/b
			# changed class to : b class="priceLarge"
			price=(doc/"table.product//tr//td/b.priceLarge").inner_html
			puts "Price: "+price if (not price.nil?)
			
			buckets=(doc/"table//td.bucket//li").each { |bucket|
				# title
				info=bucket.at("b").inner_html
				if @amazonInfoLabels.include?(info.downcase)
					puts info
					# some cleaning up: removes <b> and <a> tags
					# we just need the text
					(bucket/"b").remove
					(bucket/"a").remove
					puts bucket.inner_html
				end
			}
		rescue
			puts "Err: "+$!
			puts "Trace:"
			$@.each {|tl| 	puts tl }
		end
	end
	def searchBamm
		# as an exercise, try to implement a scrapper for books-a-million data.
	end
end



#isbn = '0451167716' if ARGV[0].nil? # defaults to my book
isbn = '0131103628' if ARGV[0].nil? # defaults to the real programming bible ;) (I got humble)
isbnScrap = ISBNScrap.new(isbn)

isbnScrap.searchAmazon
