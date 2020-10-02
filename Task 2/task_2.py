import scrapy as scr
import json

class Web_scrappy(scr.Spider):
    name = "geek"
    ret_data = {}

    def start_requests(self):
        urls = [
            "https://www.gkseries.com/general-knowledge/geography/geo-tectonics/geography-mcqs"
        ]
        for url in urls:
            yield scr.Request(url=url, callback=self.parse)

    def parse(self, response):
        select_headr = "h1 small::text"
        print(response.css(select_headr).extract_first())
        
        select_mcq = ".mcq"
        for ques in response.css(select_mcq):
            select_ques = ".question-content.clearfix::text"
            select_opt = ".options .row div span::text"
            select_ans = ".collapse div blockquote::text "

            qs = ques.css(select_ques)[3].extract() 
            ans = ques.css(select_ans).extract_first()

            self.ret_data['Question'] = ((qs.rstrip()).replace("\r\n","")).replace("\t","")
            self.ret_data['Options'] =  ques.css(select_opt).extract()
            self.ret_data['Answer'] = (ans.split('[')[1]).split(']')[0]
            yield {
                'question': ((qs.rstrip()).replace("\r\n","")).replace("\t",""),
                'options': ques.css(select_opt).extract(),
                'answer': (ans.split('[')[1]).split(']')[0],
            }
        select_nxt = ".pagination li a::attr(href)"
        nxt_page = response.css(select_nxt)[-1].extract()
        if nxt_page:
            yield scr.Request(
                response.urljoin(nxt_page),
                callback=self.parse
            )