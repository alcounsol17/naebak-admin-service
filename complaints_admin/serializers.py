"""
Serializers لإدارة الشكاوى - خدمة الأدمن - نائبك.كوم
Complaints Admin Serializers for Naebak Admin Service
"""

from rest_framework import serializers
from .models import (
    ComplaintCategory, ComplaintAdminAction, ComplaintStatistics,
    ComplaintExport, ComplaintTemplate
)
from django.utils import timezone
from datetime import timedelta


class ComplaintCategorySerializer(serializers.ModelSerializer):
    """
    Serializer لتصنيفات الشكاوى
    """
    class Meta:
        model = ComplaintCategory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ComplaintAdminActionSerializer(serializers.ModelSerializer):
    """
    Serializer لإجراءات الأدمن على الشكاوى
    """
    action_type_display = serializers.CharField(source='get_action_type_display', read_only=True)
    priority_level_display = serializers.CharField(source='get_priority_level_display', read_only=True)
    
    class Meta:
        model = ComplaintAdminAction
        fields = '__all__'
        read_only_fields = ('created_at',)
        
    def validate_expected_resolution_date(self, value):
        """التحقق من تاريخ الحل المتوقع"""
        if value and value <= timezone.now():
            raise serializers.ValidationError("تاريخ الحل المتوقع يجب أن يكون في المستقبل")
        return value
        
    def validate(self, data):
        """التحقق من صحة البيانات"""
        action_type = data.get('action_type')
        
        # التحقق من وجود معرف النائب عند الإسناد
        if action_type == 'assigned':
            if not data.get('assigned_to_representative_id'):
                raise serializers.ValidationError({
                    'assigned_to_representative_id': 'معرف النائب مطلوب عند إسناد الشكوى'
                })
            if not data.get('assigned_to_representative_name'):
                raise serializers.ValidationError({
                    'assigned_to_representative_name': 'اسم النائب مطلوب عند إسناد الشكوى'
                })
                
        return data


class ComplaintStatisticsSerializer(serializers.ModelSerializer):
    """
    Serializer لإحصائيات الشكاوى
    """
    resolution_rate = serializers.SerializerMethodField()
    rejection_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplaintStatistics
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        
    def get_resolution_rate(self, obj):
        """حساب معدل الحل"""
        if obj.total_complaints > 0:
            return round((obj.resolved_complaints / obj.total_complaints) * 100, 2)
        return 0.0
        
    def get_rejection_rate(self, obj):
        """حساب معدل الرفض"""
        if obj.total_complaints > 0:
            return round((obj.rejected_complaints / obj.total_complaints) * 100, 2)
        return 0.0


class ComplaintExportSerializer(serializers.ModelSerializer):
    """
    Serializer لتصدير الشكاوى
    """
    export_format_display = serializers.CharField(source='get_export_format_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    file_size_mb = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = ComplaintExport
        fields = '__all__'
        read_only_fields = (
            'export_id', 'status', 'file_path', 'file_size', 
            'download_url', 'error_message', 'created_at', 'completed_at'
        )
        
    def validate_filter_criteria(self, value):
        """التحقق من معايير التصفية"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("معايير التصفية يجب أن تكون كائن JSON")
        return value


class ComplaintTemplateSerializer(serializers.ModelSerializer):
    """
    Serializer لقوالب الردود على الشكاوى
    """
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    
    class Meta:
        model = ComplaintTemplate
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        
    def validate_content(self, value):
        """التحقق من محتوى القالب"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("محتوى القالب يجب أن يكون على الأقل 10 أحرف")
        return value


class ComplaintSummarySerializer(serializers.Serializer):
    """
    Serializer لملخص الشكاوى من خدمة الشكاوى
    """
    complaint_id = serializers.CharField()
    citizen_name = serializers.CharField()
    citizen_phone = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()
    status = serializers.CharField()
    priority = serializers.CharField()
    category = serializers.CharField(required=False)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    attachments_count = serializers.IntegerField(default=0)
    youtube_link = serializers.URLField(required=False, allow_blank=True)
    assigned_to_representative_id = serializers.CharField(required=False, allow_blank=True)
    assigned_to_representative_name = serializers.CharField(required=False, allow_blank=True)
    resolution_text = serializers.CharField(required=False, allow_blank=True)
    resolved_at = serializers.DateTimeField(required=False, allow_null=True)


class ComplaintAssignmentSerializer(serializers.Serializer):
    """
    Serializer لإسناد الشكوى للنائب
    """
    complaint_id = serializers.CharField()
    representative_id = serializers.CharField()
    representative_name = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
    priority_level = serializers.ChoiceField(
        choices=[
            ('low', 'منخفضة'),
            ('medium', 'متوسطة'),
            ('high', 'عالية'),
            ('urgent', 'عاجلة'),
        ],
        default='medium'
    )
    expected_resolution_date = serializers.DateTimeField(required=False, allow_null=True)
    
    def validate_expected_resolution_date(self, value):
        """التحقق من تاريخ الحل المتوقع"""
        if value and value <= timezone.now():
            raise serializers.ValidationError("تاريخ الحل المتوقع يجب أن يكون في المستقبل")
        return value


class ComplaintResolutionSerializer(serializers.Serializer):
    """
    Serializer لحل الشكوى
    """
    complaint_id = serializers.CharField()
    resolution_text = serializers.CharField()
    representative_score_increase = serializers.IntegerField(default=1, min_value=0, max_value=10)
    achievement_text = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="جملة الشكر التي ستظهر في قسم الإنجازات"
    )
    notify_citizen = serializers.BooleanField(default=True)
    
    def validate_resolution_text(self, value):
        """التحقق من نص الحل"""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("نص الحل يجب أن يكون على الأقل 10 أحرف")
        return value


