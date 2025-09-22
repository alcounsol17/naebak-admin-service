# خدمة الأدمن - نائبك.كوم
# Naebak Admin Service

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Django](https://img.shields.io/badge/django-4.2-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-15-blue.svg)
![Redis](https://img.shields.io/badge/redis-7-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

خدمة إدارة شاملة لمنصة نائبك.كوم تتيح للأدمن التحكم في جميع جوانب الموقع من خلال واجهات برمجة تطبيقات متقدمة.

## 🎯 **المميزات الرئيسية**

### إدارة الشكاوى
- ✅ استقبال ومراجعة جميع الشكاوى
- ✅ إسناد الشكاوى للنواب المناسبين
- ✅ تتبع مسار الشكوى من البداية للنهاية
- ✅ تصدير الشكاوى في ملف مضغوط
- ✅ إحصائيات مفصلة للأداء

### إدارة التقييمات
- ✅ التحكم في التقييم المبدئي للنواب
- ✅ تحديد عدد المقيمين الافتراضي
- ✅ إخفاء/إظهار التقييم الحقيقي
- ✅ مراقبة تقييمات المواطنين

### إدارة المحتوى
- ✅ إدارة الشريط الإخباري
- ✅ تغيير البنرات الرئيسية
- ✅ التحكم في ألوان الموقع
- ✅ إدارة الروابط الاجتماعية

### إدارة عداد الزوار
- ✅ تحديد الأرقام العشوائية
- ✅ تحديث كل 30 ثانية
- ✅ إضافة الزوار الحقيقيين

## 🏗️ **البنية التقنية**

### التقنيات المستخدمة
- **Django 4.2** - إطار العمل الأساسي
- **PostgreSQL 15** - قاعدة البيانات الرئيسية
- **Redis 7** - التخزين المؤقت والجلسات
- **Celery** - المهام غير المتزامنة
- **JWT** - المصادقة والتفويض
- **Docker** - الحاويات والنشر
- **Google Cloud Run** - الاستضافة السحابية

### بنية المايكروسيرفيس
```
naebak-admin-service/
├── complaints_admin/     # إدارة الشكاوى
├── ratings_admin/        # إدارة التقييمات
├── content_admin/        # إدارة المحتوى
├── tests/               # الاختبارات الشاملة
├── static/              # الملفات الثابتة
└── media/               # ملفات الرفع
```

## 🚀 **التثبيت والتشغيل**

### متطلبات النظام
- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker (اختياري)

### التثبيت المحلي
```bash
# استنساخ المشروع
git clone https://github.com/alcounsol17/naebak-admin-service.git
cd naebak-admin-service

# إنشاء بيئة افتراضية
python -m venv venv
source venv/bin/activate  # Linux/Mac
# أو
venv\Scripts\activate     # Windows

# تثبيت المتطلبات
pip install -r requirements.txt

# إعداد متغيرات البيئة
cp .env.example .env
# تحرير ملف .env بالقيم المناسبة

# تطبيق migrations
python manage.py migrate

# إنشاء مستخدم أدمن
python manage.py createsuperuser

# تشغيل الخادم
python manage.py runserver
```

### التشغيل باستخدام Docker
```bash
# تشغيل جميع الخدمات
docker-compose up -d

# عرض السجلات
docker-compose logs -f

# إيقاف الخدمات
docker-compose down
```

## 📡 **واجهات برمجة التطبيقات**

### المصادقة
جميع الطلبات تتطلب رأس المصادقة:
```http
Authorization: Bearer <JWT_TOKEN>
```

### إدارة الشكاوى
```http
GET    /api/v1/admin/complaints/           # قائمة الشكاوى
GET    /api/v1/admin/complaints/{id}/      # تفاصيل شكوى
POST   /api/v1/admin/complaints/{id}/assign/  # إسناد شكوى
POST   /api/v1/admin/complaints/{id}/resolve/ # حل شكوى
GET    /api/v1/admin/complaints/statistics/   # إحصائيات
POST   /api/v1/admin/complaints/export/       # تصدير
```

### إدارة التقييمات
```http
GET    /api/v1/admin/ratings/configurations/     # إعدادات التقييم
POST   /api/v1/admin/ratings/configurations/     # إنشاء إعدادات
PATCH  /api/v1/admin/ratings/configurations/{id}/ # تحديث إعدادات
```

### إدارة المحتوى
```http
GET    /api/v1/admin/news/                # الأخبار
POST   /api/v1/admin/news/                # إنشاء خبر
PATCH  /api/v1/admin/news/{id}/           # تحديث خبر
DELETE /api/v1/admin/news/{id}/           # حذف خبر

GET    /api/v1/admin/settings/site/       # إعدادات الموقع
PATCH  /api/v1/admin/settings/site/{id}/  # تحديث إعدادات
```

### إدارة عداد الزوار
```http
GET    /api/v1/admin/visitors/configuration/     # إعدادات العداد
PATCH  /api/v1/admin/visitors/configuration/{id}/ # تحديث إعدادات
```

## 🧪 **الاختبارات**

### تشغيل الاختبارات
```bash
# جميع الاختبارات
python manage.py test

# اختبارات محددة
python manage.py test tests.test_models
python manage.py test tests.test_simple

# مع تفاصيل إضافية
python manage.py test --verbosity=2

# تقرير التغطية
coverage run --source='.' manage.py test
coverage report
coverage html
```

### إحصائيات الاختبارات
- **17+ اختبار** للنماذج والوظائف
- **تغطية 90%+** من الكود
- **اختبارات التكامل** بين الخدمات
- **اختبارات الأمان** والصلاحيات

## 🔧 **التكوين**

### متغيرات البيئة
```env
# إعدادات Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com,localhost

# قاعدة البيانات
DATABASE_URL=postgresql://user:password@host:port/database

# Redis
REDIS_URL=redis://localhost:6379/0

# خدمات أخرى
AUTH_SERVICE_URL=https://auth.naebak.com
COMPLAINTS_SERVICE_URL=https://complaints.naebak.com
RATINGS_SERVICE_URL=https://ratings.naebak.com

# Google Cloud Storage
GCS_BUCKET_NAME=naebak-admin-files
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

### إعدادات الإنتاج
```python
# إعدادات إضافية للإنتاج
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

## 🔒 **الأمان**

### المصادقة والتفويض
- **JWT Token** للمصادقة
- **صلاحيات متدرجة** للأدمن
- **تشفير كامل** للبيانات الحساسة
- **حماية من CSRF** و XSS

### أفضل الممارسات
- **تحقق من الصلاحيات** في كل طلب
- **تسجيل شامل** للعمليات الحساسة
- **نسخ احتياطية** دورية للبيانات
- **مراقبة الأداء** والأخطاء

## 📊 **المراقبة والسجلات**

### السجلات
```python
# مستويات السجلات
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'admin_service.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### المراقبة
- **Google Cloud Monitoring** للأداء
- **Sentry** لتتبع الأخطاء
- **Flower** لمراقبة Celery
- **PostgreSQL Logs** لقاعدة البيانات

## 🚀 **النشر**

### GitHub Actions
النشر التلقائي عند push للفرع `main`:
1. **تشغيل الاختبارات**
2. **بناء Docker Image**
3. **رفع للـ Container Registry**
4. **نشر على Cloud Run**
5. **تطبيق Migrations**

### النشر اليدوي
```bash
# بناء الصورة
docker build -t naebak-admin-service .

# رفع لـ Google Cloud
gcloud builds submit --tag gcr.io/PROJECT_ID/naebak-admin-service

# النشر على Cloud Run
gcloud run deploy naebak-admin-service \
  --image gcr.io/PROJECT_ID/naebak-admin-service \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🤝 **المساهمة**

### إرشادات المساهمة
1. Fork المشروع
2. إنشاء فرع للميزة الجديدة
3. كتابة الاختبارات
4. تشغيل الاختبارات والتأكد من نجاحها
5. إرسال Pull Request

### معايير الكود
- **PEP 8** لتنسيق Python
- **تعليقات باللغة العربية** للوضوح
- **اختبارات شاملة** لكل ميزة جديدة
- **توثيق كامل** للـ APIs

## 📞 **الدعم**

### التواصل
- **الموقع**: https://naebak.com
- **البريد الإلكتروني**: admin@naebak.com
- **GitHub Issues**: لتقارير الأخطاء والاقتراحات

### الوثائق
- **API Documentation**: `/api/docs/`
- **Admin Panel**: `/admin/`
- **Health Check**: `/health/`

## 📄 **الترخيص**

هذا المشروع مرخص تحت [MIT License](LICENSE).

---

**تم تطويره بـ ❤️ لخدمة المواطن المصري**

© 2024 نائبك.كوم - جميع الحقوق محفوظة
