from django.db import models

# Create your models here.
class Playlists(models.Model):

    id =models.CharField(max_length=255,default='',primary_key=True)
    name=models.CharField(max_length=255,null=True)
    type=models.CharField(max_length=255,null=True)
    tags=models.CharField(max_length=255,null=True)
    create_time=models.CharField(max_length=255,null=True)
    update_time=models.CharField(max_length=255,null=True)
    tracks_num=models.IntegerField(null=True)
    play_count=models.IntegerField(null=True)
    subscribed_count=models.IntegerField(null=True)
    share_count=models.IntegerField(null=True)
    comment_count=models.IntegerField(null=True)
    nickname=models.CharField(max_length=255,null=True)
    gender=models.CharField(max_length=255,null=True)
    user_type=models.CharField(max_length=255,null=True)
    vip_type=models.CharField(max_length=255,null=True)
    province=models.CharField(max_length=255,null=True)
    city=models.CharField(max_length=255,null=True)
    def toDict(self):
        return {"id":self.id,"name":self.name,"type":self.type,"tags":self.tags,"create_time":self.create_time,"update_time":self.update_time,
                "tracks_num":self.tracks_num,"play_count":self.play_count,"subscribed_count":self.subscribed_count,"share_count":self.share_count,
                "comment_count":self.comment_count,"nickname":self.nickname,"gender":self.gender,"user_type":self.user_type,"vip_type":self.vip_type,"province":self.province,"city":self.city,}
    class Meta:
        db_table ='playlists'