class ComplaintBulkActionSerializer(serializers.Serializer):
    """
    Serializer للإجراءات المجمعة على الشكاوى
    """
    complaint_ids = serializers.ListField(
        child=serializers.CharField(),
        min_length=1,
        max_length=100,
        help_text="قائمة معرفات الشكاوى"
    )
    action_type = serializers.ChoiceField(
        choices=[
            ('assign', 'إسناد'),
            ('reject', 'رفض'),
            ('archive', 'أرشفة'),
            ('change_priority', 'تغيير الأولوية'),
        ]
    )
    representative_id = serializers.CharField(required=False, allow_blank=True)
    representative_name = serializers.CharField(required=False, allow_blank=True)
    priority_level = serializers.ChoiceField(
        choices=[
            ('low', 'منخفضة'),
            ('medium', 'متوسطة'),
            ('high', 'عالية'),
            ('urgent', 'عاجلة'),
        ],
        required=False
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """التحقق من صحة البيانات"""
        action_type = data.get('action_type')
        
        # التحقق من وجود معرف النائب عند الإسناد
        if action_type == 'assign':
            if not data.get('representative_id'):
                raise serializers.ValidationError({
                    'representative_id': 'معرف النائب مطلوب عند الإسناد'
                })
            if not data.get('representative_name'):
                raise serializers.ValidationError({
                    'representative_name': 'اسم النائب مطلوب عند الإسناد'
                })
                
        # التحقق من وجود مستوى الأولوية عند تغيير الأولوية
        if action_type == 'change_priority':
            if not data.get('priority_level'):
                raise serializers.ValidationError({
                    'priority_level': 'مستوى الأولوية مطلوب عند تغيير الأولوية'
                })
                
        return data


class ComplaintFilterSerializer(serializers.Serializer):
    """
    Serializer لتصفية الشكاوى
    """
    status = serializers.ChoiceField(
        choices=[
            ('pending', 'في الانتظار'),
            ('assigned', 'مُسندة'),
            ('accepted', 'مقبولة'),
            ('rejected', 'مرفوضة'),
            ('resolved', 'محلولة'),
            ('on_hold', 'معلقة'),
        ],
        required=False
    )
    priority = serializers.ChoiceField(
        choices=[
            ('low', 'منخفضة'),
            ('medium', 'متوسطة'),
            ('high', 'عالية'),
            ('urgent', 'عاجلة'),
        ],
        required=False
    )
    representative_id = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)
    date_from = serializers.DateTimeField(required=False)
    date_to = serializers.DateTimeField(required=False)
    search = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """التحقق من صحة فترة التاريخ"""
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError({
                'date_to': 'تاريخ النهاية يجب أن يكون بعد تاريخ البداية'
            })
            
        return data
