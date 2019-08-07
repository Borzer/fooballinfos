# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiutanItem(scrapy.Item):
    sql_team_id = scrapy.Field()
    sql_team_name = scrapy.Field()
    sql_city = scrapy.Field()
    sql_y_name = scrapy.Field()
    sql_eng_name = scrapy.Field()
    sql_host_ground = scrapy.Field()
    sql_set_time = scrapy.Field()
    sql_url = scrapy.Field()
    sql_address = scrapy.Field()
    sql_cotch = scrapy.Field()
    sql_streng = scrapy.Field()
    sql_style = scrapy.Field()
    sql_weak = scrapy.Field()

    sql_win = scrapy.Field()
    sql_m_ping = scrapy.Field()
    sql_defeat = scrapy.Field()
    sql_fg = scrapy.Field()
    sql_yp = scrapy.Field()
    sql_rp = scrapy.Field()
    sql_kql = scrapy.Field()
    sql_sz = scrapy.Field()
    sql_cq = scrapy.Field()
    sql_cqcgl = scrapy.Field()
    sql_grcs = scrapy.Field()
    sql_pf = scrapy.Field()
    sql_sl = scrapy.Field()

    sql_match_id = scrapy.Field()
    sql_match_time = scrapy.Field()
    sql_host_id = scrapy.Field()
    sql_guest_id = scrapy.Field()
    sql_m_score = scrapy.Field()

    sql_player_pf = scrapy.Field()
    sql_player_match_id = scrapy.Field()
    sql_player_id = scrapy.Field()
    sql_player_team_id = scrapy.Field()
    sql_player_name = scrapy.Field()
    sql_player_posi = scrapy.Field()
    sql_player_sm = scrapy.Field()
    sql_player_sz = scrapy.Field()
    sql_player_gzcq = scrapy.Field()
    sql_player_dqgr = scrapy.Field()
    sql_player_cqcs = scrapy.Field()
    sql_player_cqcg = scrapy.Field()
    sql_player_cqcgl = scrapy.Field()
    sql_player_hccs = scrapy.Field()
    sql_player_zdcg = scrapy.Field()
    sql_player_stjc = scrapy.Field()


    # 构建不同的item入库函数以便pipelines能区别出来
    def get_item1(self):
        insert_sql = 'INSERT INTO team_info(team_id,team_name,city,y_name,eng_name,url,host_ground,set_time,address,cotch,strengths,style,weakness) values ' \
                     '(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        params = (
            self['sql_team_id'], self['sql_team_name'], self['sql_city'], self['sql_y_name'], self['sql_eng_name'],
            self['sql_url'],
            self['sql_host_ground'], self['sql_set_time'], self['sql_address'], self['sql_cotch'], self['sql_streng'],
            self['sql_style'], self['sql_weak'])
        return insert_sql, params

    def get_item2(self):
        insert_sql = 'INSERT INTO match_info(team_id,team_name,win,ping,dfeat,sl,fg,yp,rp,kql,sz,cq,cqcgl,grcs,pf) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        data = (self['sql_team_id'],self['sql_team_name'],self['sql_win'],self['sql_m_ping'],self['sql_defeat'],self['sql_sl'],self['sql_fg'],self['sql_yp'],self['sql_rp'],self['sql_kql'],self['sql_sz'],self['sql_cq'],self['sql_cqcgl'],self['sql_grcs'],self['sql_pf'])
        return insert_sql, data

    def get_item3(self):
        insert_sql = 'INSERT INTO match_score(match_id,match_time,host_id,guest_id,m_score) values(%s,%s,%s,%s,%s)'
        match_data = (self['sql_match_id'],self['sql_match_time'],self['sql_host_id'],self['sql_guest_id'],self['sql_m_score'])
        return insert_sql,match_data

    def get_item4(self):
        insert_sql = 'INSERT INTO player_info(match_id,player_id,team_id,name,posi,sm,sz,gzcq,dqgr,cqcs,cqcg,cqcgl,hccs,zdcg,stjc,pf) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        player_data = (self['sql_player_match_id'],self['sql_player_id'],self['sql_player_team_id'],self['sql_player_name'],self['sql_player_posi'],self['sql_player_sm'],self['sql_player_sz'],self['sql_player_gzcq'],self['sql_player_dqgr'],self['sql_player_cqcs'],self['sql_player_cqcg'],self['sql_player_cqcgl'],self['sql_player_hccs'],self['sql_player_zdcg'],self['sql_player_stjc'],self['sql_player_pf'])
        return insert_sql,player_data
