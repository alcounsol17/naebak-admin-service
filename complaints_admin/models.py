"""
نماذج إدارة الشكاوى - خدمة الأدمن - نائبك.كوم
Complaints Admin Models for Naebak Admin Service
"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxLengthValidator
import uuid


class ComplaintCategory(models.Model):
    """
    تصنيفات الشكاوى
    Complaint Categories
    """
    name = models.CharField(
        max_length=100,
        verbose_name="اسم التصنيف",
        help_text="اسم تصنيف الشكوى"
    )
    description = models.TextField(
        blank=True,
        verbose_name="الوصف",
        help_text="وصف تصنيف الشكوى"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط",
        help_text="هل التصنيف نشط؟"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "تصنيف الشكوى"
        verbose_name_plural = "تصنيفات الشكاوى"
        ordering = ['name']
        
    def __str__(self):
        return self.name


class ComplaintAdminAction(models.Model):
    """
    إجراءات الأدمن على الشكاوى
    Admin Actions on Complaints
    """
    ACTION_TYPES = [
        ('received', 'تم الاستلام'),
        ('reviewed', 'تمت المراجعة'),
        ('assigned', 'تم الإسناد'),
        ('escalated', 'تم التصعيد'),
        ('resolved', 'تم الحل'),
        ('rejected', 'تم الرفض'),
        ('archived', 'تم الأرشفة'),
        ('reopened', 'تم إعادة الفتح'),
    ]
    
    complaint_id = models.CharField(
        max_length=50,
        verbose_name="معرف الشكوى",
        help_text="معرف الشكوى في خدمة الشكاوى"
    )
    admin_id = models.CharField(
        max_length=50,
        verbose_name="معرف الأدمن",
        help_text="معرف الأدمن الذي قام بالإجراء"
    )
    admin_name = models.CharField(
        max_length=100,
        verbose_name="اسم الأدمن",
        help_text="اسم الأدمن الذي قام بالإجراء"
    )
    action_type = models.CharField(
        max_length=20,
        choices=ACTION_TYPES,
        verbose_name="نوع الإجراء",
        help_text="نوع الإجراء المتخذ"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات",
        help_text="ملاحظات الأدمن على الإجراء"
    )
    assigned_to_representative_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="معرف النائب المُسند إليه",
        help_text="معرف النائب الذي تم إسناد الشكوى إليه"
    )
    assigned_to_representative_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="اسم النائب المُسند إليه",
        help_text="اسم النائب الذي تم إسناد الشكوى إليه"
    )
    priority_level = models.CharField(
        max_length=20,
        choices=[
            ('low', 'منخفضة'),
            ('medium', 'متوسطة'),
            ('high', 'عالية'),
            ('urgent', 'عاجلة'),
        ],
        default='medium',
        verbose_name="مستوى الأولوية",
        help_text="مستوى أولوية الشكوى"
    )
    expected_resolution_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاريخ الحل المتوقع",
        help_text="التاريخ المتوقع لحل الشكوى"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإجراء")
    
    class Meta:
        verbose_name = "إجراء أدمن على الشكوى"
        verbose_name_plural = "إجراءات الأدمن على الشكاوى"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.get_action_type_display()} - {self.complaint_id}"


class ComplaintStatistics(models.Model):
    """
    إحصائيات الشكاوى
    Complaint Statistics
    """
    date = models.DateField(
        default=timezone.now,
        verbose_name="التاريخ",
        help_text="تاريخ الإحصائية"
    )
    total_complaints = models.IntegerField(
        default=0,
        verbose_name="إجمالي الشكاوى",
        help_text="إجمالي عدد الشكاوى"
    )
    new_complaints = models.IntegerField(
        default=0,
        verbose_name="الشكاوى الجديدة",
        help_text="عدد الشكاوى الجديدة"
    )
    assigned_complaints = models.IntegerField(
        default=0,
        verbose_name="الشكاوى المُسندة",
        help_text="عدد الشكاوى المُسندة للنواب"
    )
    resolved_complaints = models.IntegerField(
        default=0,
        verbose_name="الشكاوى المحلولة",
        help_text="عدد الشكاوى المحلولة"
    )
    rejected_complaints = models.IntegerField(
        default=0,
        verbose_name="الشكاوى المرفوضة",
        help_text="عدد الشكاوى المرفوضة"
    )
    pending_complaints = models.IntegerField(
        default=0,
        verbose_name="الشكاوى المعلقة",
        help_text="عدد الشكاوى المعلقة"
    )
    average_resolution_time = models.FloatField(
        default=0.0,
        verbose_name="متوسط وقت الحل (بالأيام)",
        help_text="متوسط الوقت المطلوب لحل الشكوى"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "إحصائية الشكاوى"
        verbose_name_plural = "إحصائيات الشكاوى"
        ordering = ['-date']
        unique_together = ['date']
        
    def __str__(self):
        return f"إحصائيات {self.date}"


class ComplaintExport(models.Model):
    """
    تصدير الشكاوى
    Complaint Exports
    """
    EXPORT_FORMATS = [
        ('zip', 'ملف مضغوط (ZIP)'),
        ('excel', 'ملف إكسل (XLSX)'),
        ('pdf', 'ملف PDF'),
        ('csv', 'ملف CSV'),
    ]
    
    EXPORT_STATUS = [
        ('pending', 'في الانتظار'),
        ('processing', 'جاري المعالجة'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
    ]
    
    export_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        verbose_name="معرف التصدير",
        help_text="معرف فريد لعملية التصدير"
    )
    admin_id = models.CharField(
        max_length=50,
        verbose_name="معرف الأدمن",
        help_text="معرف الأدمن الذي طلب التصدير"
    )
    admin_name = models.CharField(
        max_length=100,
        verbose_name="اسم الأدمن",
        help_text="اسم الأدمن الذي طلب التصدير"
    )
    export_format = models.CharField(
        max_length=10,
        choices=EXPORT_FORMATS,
        default='zip',
        verbose_name="صيغة التصدير",
        help_text="صيغة ملف التصدير"
    )
    status = models.CharField(
        max_length=20,
        choices=EXPORT_STATUS,
        default='pending',
        verbose_name="حالة التصدير",
        help_text="حالة عملية التصدير"
    )
    filter_criteria = models.JSONField(
        default=dict,
        verbose_name="معايير التصفية",
        help_text="معايير تصفية الشكاوى للتصدير"
    )
    total_complaints = models.IntegerField(
        default=0,
        verbose_name="عدد الشكاوى",
        help_text="عدد الشكاوى المُصدرة"
    )
    file_path = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="مسار الملف",
        help_text="مسار ملف التصدير"
    )
    file_size = models.BigIntegerField(
        default=0,
        verbose_name="حجم الملف (بايت)",
        help_text="حجم ملف التصدير بالبايت"
    )
    download_url = models.URLField(
        blank=True,
        verbose_name="رابط التحميل",
        help_text="رابط تحميل ملف التصدير"
    )
    expires_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاريخ انتهاء الصلاحية",
        help_text="تاريخ انتهاء صلاحية رابط التحميل"
    )
    error_message = models.TextField(
        blank=True,
        verbose_name="رسالة الخطأ",
        help_text="رسالة الخطأ في حالة فشل التصدير"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    completed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="تاريخ الإكمال",
        help_text="تاريخ إكمال التصدير"
    )
    
    class Meta:
        verbose_name = "تصدير الشكاوى"
        verbose_name_plural = "تصديرات الشكاوى"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"تصدير {self.export_id} - {self.get_status_display()}"
        
    @property
    def is_expired(self):
        """التحقق من انتهاء صلاحية التصدير"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
        
    @property
    def file_size_mb(self):
        """حجم الملف بالميجابايت"""
        return round(self.file_size / (1024 * 1024), 2) if self.file_size else 0


