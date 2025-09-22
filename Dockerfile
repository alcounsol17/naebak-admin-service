# Dockerfile لخدمة الأدمن - نائبك.كوم
# Naebak Admin Service Docker Configuration

FROM python:3.11-slim

# تثبيت متطلبات النظام
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# إنشاء مستخدم غير جذر
RUN useradd --create-home --shell /bin/bash app

# تعيين مجلد العمل
WORKDIR /app

# نسخ ملفات المتطلبات
COPY requirements.txt .

# تثبيت متطلبات Python
RUN pip install --no-cache-dir -r requirements.txt

# نسخ كود التطبيق
COPY . .

# تغيير ملكية الملفات للمستخدم app
RUN chown -R app:app /app

# التبديل للمستخدم غير الجذر
USER app

# جمع الملفات الثابتة
RUN python manage.py collectstatic --noinput

# فتح المنفذ
EXPOSE 8000

# متغيرات البيئة
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=admin_service.settings

# فحص صحة التطبيق
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# تشغيل التطبيق
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "admin_service.wsgi:application"]
