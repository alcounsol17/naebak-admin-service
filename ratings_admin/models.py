"""
نماذج إدارة التقييمات وعداد الزوار - خدمة الأدمن - نائبك.كوم
Ratings & Visitor Counter Admin Models for Naebak Admin Service
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class RatingConfiguration(models.Model):
    """
    إعدادات التقييمات
    Rating Configuration
    """
    representative_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="معرف النائب",
        help_text="معرف النائب في خدمة المحتوى"
    )
    representative_name = models.CharField(
        max_length=100,
        verbose_name="اسم النائب",
        help_text="اسم النائب"
    )
    default_rating = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(5.0)],
        default=4.8,
        verbose_name="التقييم الافتراضي",
        help_text="التقييم الافتراضي للنائب (1-5)"
    )
    default_voters_count = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=4000,
        verbose_name="عدد المقيمين الافتراضي",
        help_text="عدد المقيمين الافتراضي"
    )
    show_real_rating = models.BooleanField(
        default=False,
        verbose_name="إظهار التقييم الحقيقي",
        help_text="إظهار التقييم الحقيقي أم الافتراضي"
    )
    is_rating_enabled = models.BooleanField(
        default=True,
        verbose_name="تفعيل التقييم",
        help_text="هل التقييم مفعل لهذا النائب؟"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "إعدادات التقييم"
        verbose_name_plural = "إعدادات التقييمات"
        ordering = ['representative_name']
        
    def __str__(self):
        return f"تقييم {self.representative_name}"


class VisitorCounterConfiguration(models.Model):
    """
    إعدادات عداد الزوار
    Visitor Counter Configuration
    """
    min_random_visitors = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=1000,
        verbose_name="الحد الأدنى للزوار العشوائيين",
        help_text="الحد الأدنى للرقم العشوائي للزوار"
    )
    max_random_visitors = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=1500,
        verbose_name="الحد الأقصى للزوار العشوائيين",
        help_text="الحد الأقصى للرقم العشوائي للزوار"
    )
    update_interval_seconds = models.IntegerField(
        validators=[MinValueValidator(10)],
        default=30,
        verbose_name="فترة التحديث (ثانية)",
        help_text="فترة تحديث عداد الزوار بالثواني"
    )
    show_real_visitors = models.BooleanField(
        default=False,
        verbose_name="إظهار الزوار الحقيقيين",
        help_text="إظهار عدد الزوار الحقيقي أم العشوائي"
    )
    is_counter_enabled = models.BooleanField(
        default=True,
        verbose_name="تفعيل العداد",
        help_text="هل عداد الزوار مفعل؟"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "إعدادات عداد الزوار"
        verbose_name_plural = "إعدادات عداد الزوار"
        
    def __str__(self):
        return f"عداد الزوار ({self.min_random_visitors}-{self.max_random_visitors})"
