from django.db import models

class Tree(models.Model):
    sujong = models.CharField('수종', max_length=100)
    gwa = models.CharField('과', max_length=100)
    leaf_shape_overall = models.CharField('전체적 잎 모양', max_length=50, blank=True)
    form = models.CharField('형태', max_length=100, blank=True)
    leaf_shape_detail = models.CharField('잎이 생긴 모양', max_length=100, blank=True)
    leaf_length = models.CharField('잎 길이(mm/cm)', max_length=50, blank=True)
    leaf_arrangement = models.CharField('잎이 나는 모양', max_length=50, blank=True)
    leaf_margin = models.CharField('잎가장자리', max_length=50, blank=True)
    leaf_margin_detail = models.CharField('잎가장자리 생김새', max_length=100, blank=True)
    sting_feel = models.CharField('잎에 찔렸을 때', max_length=100, blank=True)
    special_notes = models.TextField('특이사항', blank=True)
    leaf_tip = models.CharField('잎끝', max_length=100, blank=True)
    petiole = models.CharField('잎자루', max_length=100, blank=True)
    vein = models.CharField('잎맥', max_length=100, blank=True)
    height = models.CharField('키', max_length=50, blank=True)
    fruit_flower = models.TextField('열매,꽃', blank=True)

    def __str__(self):
        return self.sujong
