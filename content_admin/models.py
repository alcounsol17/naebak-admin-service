"""
نماذج إدارة المحتوى والإعدادات - خدمة الأدمن - نائبك.كوم
Content & Settings Admin Models for Naebak Admin Service
"""

from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator, RegexValidator
import uuid


class NewsTickerItem(models.Model):
    """
    عناصر الشريط الإخباري
    News Ticker Items
    """
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان الخبر",
        help_text="عنوان الخبر في الشريط الإخباري"
    )
    content = models.TextField(
        blank=True,
        verbose_name="محتوى الخبر",
        help_text="محتوى تفصيلي للخبر (اختياري)"
    )
    link = models.URLField(
        blank=True,
        verbose_name="رابط الخبر",
        help_text="رابط خارجي للخبر (اختياري)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط",
        help_text="هل الخبر نشط في الشريط؟"
    )
    priority = models.IntegerField(
        default=1,
        verbose_name="الأولوية",
        help_text="ترتيب الخبر في الشريط (1 = الأعلى)"
    )
    start_date = models.DateTimeField(
        default=timezone.now,
        verbose_name="تاريخ البداية",
        help_text="تاريخ بداية عرض الخبر"
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاريخ النهاية",
        help_text="تاريخ نهاية عرض الخبر (اختياري)"
    )
    created_by = models.CharField(
        max_length=100,
        verbose_name="أنشأ بواسطة",
        help_text="الأدمن الذي أنشأ الخبر"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "خبر الشريط الإخباري"
        verbose_name_plural = "أخبار الشريط الإخباري"
        ordering = ['priority', '-created_at']
        
    def __str__(self):
        return self.title


class SiteConfiguration(models.Model):
    """
    إعدادات الموقع العامة
    Site Configuration
    """
    site_name = models.CharField(
        max_length=100,
        default="نائبك.كوم",
        verbose_name="اسم الموقع",
        help_text="اسم الموقع"
    )
    primary_color = models.CharField(
        max_length=7,
        default="#22C55E",
        validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'يجب أن يكون لون hex صحيح')],
        verbose_name="اللون الأساسي",
        help_text="اللون الأساسي للموقع (أخضر)"
    )
    secondary_color = models.CharField(
        max_length=7,
        default="#F97316",
        validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'يجب أن يكون لون hex صحيح')],
        verbose_name="اللون الثانوي",
        help_text="اللون الثانوي للموقع (برتقالي)"
    )
    facebook_url = models.URLField(
        blank=True,
        verbose_name="رابط فيسبوك",
        help_text="رابط صفحة فيسبوك"
    )
    twitter_url = models.URLField(
        blank=True,
        verbose_name="رابط تويتر",
        help_text="رابط حساب تويتر"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "إعدادات الموقع"
        
    def __str__(self):
        return self.site_name
