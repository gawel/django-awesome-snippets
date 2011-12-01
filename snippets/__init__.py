# -*- coding: utf-8 -*-
try:
    from django.conf import settings
    from django.core.cache import cache
    from django.template.loader import render_to_string
except ImportError:
    pass


class Snippet(property):

    def __init__(self, func=None, name=None, template=None, delay=None, cache_field=None):
        self.func = func
        self.name = self.__doc__ = None
        if func:
            self.name = name or func.__name__
            self.__doc__ = func.__doc__
        elif name:
            self.name = name
            self.__doc__ = 'Snippet for %s' % name
        self.template = template
        if delay is not None:
            self.delay = delay
        else:
            self.delay = getattr(settings, 'SNIPPETS_CACHE_DELAY', None)
        self.cache_field = cache_field

    def render(self, instance):
        if self.template:
            template = self.template
        else:
            template = '%s/snippets/%s_%s.html' % (instance._meta.app_label,
                                                   instance.__class__.__name__.lower(),
                                                   self.name)
        ctx = dict(object=instance, settings=settings,
                   MEDIA_URL=settings.MEDIA_URL)
        if self.func:
            vars = self.func(instance)
            if isinstance(vars, dict):
                ctx.update(vars)
        value = render_to_string(template, ctx)
        return value

    def key(self, instance):
        if self.cache_field:
            field = getattr(instance, self.cache_field)
            if hasattr(field, 'pk'):
                field = field.pk
        else:
            field = instance.pk
        value = 'snippets-%s-%s-%s-%s' % (instance._meta.app_label,
                                         instance.__class__.__name__.lower(),
                                         self.name, field)
        return value.lower()

    def purge(self, instance):
        cache.set(self.key(instance), '', 1)

    def __get__(self, instance, klass):
        if self.delay is None:
            return self.render(instance)
        else:
            key = self.key(instance)
            value = cache.get(key)
            if not value:
                value = self.render(instance)
                cache.set(key, value, self.delay)
            return value

    def __call__(self, func):
        self.func = func
        if self.name is None:
            self.name = self.func.__name__
        self.__doc__ = func.__doc__
        return self

def snippet(*args, **kwargs):
    """snippet decorator"""
    return Snippet(*args, **kwargs)

def purge(instance):
    """purge cached attribute of an instance"""
    klass = instance.__class__
    for v in klass.__dict__.values():
        if isinstance(v, Snippet) and v.delay is not None:
            v.purge(instance)
