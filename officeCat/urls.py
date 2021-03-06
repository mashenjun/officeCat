"""officeCat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
import notifications.urls
from rest_framework.documentation import include_docs_urls


# from django.contrib import admin

urlpatterns = [
    url(r'^accounts/', include('accounts.urls',namespace='accounts')),
    url(r'^profiles/', include('profiles.urls',namespace='profiles')),
    url(r'^hire/', include('hire.urls',namespace='hire')),
    url(r'^functions/', include('functions.urls',namespace='functions')),
    url(r'^cms/', include('cms.urls',namespace='cms')),
    # url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    # url(r'^admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^utils/', include('captcha.urls')),
    url(r'^api-docs/', include('rest_framework_docs.urls')),
]

if settings.DEBUG :
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns +=[
    url(r'^', include('my-app.urls', namespace='my-app')),
]
