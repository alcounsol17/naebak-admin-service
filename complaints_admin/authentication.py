"""
نظام المصادقة JWT لخدمة الأدمن - نائبك.كوم
JWT Authentication system for Naebak Admin Service
"""

import jwt
import requests
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication, exceptions
from rest_framework.authentication import BaseAuthentication
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class AdminUser:
    """
    فئة المستخدم الأدمن المخصصة
    Custom Admin User class for JWT authentication
    """
    def __init__(self, user_data):
        self.id = user_data.get('user_id')
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.first_name = user_data.get('first_name', '')
        self.last_name = user_data.get('last_name', '')
        self.user_type = user_data.get('user_type', 'admin')
        self.is_active = user_data.get('is_active', True)
        self.is_staff = user_data.get('is_staff', True)
        self.is_superuser = user_data.get('is_superuser', False)
        self.permissions = user_data.get('permissions', [])
        self.groups = user_data.get('groups', [])
        
    def is_authenticated(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def has_perm(self, perm):
        """التحقق من صلاحية معينة"""
        return perm in self.permissions or self.is_superuser
        
    def has_perms(self, perms):
        """التحقق من عدة صلاحيات"""
        return all(self.has_perm(perm) for perm in perms)
        
    def has_module_perms(self, app_label):
        """التحقق من صلاحيات تطبيق معين"""
        return self.is_superuser or any(
            perm.startswith(f'{app_label}.') for perm in self.permissions
        )
        
    def get_full_name(self):
        """الحصول على الاسم الكامل"""
        return f"{self.first_name} {self.last_name}".strip()
        
    def get_short_name(self):
        """الحصول على الاسم المختصر"""
        return self.first_name or self.username
        
    def __str__(self):
        return self.username


class JWTAuthentication(BaseAuthentication):
    """
    نظام المصادقة JWT المخصص
    Custom JWT Authentication for Admin Service
    """
    
    def authenticate(self, request):
        """
        التحقق من صحة التوكين
        Authenticate the request and return a two-tuple of (user, token)
        """
        auth_header = authentication.get_authorization_header(request).split()
        
        if not auth_header or auth_header[0].lower() != b'bearer':
            return None
            
        if len(auth_header) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
            
        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
            
        return self.authenticate_credentials(token)
        
    def authenticate_credentials(self, token):
        """
        التحقق من صحة التوكين وإرجاع المستخدم
        Authenticate the token and return user
        """
        try:
            # محاولة فك تشفير التوكين محلياً أولاً
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            # التحقق من انتهاء صلاحية التوكين
            exp_timestamp = payload.get('exp')
            if exp_timestamp and datetime.utcnow().timestamp() > exp_timestamp:
                raise exceptions.AuthenticationFailed('Token has expired.')
                
            # التحقق من نوع المستخدم (يجب أن يكون أدمن)
            user_type = payload.get('user_type')
            if user_type != 'admin':
                raise exceptions.AuthenticationFailed('Access denied. Admin privileges required.')
                
            # إنشاء كائن المستخدم
            user = AdminUser(payload)
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            # إذا فشل فك التشفير المحلي، نحاول التحقق مع خدمة المصادقة
            return self.verify_with_auth_service(token)
        except Exception as e:
            logger.error(f"JWT Authentication error: {str(e)}")
            raise exceptions.AuthenticationFailed('Invalid token.')
            
    def verify_with_auth_service(self, token):
        """
        التحقق من التوكين مع خدمة المصادقة
        Verify token with authentication service
        """
        try:
            auth_service_url = settings.AUTH_SERVICE_URL
            response = requests.post(
                f"{auth_service_url}/api/v1/auth/verify-token/",
                headers={'Authorization': f'Bearer {token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                
                # التحقق من نوع المستخدم
                if user_data.get('user_type') != 'admin':
                    raise exceptions.AuthenticationFailed('Access denied. Admin privileges required.')
                    
                user = AdminUser(user_data)
                return (user, token)
            else:
                raise exceptions.AuthenticationFailed('Invalid token.')
                
        except requests.RequestException as e:
            logger.error(f"Auth service verification failed: {str(e)}")
            raise exceptions.AuthenticationFailed('Authentication service unavailable.')
        except Exception as e:
            logger.error(f"Token verification error: {str(e)}")
            raise exceptions.AuthenticationFailed('Token verification failed.')
            
    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return a `403 Permission Denied` response.
        """
        return 'Bearer'


def create_admin_token(user_data):
    """
    إنشاء توكين JWT للأدمن
    Create JWT token for admin user
    """
    payload = {
        'user_id': user_data['user_id'],
        'username': user_data['username'],
        'email': user_data['email'],
        'user_type': 'admin',
        'is_staff': True,
        'is_superuser': user_data.get('is_superuser', False),
        'permissions': user_data.get('permissions', []),
        'groups': user_data.get('groups', []),
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA),
        'iat': datetime.utcnow(),
    }
    
    token = jwt.encode(
        payload, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token


def decode_admin_token(token):
    """
    فك تشفير توكين الأدمن
    Decode admin JWT token
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed('Token has expired.')
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed('Invalid token.')


class AdminPermissionMixin:
    """
    خليط الصلاحيات للأدمن
    Admin permission mixin for views
    """
    
    def check_admin_permission(self, request, required_permission=None):
        """
        التحقق من صلاحيات الأدمن
        Check admin permissions
        """
        if not hasattr(request, 'user') or not request.user.is_authenticated():
            raise exceptions.PermissionDenied('Authentication required.')
            
        if request.user.user_type != 'admin':
            raise exceptions.PermissionDenied('Admin privileges required.')
            
        if required_permission and not request.user.has_perm(required_permission):
            raise exceptions.PermissionDenied(f'Permission required: {required_permission}')
            
        return True
        
    def check_superuser_permission(self, request):
        """
        التحقق من صلاحيات المدير العام
        Check superuser permissions
        """
        self.check_admin_permission(request)
        
        if not request.user.is_superuser:
            raise exceptions.PermissionDenied('Superuser privileges required.')
            
        return True
