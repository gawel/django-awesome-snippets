from django.db import models
from snippets import snippet

class MyModel(models.Model):

    class Meta:
        app_label = 'app'

    name = models.CharField(max_length=255)

    # simple attribute (name is required)
    h1 = snippet(name='h1')

    # as a property. Then then function may return a dict. This dict will be
    # available in the template
    @snippet
    def a_tag(self):
        return dict(url=self.get_absolute_url())

    # as a property with extra arguments
    @snippet(template='app/snippets/mymodel_a_tag.html')
    def custom_template(self):
        return dict(url=self.get_absolute_url())

    # as a cached property using another template (specified by name)
    # here the template used will be app/snippets/mymodel_a_tag.html instead of
    # app/snippets/mymodel_a_cached_tag.html
    @snippet(name='a_tag', delay=60)
    def a_cached_tag(self):
        return dict(url=self.get_absolute_url())

    def get_absolute_url(self):
        return '/mymodel/%s' % self.id


