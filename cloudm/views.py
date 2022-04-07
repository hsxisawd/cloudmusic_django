from django.shortcuts import render
from cloudm.models import Playlists
from django.http import HttpResponse
import pandas as pd
# Create your views here.
import json
import re

di=Playlists.objects.all()
list1=[]
for i in di:
    list1.append(i.toDict())
df=pd.DataFrame(list1)

"""最受欢迎的歌单类型"""



def get_hot_type(request):
    hot_type_df = df[['type', 'play_count']].groupby(df['type']).sum().sort_values('play_count',ascending=False).reset_index()
    hot_type_top7 = hot_type_df.head(7)
    playlist_type = hot_type_top7['type'].tolist()
    play_count = hot_type_top7['play_count'].tolist()

    return HttpResponse(json.dumps({'playlist_type': playlist_type, 'play_count': play_count}, ensure_ascii=False))


"""最受欢迎的歌单"""



def get_hot_playlist(request):
    hot_playlist_df = df[['name', 'play_count']].sort_values('play_count', ascending=False).reset_index()
    hot_playlist_top5 = hot_playlist_df.head(5)
    playlist_name = hot_playlist_top5['name'].tolist()
    play_count = hot_playlist_top5['play_count'].tolist()

    return HttpResponse(json.dumps({'playlist_name': playlist_name, 'play_count': play_count}, ensure_ascii=False))


"""歌单数据随月份变化"""



def get_month_data(request):
    yearList = []

    for year in ['2018', '2019']:
        yearList.append({
            "year": year,
            "data": [
                df[df['create_time'].str[:4] == year].groupby(df['create_time'].str[5:7]).sum().reset_index()[
                    'share_count'].tolist(),
                df[df['create_time'].str[:4] == year].groupby(df['create_time'].str[5:7]).sum().reset_index()[
                    'comment_count'].tolist()
            ]
        })
    month = df[df['create_time'].str[:4] == year].groupby(df['create_time'].str[5:7]).sum().reset_index()[
        'create_time'].tolist()
    yearData = {
        "yearData": yearList,
        "monthList": [str(int(x)) + '月' for x in month]
    }

    return HttpResponse(json.dumps(yearData, ensure_ascii=False))


"""歌单数据随天数变化"""



def get_day_data(request):
    non_vip_df = df[df['vip_type'] == '0'].groupby(df['create_time'].str[8:10]).sum().reset_index()[
        ['create_time', 'subscribed_count']]
    vip_df = \
    df[(df['vip_type'] == '10') | (df['vip_type'] == '11')].groupby(df['create_time'].str[8:10]).sum().reset_index()[
        ['create_time', 'subscribed_count']]
    vip_type_df = pd.merge(non_vip_df, vip_df, left_on='create_time', right_on='create_time', how='inner')

    sub_data = {
        "day": [str(int(x)) for x in vip_type_df["create_time"].tolist()],
        "vip": vip_type_df["subscribed_count_y"].tolist(),
        "nonvip": vip_type_df["subscribed_count_x"].tolist(),

    }

    return HttpResponse(json.dumps(sub_data, ensure_ascii=False))


"""歌单歌曲数量分布"""



def get_track_data(request):
    bins = [0, 50, 150, 500, 100000]
    cuts = pd.cut(df['tracks_num'], bins=bins, right=False, include_lowest=True)
    data_count = cuts.value_counts()
    data = dict(zip([str(x) for x in data_count.index.tolist()], data_count.tolist()))
    map_data = [{'name': name, 'value': value} for name, value in data.items()]
    track_value = {'t_v': map_data}

    return HttpResponse(json.dumps(track_value, ensure_ascii=False))


"""语种类型歌单播放量"""



def get_type_data(request):
    playlist_type_df = df[['type', 'play_count']].groupby(df['type']).sum()
    playlist_type_df = playlist_type_df.loc[['华语', '欧美', '日语', '韩语', '粤语'], :]
    data = dict(zip(playlist_type_df.index.tolist(), playlist_type_df['play_count'].tolist()))
    map_data = [{'name': name, 'value': value} for name, value in data.items()]
    type_sum = {'t_s': map_data}

    return HttpResponse(json.dumps(type_sum, ensure_ascii=False))


def replace_str(x):
    rep_list = ['省', '市', '维吾尔', '自治区', '壮族', '回族', '维吾尔族', '特别行政区']
    for rep in rep_list:
        x = re.sub(rep, '', x)
    return x


def add_province(df_data, province):
    # 所有年份
    years = df_data['create_time'].drop_duplicates().tolist()
    for year in years:
        # 每年的省份
        new_province = df_data.loc[df_data['create_time'] == year, :]['province'].drop_duplicates().tolist()
        # 缺失的省份 = 所有省份 - 每年的省份
        rest_province = [x for x in province if x not in new_province]
        # 对缺失的省份生成一个DataFrame，填充0值，并与原DataFrame合并
        if len(rest_province):
            rest_df = pd.DataFrame([[year, x, 0, 0] for x in rest_province], columns=df_data.columns)
            df_data = pd.concat([df_data, rest_df], ignore_index=True)

    return df_data


"""动态地图"""



def get_map_data(request):
    time_df = df.groupby([df['create_time'].str[:4], df['province'].apply(replace_str)])[
        ['play_count', 'share_count']].count().reset_index()
    re_time_df = time_df[time_df['province'] != '海外']
    province = re_time_df['province'].drop_duplicates().tolist()

    re_time_df2 = add_province(re_time_df, province)

    final_time_df = re_time_df2.sort_values(by=['create_time', 'province']).reset_index(drop=True)
    final_province = final_time_df['province'].drop_duplicates().tolist()
    final_year = final_time_df['create_time'].drop_duplicates().tolist()

    playlist_num = []
    for year in final_year:
        playlist_num.append(final_time_df.loc[final_time_df['create_time'] == year, 'play_count'].tolist())

    playlist_data = {"year": final_year, "province": final_province, "playlist_num": playlist_num}

    return HttpResponse(json.dumps(playlist_data, ensure_ascii=False))



def index(request):
    gender_df = df[['gender']].groupby(df['gender']).count()
    gender_data = {'男': gender_df.loc['男', 'gender'], '女': gender_df.loc['女', 'gender']}
    return render(request,'index.html',gender_data)