class ComplaintTemplate(models.Model):
    """
    قوالب الردود على الشكاوى
    Complaint Response Templates
    """
    TEMPLATE_TYPES = [
        ('acknowledgment', 'إقرار الاستلام'),
        ('assignment', 'إشعار الإسناد'),
        ('resolution', 'إشعار الحل'),
        ('rejection', 'إشعار الرفض'),
        ('follow_up', 'متابعة'),
        ('closure', 'إغلاق الشكوى'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name="اسم القالب",
        help_text="اسم قالب الرد"
    )
    template_type = models.CharField(
        max_length=20,
        choices=TEMPLATE_TYPES,
        verbose_name="نوع القالب",
        help_text="نوع قالب الرد"
    )
    subject = models.CharField(
        max_length=200,
        verbose_name="موضوع الرسالة",
        help_text="موضوع رسالة الرد"
    )
    content = models.TextField(
        verbose_name="محتوى القالب",
        help_text="محتوى قالب الرد (يمكن استخدام متغيرات مثل {citizen_name})"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط",
        help_text="هل القالب نشط؟"
    )
    created_by = models.CharField(
        max_length=100,
        verbose_name="أنشأ بواسطة",
        help_text="الأدمن الذي أنشأ القالب"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")
    
    class Meta:
        verbose_name = "قالب الرد"
        verbose_name_plural = "قوالب الردود"
        ordering = ['template_type', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
        
    def render_content(self, context):
        """تطبيق المتغيرات على محتوى القالب"""
        content = self.content
        for key, value in context.items():
            content = content.replace(f"{{{key}}}", str(value))
        return content
