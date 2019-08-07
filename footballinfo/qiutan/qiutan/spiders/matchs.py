# -*- coding: utf-8 -*-
import scrapy
import re
from qiutan.items import QiutanItem

class MatchsSpider(scrapy.Spider):
    name = 'matchs'
    allowed_domains = ['win007.com']
    # 请求头的常规配置，这里配置的是全局
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Referer': 'http://zq.win007.com/big/League/36.html'
        }
    }


    def start_requests(self):
        # 定义需要获取的赛季列表
        season_list = ['2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018', '2018-2019']

        # 遍历循环赛季列表以获取每个赛季的球队信息（version=需根据时间变化填写）
        for i in range(len(season_list)):
            base_url = 'http://zq.win007.com/jsData/matchResult/{}/s36.js?version=2018080713'
            url = base_url.format(season_list[i])
            req = scrapy.Request(url=url, callback=self.parse)
            req.headers['Referer'] = 'http://zq.win007.com/big/League/{}/36.html'.format(season_list[i])
            yield req

    def parse(self, response):
        html_str = response.body.decode('utf-8')

        pat = r"(\d+),\'\w+\',\'(\w+)\'"
        pat_match_id = r'jh\[\"R_\d+\"\] = \[(\[.*)\];'
        team_id = re.findall(pat, html_str)
        match_id = re.findall(pat_match_id, html_str)

        for i in team_id[2:]:
            item = QiutanItem()
            # 球队id
            sql_team_id = str(i[0])
            # 球队名字
            sql_team_name = str(i[1])

            base_url = 'http://zq.win007.com/jsData/teamInfo/teamDetail/tdl{}.js?version=2019042920'
            url = base_url.format(i[0])
            req = scrapy.Request(url=url, callback=self.parse_team_info)
            req.headers['Referer'] = 'http://zq.win007.com/big/team/Summary/{}.html'.format(i[0])

            item['sql_team_id'] = sql_team_id
            item['sql_team_name'] = sql_team_name
            req.meta['item'] = item
            yield req

        for i in range(len(match_id)):
            for j in eval(match_id[i].replace(',,', '')):
                item = QiutanItem()
                # 比赛id
                sql_match_id = str(j[0])
                # 比赛时间
                sql_match_time = j[3]
                # 主队id
                sql_host_id = str(j[4])
                # 客队id
                sql_guest_id = str(j[5])
                # 比赛分数
                sql_m_score = j[6]

                base_url = 'http://bf.win007.com/Count/{}cn.htm'
                url = base_url.format(j[0])
                req1 = scrapy.Request(url=url, callback=self.parse_player_info)
                req1.headers['Referer'] = 'http://live.win007.com/detail/{}cn.htm'.format(str(j[0]))
                # 传递match_id给下一个函数
                if 'match_id' not in response.meta:
                    response.meta['match_id'] = str(j[0])
                else:
                    response.meta['match_id'] = str(j[0])
                req1.meta['match_id'] = response.meta['match_id']

                item['sql_match_id'] = sql_match_id
                item['sql_match_time'] = sql_match_time
                item['sql_host_id'] = sql_host_id
                item['sql_guest_id'] = sql_guest_id
                item['sql_m_score'] = sql_m_score
                yield item
                yield req1

    def parse_team_info(self, response):
        html_str = response.body.decode('utf-8')

        pat = r"var teamDetail = \[(\d+),(\'.*\')+"
        pat1 = r"var coach = \[\[(\'.*\')+"
        pat2 = r"var teamCharacter = \[(\[.*\])+"
        # \([^)]*\) 从一个开括号到最近的闭括号。
        pat_bifen = r"var countSum = \[\[([^[]*)\]"
        team_id = re.findall(pat, html_str)
        cotch_id = re.findall(pat1, html_str)
        tedian = re.findall(pat2, html_str)
        bifen = re.findall(pat_bifen, html_str)

        for i in team_id:
            item = response.meta['item']
            # 粤语名字
            sql_y_name = i[1].split(',')[1].replace("'", '')
            # 英文名字
            sql_eng_name = i[1].split(',')[2].replace("'", '')
            # 所在城市
            sql_city = i[1].split(',')[5].replace("'", '')
            # 主场场地
            sql_host_ground = i[1].split(',')[7].replace("'", '')
            # 球队成立时间
            sql_set_time = i[1].split(',')[11].replace("'", '')
            # 球队的官网
            sql_url = i[1].split(',')[12].replace("'", '')
            # 球队的地址
            sql_address = i[1].split(',')[-1].replace("'", '')

            item['sql_y_name'] = str(sql_y_name)
            item['sql_eng_name'] = str(sql_eng_name)
            item['sql_host_ground'] = str(sql_host_ground)
            item['sql_set_time'] = str(sql_set_time)
            item['sql_url'] = str(sql_url)
            item['sql_address'] = str(sql_address)
            item['sql_city'] = sql_city

        for j in cotch_id:
            item = response.meta['item']
            # 教练名字
            item['sql_cotch'] = j.split(',')[3].replace("'", '')

        for k in tedian:
            pat3 = r"([1]),(\d+),\"(\w+)"
            pat4 = r"([2]),(\d+),\"(\w+)"
            pat5 = r"([3]),(\d+),\"(\w+)"
            tedian1 = re.findall(pat3, k)
            tedian2 = re.findall(pat4, k)
            tedian3 = re.findall(pat5, k)

            # 球队特点
            streng_list = []
            for strengths in tedian1:
                print(strengths[2])
                streng_list.append(strengths[2])
            item = response.meta['item']
            item['sql_streng'] = ','.join(streng_list)

            # 球队风格
            style_list = []
            for style in tedian3:
                print(style[2])
                style_list.append(style[2])
            item = response.meta['item']
            item['sql_style'] = ','.join(style_list)

            # 球队弱点
            weak_list = []
            for weakness in tedian2:
                print(weakness[2])
                weak_list.append(weakness[2])
            item = response.meta['item']
            item['sql_weak'] = ','.join(weak_list)

        for match_bifen in bifen:
            # 胜场
            sql_win = match_bifen.split(',')[2].replace("'", '')
            # 平场
            sql_m_ping = match_bifen.split(',')[3].replace("'", '')
            # 败场
            sql_defeat = match_bifen.split(',')[4].replace("'", '')
            # 犯规
            sql_fg = match_bifen.split(',')[5].replace("'", '')
            # 黄牌
            sql_yp = match_bifen.split(',')[6].replace("'", '')
            # 红牌
            sql_rp = match_bifen.split(',')[7].replace("'", '')
            # 控球率
            sql_kql = match_bifen.split(',')[8].replace("'", '') + '%'
            # 射正
            sql_sz = match_bifen.split(',')[9].replace("'", '') + '(' + match_bifen.split(',')[10].replace("'",
                                                                                                           '') + ')'
            # 传球
            sql_cq = match_bifen.split(',')[11].replace("'", '') + '(' + match_bifen.split(',')[12].replace("'",
                                                                                                            '') + ')'
            # 传球成功率
            sql_cqcgl = str(float(match_bifen.split(',')[13].replace("'", '')) * 100)[:2] + '%'
            # 过人次数
            sql_grcs = match_bifen.split(',')[14].replace("'", '')
            # 评分
            sql_pf = match_bifen.split(',')[-1].replace("'", '')
            # 胜率
            sql_sl = str((float(sql_defeat) / float(sql_win)) * 100)[:2] + '%'

            item = response.meta['item']
            item['sql_win'] = str(sql_win)
            item['sql_m_ping'] = str(sql_m_ping)
            item['sql_defeat'] = sql_defeat
            item['sql_fg'] = str(sql_fg)
            item['sql_yp'] = sql_yp
            item['sql_rp'] = sql_rp
            item['sql_kql'] = sql_kql
            item['sql_sz'] = sql_sz
            item['sql_cq'] = sql_cq
            item['sql_cqcgl'] = sql_cqcgl
            item['sql_grcs'] = sql_grcs
            item['sql_pf'] = sql_pf
            item['sql_sl'] = sql_sl
            yield item

    def parse_player_info(self, response):
        # 球员id
        player_id = response.xpath('//tr[@id="drs"]/td[2]/a/@href').extract()
        # 球员名字
        player_name = response.xpath('//tr[@id="drs"]/td[2]/a/text()').extract()
        # 球员位置
        player_posi = response.xpath('//tr[@id="drs"]/td[3]/text()').extract()
        # 球员射门
        player_sm = response.xpath('//tr[@id="drs"]/td[4]/text()').extract()
        # 球员射正
        player_sz = response.xpath('//tr[@id="drs"]/td[5]/text()').extract()
        # 关键传球
        player_gzcq = response.xpath('//tr[@id="drs"]/td[6]/text()').extract()
        # 带球过人
        player_dqgr = response.xpath('//tr[@id="drs"]/td[7]/text()').extract()
        # 传球次数
        player_cqcs = response.xpath('//tr[@id="drs"]/td[8]/text()').extract()
        # 传球成功
        player_cqcg = response.xpath('//tr[@id="drs"]/td[9]/text()').extract()
        # 传球成功率
        player_cqcgl = response.xpath('//tr[@id="drs"]/td[10]/text()').extract()
        # 横传次数
        player_hccs = response.xpath('//tr[@id="drs"]/td[11]/text()').extract()
        # 争顶成功
        player_zdcg = response.xpath('//tr[@id="drs"]/td[17]/text()').extract()
        # 身体接触
        player_stjc = response.xpath('//tr[@id="drs"]/td[18]/text()').extract()
        # 球员评分
        player_pf = response.xpath('//tr[@id="drs"]/td[30]/text()').extract()

        pat = 'PlayerID=(.*)&TeamID=(.*)'

        for x, y, z, a, b, c, d, e, f, g, h, i, j, k in zip(player_id, player_name, player_posi, player_sm, player_sz,
                                                            player_gzcq, player_dqgr, player_cqcs, player_cqcg,
                                                            player_cqcgl,
                                                            player_hccs, player_zdcg, player_stjc, player_pf):
            player_list = re.findall(pat, str(x))
            item = QiutanItem()
            sql_player_match_id = response.meta['match_id']
            sql_player_id = player_list[0][0]
            sql_player_team_id = player_list[0][1]
            sql_player_name = y.strip()
            sql_player_posi = z.strip()
            sql_player_sm = a.strip()
            sql_player_sz = b.strip()
            sql_player_gzcq = c.strip()
            sql_player_dqgr = d.strip()
            sql_player_cqcs = e.strip()
            sql_player_cqcg = f.strip()
            sql_player_cqcgl = g.strip()
            sql_player_hccs = h.strip()
            sql_player_zdcg = i.strip()
            sql_player_stjc = j.strip()
            sql_player_pf = k.strip()

            item['sql_player_match_id'] = sql_player_match_id
            item['sql_player_id'] = sql_player_id
            item['sql_player_team_id'] = sql_player_team_id
            item['sql_player_name'] = sql_player_name
            item['sql_player_posi'] = sql_player_posi
            item['sql_player_sm'] = sql_player_sm
            item['sql_player_sz'] = sql_player_sz
            item['sql_player_gzcq'] = sql_player_gzcq
            item['sql_player_dqgr'] = sql_player_dqgr
            item['sql_player_cqcs'] = sql_player_cqcs
            item['sql_player_cqcg'] = sql_player_cqcg
            item['sql_player_cqcgl'] = sql_player_cqcgl
            item['sql_player_hccs'] = sql_player_hccs
            item['sql_player_zdcg'] = sql_player_zdcg
            item['sql_player_stjc'] = sql_player_stjc
            item['sql_player_pf'] = sql_player_pf
            yield item
