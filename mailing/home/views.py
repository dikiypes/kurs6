from django.views.generic import TemplateView
from django.core.cache import cache
from blog.models import BlogPost
from mailing_service.models import MailingList, Client


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение или установка значения из кеша
        total_mailings = cache.get('total_mailings')
        active_mailings = cache.get('active_mailings')
        unique_clients = cache.get('unique_clients')
        random_blog_posts = cache.get('random_blog_posts')

        if not total_mailings or not active_mailings or not unique_clients or not random_blog_posts:
            # Кеширование данных
            total_mailings = MailingList.objects.count()
            active_mailings = MailingList.objects.filter(status='active').count()
            unique_clients = Client.objects.distinct('email').count()

            # Получение 3 случайных статей блога
            random_blog_posts = BlogPost.objects.order_by('?')[:3]

            # Установка данных в кеш
            cache.set('total_mailings', total_mailings)
            cache.set('active_mailings', active_mailings)
            cache.set('unique_clients', unique_clients)
            cache.set('random_blog_posts', random_blog_posts)

        context['total_mailings'] = total_mailings
        context['active_mailings'] = active_mailings
        context['unique_clients'] = unique_clients
        context['random_blog_posts'] = random_blog_posts

        return context
