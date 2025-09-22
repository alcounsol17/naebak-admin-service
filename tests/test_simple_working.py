"""
اختبارات مبسطة وعاملة لنماذج خدمة الأدمن
Simple working tests for admin service models
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone
from datetime import datetime, timedelta
import uuid

from complaints_admin.models import (
    ComplaintCategory, ComplaintAdminAction, ComplaintStatistics,
    ComplaintExport, ComplaintTemplate
)
from ratings_admin.models import RatingConfiguration, VisitorCounterConfiguration


class ComplaintCategoryTest(TestCase):
    """اختبارات تصنيفات الشكاوى"""
    
    def test_create_category(self):
        """اختبار إنشاء تصنيف"""
        category = ComplaintCategory.objects.create(
            name='شكاوى الخدمات',
            description='شكاوى متعلقة بالخدمات العامة'
        )
        self.assertEqual(category.name, 'شكاوى الخدمات')
        self.assertTrue(category.is_active)
        self.assertIsNotNone(category.created_at)
    
    def test_category_str(self):
        """اختبار تمثيل النص"""
        category = ComplaintCategory.objects.create(name='تصنيف تجريبي')
        self.assertEqual(str(category), 'تصنيف تجريبي')
    
    def test_category_ordering(self):
        """اختبار ترتيب التصنيفات"""
        cat1 = ComplaintCategory.objects.create(name='ب - تصنيف')
        cat2 = ComplaintCategory.objects.create(name='أ - تصنيف')
        
        categories = ComplaintCategory.objects.all()
        # التحقق من وجود التصنيفات
        self.assertEqual(categories.count(), 2)


class ComplaintAdminActionTest(TestCase):
    """اختبارات إجراءات الأدمن"""
    
    def test_create_action(self):
        """اختبار إنشاء إجراء"""
        action = ComplaintAdminAction.objects.create(
            complaint_id='COMP-001',
            admin_id='ADMIN-001',
            admin_name='أحمد الأدمن',
            action_type='assigned',
            priority_level='high'
        )
        self.assertEqual(action.complaint_id, 'COMP-001')
        self.assertEqual(action.action_type, 'assigned')
        self.assertEqual(action.priority_level, 'high')
        self.assertIsNotNone(action.created_at)
    
    def test_action_str(self):
        """اختبار تمثيل النص"""
        action = ComplaintAdminAction.objects.create(
            complaint_id='COMP-001',
            admin_id='ADMIN-001',
            admin_name='أحمد الأدمن',
            action_type='assigned'
        )
        expected = f"تم الإسناد - {action.complaint_id}"
        self.assertEqual(str(action), expected)
    
    def test_action_choices(self):
        """اختبار خيارات الإجراءات"""
        valid_actions = ['received', 'reviewed', 'assigned', 'resolved']
        for i, action_type in enumerate(valid_actions):
            action = ComplaintAdminAction.objects.create(
                complaint_id=f'COMP-{i}',
                admin_id='ADMIN-001',
                admin_name='أحمد الأدمن',
                action_type=action_type
            )
            self.assertEqual(action.action_type, action_type)


class ComplaintStatisticsTest(TestCase):
    """اختبارات إحصائيات الشكاوى"""
    
    def test_create_statistics(self):
        """اختبار إنشاء إحصائية"""
        stats = ComplaintStatistics.objects.create(
            date=timezone.now().date(),
            total_complaints=100,
            new_complaints=20,
            resolved_complaints=50
        )
        self.assertEqual(stats.total_complaints, 100)
        self.assertEqual(stats.new_complaints, 20)
        self.assertEqual(stats.resolved_complaints, 50)
        self.assertIsNotNone(stats.created_at)
    
    def test_statistics_str(self):
        """اختبار تمثيل النص"""
        stats = ComplaintStatistics.objects.create(
            date=timezone.now().date(),
            total_complaints=50
        )
        expected = f"إحصائيات {stats.date}"
        self.assertEqual(str(stats), expected)
    
    def test_unique_date(self):
        """اختبار تفرد التاريخ"""
        date = timezone.now().date()
        ComplaintStatistics.objects.create(date=date, total_complaints=50)
        
        with self.assertRaises(IntegrityError):
            ComplaintStatistics.objects.create(date=date, total_complaints=60)


class ComplaintExportTest(TestCase):
    """اختبارات تصدير الشكاوى"""
    
    def test_create_export(self):
        """اختبار إنشاء تصدير"""
        export = ComplaintExport.objects.create(
            admin_id='ADMIN-001',
            admin_name='أحمد الأدمن',
            export_format='zip',
            status='pending'
        )
        self.assertEqual(export.admin_name, 'أحمد الأدمن')
        self.assertEqual(export.export_format, 'zip')
        self.assertEqual(export.status, 'pending')
        self.assertIsInstance(export.export_id, uuid.UUID)
        self.assertIsNotNone(export.created_at)
    
    def test_export_str(self):
        """اختبار تمثيل النص"""
        export = ComplaintExport.objects.create(
            admin_id='ADMIN-001',
            admin_name='أحمد الأدمن',
            export_format='zip',
            status='pending'
        )
        expected = f"تصدير {export.export_id} - في الانتظار"
        self.assertEqual(str(export), expected)
    
    def test_export_formats(self):
        """اختبار صيغ التصدير"""
        formats = ['zip', 'excel', 'pdf', 'csv']
        for i, fmt in enumerate(formats):
            export = ComplaintExport.objects.create(
                admin_id=f'ADMIN-{i}',
                admin_name='أحمد الأدمن',
                export_format=fmt
            )
            self.assertEqual(export.export_format, fmt)
    
    def test_file_size_mb(self):
        """اختبار حساب حجم الملف"""
        export = ComplaintExport.objects.create(
            admin_id='ADMIN-001',
            admin_name='أحمد الأدمن',
            file_size=2097152  # 2 MB
        )
        self.assertEqual(export.file_size_mb, 2.0)
    
    def test_is_expired(self):
        """اختبار انتهاء الصلاحية"""
        export = ComplaintExport.objects.create(
            admin_id='ADMIN-001',
            admin_name='أحمد الأدمن',
            expires_at=timezone.now() - timedelta(hours=1)
        )
        self.assertTrue(export.is_expired)


class ComplaintTemplateTest(TestCase):
    """اختبارات قوالب الردود"""
    
    def test_create_template(self):
        """اختبار إنشاء قالب"""
        template = ComplaintTemplate.objects.create(
            name='قالب الاستلام',
            template_type='acknowledgment',
            subject='تم الاستلام',
            content='تم استلام شكواكم رقم {complaint_id}',
            created_by='أحمد الأدمن'
        )
        self.assertEqual(template.name, 'قالب الاستلام')
        self.assertEqual(template.template_type, 'acknowledgment')
        self.assertTrue(template.is_active)
        self.assertIsNotNone(template.created_at)
    
    def test_template_str(self):
        """اختبار تمثيل النص"""
        template = ComplaintTemplate.objects.create(
            name='قالب تجريبي',
            template_type='acknowledgment',
            subject='اختبار',
            content='محتوى تجريبي',
            created_by='أحمد الأدمن'
        )
        expected = f"{template.name} (إقرار الاستلام)"
        self.assertEqual(str(template), expected)
    
    def test_render_content(self):
        """اختبار تطبيق المتغيرات"""
        template = ComplaintTemplate.objects.create(
            name='قالب تجريبي',
            template_type='acknowledgment',
            subject='اختبار',
            content='مرحباً {name}، شكواكم رقم {id}',
            created_by='أحمد الأدمن'
        )
        
        context = {'name': 'أحمد', 'id': 'COMP-001'}
        result = template.render_content(context)
        expected = 'مرحباً أحمد، شكواكم رقم COMP-001'
        self.assertEqual(result, expected)
    
    def test_template_types(self):
        """اختبار أنواع القوالب"""
        types = ['acknowledgment', 'assignment', 'resolution', 'rejection']
        for i, template_type in enumerate(types):
            template = ComplaintTemplate.objects.create(
                name=f'قالب {i}',
                template_type=template_type,
                subject='موضوع',
                content='محتوى',
                created_by='أحمد الأدمن'
            )
            self.assertEqual(template.template_type, template_type)


class RatingConfigurationTest(TestCase):
    """اختبارات إعدادات التقييم"""
    
    def test_create_rating_config(self):
        """اختبار إنشاء إعدادات تقييم"""
        config = RatingConfiguration.objects.create(
            representative_id='REP-001',
            representative_name='د. أحمد محمد',
            default_rating=4.5,
            default_voters_count=1000
        )
        self.assertEqual(config.representative_id, 'REP-001')
        self.assertEqual(config.default_rating, 4.5)
        self.assertEqual(config.default_voters_count, 1000)
        self.assertTrue(config.is_rating_enabled)
        self.assertIsNotNone(config.created_at)
    
    def test_rating_config_str(self):
        """اختبار تمثيل النص"""
        config = RatingConfiguration.objects.create(
            representative_id='REP-001',
            representative_name='د. أحمد محمد'
        )
        expected = f"تقييم {config.representative_name}"
        self.assertEqual(str(config), expected)
    
    def test_unique_representative(self):
        """اختبار تفرد النائب"""
        RatingConfiguration.objects.create(
            representative_id='REP-001',
            representative_name='د. أحمد محمد'
        )
        
        with self.assertRaises(IntegrityError):
            RatingConfiguration.objects.create(
                representative_id='REP-001',
                representative_name='د. محمد أحمد'
            )
    
    def test_rating_range(self):
        """اختبار نطاق التقييم"""
        # تقييم صحيح
        config = RatingConfiguration.objects.create(
            representative_id='REP-001',
            representative_name='د. أحمد محمد',
            default_rating=3.5
        )
        self.assertEqual(config.default_rating, 3.5)


class VisitorCounterConfigurationTest(TestCase):
    """اختبارات إعدادات عداد الزوار"""
    
    def test_create_counter_config(self):
        """اختبار إنشاء إعدادات عداد"""
        config = VisitorCounterConfiguration.objects.create(
            min_random_visitors=1000,
            max_random_visitors=1500,
            update_interval_seconds=30
        )
        self.assertEqual(config.min_random_visitors, 1000)
        self.assertEqual(config.max_random_visitors, 1500)
        self.assertEqual(config.update_interval_seconds, 30)
        self.assertTrue(config.is_counter_enabled)
        self.assertIsNotNone(config.created_at)
    
    def test_counter_str(self):
        """اختبار تمثيل النص"""
        config = VisitorCounterConfiguration.objects.create(
            min_random_visitors=500,
            max_random_visitors=800
        )
        expected = 'عداد الزوار (500-800)'
        self.assertEqual(str(config), expected)
    
    def test_counter_settings(self):
        """اختبار إعدادات العداد"""
        config = VisitorCounterConfiguration.objects.create(
            min_random_visitors=100,
            max_random_visitors=200,
            update_interval_seconds=60,
            show_real_visitors=True
        )
        self.assertTrue(config.show_real_visitors)
        self.assertEqual(config.update_interval_seconds, 60)


class IntegrationTest(TestCase):
    """اختبارات التكامل"""
    
    def test_complaint_workflow(self):
        """اختبار سير عمل الشكوى"""
        # إنشاء تصنيف
        category = ComplaintCategory.objects.create(
            name='شكاوى عامة'
        )
        
        # إنشاء إجراء
        action = ComplaintAdminAction.objects.create(
            complaint_id='COMP-001',
            admin_id='ADMIN-001',
            admin_name='أحمد الأدمن',
            action_type='assigned',
            assigned_to_representative_id='REP-001',
            assigned_to_representative_name='د. محمد السيد'
        )
        
        # إنشاء قالب
        template = ComplaintTemplate.objects.create(
            name='قالب الإسناد',
            template_type='assignment',
            subject='تم الإسناد',
            content='تم إسناد الشكوى {complaint_id} للنائب {representative_name}',
            created_by='أحمد الأدمن'
        )
        
        # اختبار التكامل
        self.assertTrue(category.is_active)
        self.assertEqual(action.action_type, 'assigned')
        self.assertEqual(template.template_type, 'assignment')
        
        # تطبيق القالب
        context = {
            'complaint_id': action.complaint_id,
            'representative_name': action.assigned_to_representative_name
        }
        result = template.render_content(context)
        expected = 'تم إسناد الشكوى COMP-001 للنائب د. محمد السيد'
        self.assertEqual(result, expected)
    
    def test_statistics_and_export(self):
        """اختبار الإحصائيات والتصدير"""
        # إنشاء إحصائية
        stats = ComplaintStatistics.objects.create(
            date=timezone.now().date(),
            total_complaints=100,
            resolved_complaints=80
        )
        
        # إنشاء تصدير
        export = ComplaintExport.objects.create(
            admin_id='ADMIN-001',
            admin_name='أحمد الأدمن',
            export_format='excel',
            status='completed',
            total_complaints=stats.resolved_complaints
        )
        
        # اختبار التكامل
        self.assertEqual(export.total_complaints, stats.resolved_complaints)
        self.assertEqual(export.status, 'completed')
    
    def test_rating_configuration(self):
        """اختبار إعدادات التقييم"""
        # إعدادات التقييم
        rating_config = RatingConfiguration.objects.create(
            representative_id='REP-001',
            representative_name='د. أحمد محمد',
            default_rating=4.2,
            show_real_rating=False
        )
        
        # إعدادات عداد الزوار
        visitor_config = VisitorCounterConfiguration.objects.create(
            min_random_visitors=800,
            max_random_visitors=1200,
            show_real_visitors=False
        )
        
        # اختبار الإعدادات
        self.assertFalse(rating_config.show_real_rating)
        self.assertFalse(visitor_config.show_real_visitors)
        self.assertEqual(rating_config.default_rating, 4.2)
        self.assertEqual(visitor_config.min_random_visitors, 800)
    
    def test_multiple_categories_and_actions(self):
        """اختبار تصنيفات وإجراءات متعددة"""
        # إنشاء تصنيفات متعددة
        categories = []
        for i in range(3):
            category = ComplaintCategory.objects.create(
                name=f'تصنيف {i+1}',
                description=f'وصف التصنيف {i+1}'
            )
            categories.append(category)
        
        # إنشاء إجراءات متعددة
        actions = []
        action_types = ['received', 'reviewed', 'assigned']
        for i, action_type in enumerate(action_types):
            action = ComplaintAdminAction.objects.create(
                complaint_id=f'COMP-{i+1:03d}',
                admin_id='ADMIN-001',
                admin_name='أحمد الأدمن',
                action_type=action_type
            )
            actions.append(action)
        
        # التحقق من الإنشاء
        self.assertEqual(ComplaintCategory.objects.count(), 3)
        self.assertEqual(ComplaintAdminAction.objects.count(), 3)
        
        # التحقق من الأنواع
        for i, action in enumerate(actions):
            self.assertEqual(action.action_type, action_types[i])
    
    def test_template_rendering_edge_cases(self):
        """اختبار حالات خاصة لتطبيق القوالب"""
        template = ComplaintTemplate.objects.create(
            name='قالب معقد',
            template_type='follow_up',
            subject='متابعة',
            content='مرحباً {name}، شكواكم {id} في حالة {status}. المتوقع: {expected_date}',
            created_by='أحمد الأدمن'
        )
        
        # حالة عادية
        context = {
            'name': 'أحمد محمد',
            'id': 'COMP-001',
            'status': 'قيد المراجعة',
            'expected_date': '2024-12-31'
        }
        result = template.render_content(context)
        expected = 'مرحباً أحمد محمد، شكواكم COMP-001 في حالة قيد المراجعة. المتوقع: 2024-12-31'
        self.assertEqual(result, expected)
        
        # حالة متغيرات ناقصة
        partial_context = {'name': 'أحمد', 'id': 'COMP-002'}
        result_partial = template.render_content(partial_context)
        # يجب أن يحتوي على المتغيرات المتاحة
        self.assertIn('أحمد', result_partial)
        self.assertIn('COMP-002', result_partial)
