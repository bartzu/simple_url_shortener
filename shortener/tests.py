from django.test import TestCase
from django.urls import reverse

from .views import shorten_url, redirect_to_url
from .models import FullURL, Shortcut


class ShortenUrlViewTest(TestCase):

    def test_loads_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed('shortener/shorten_url.html')

    def test_redirects_after_POST(self):
        response = self.client.post('/', {'full_url': 'http://correct.url', 'proposed_shortcut': ''})
        #self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, 
            response['location']
        )

    def test_creates_new_random_shortcut(self):
        url = 'http://correct.url'
        response = self.client.post(
            '/', 
            {'full_url': url, 'proposed_shortcut': ''}
        )
        self.assertEqual(FullURL.objects.all()[0].url, url)
        self.assertEqual(Shortcut.objects.count(), 1)
    
    def test_creates_new_proposed_shortcut(self):
        url = 'http://correct.url'
        proposition = 'skrot'
        response = self.client.post(
            '/', 
            {'full_url': url, 'proposed_shortcut': proposition}
        )

        link = FullURL.objects.get(url=url)
        self.assertEqual(
            Shortcut.objects.get(full_url=link).value,
            proposition
        )


class RedirectToURLViewTest(TestCase):

    def test_getting_unexisting_sc(self):
        response = self.client.get(
            reverse('shortener:redirect_to_url', args=['not_existing_sc']))
        self.assertEqual(response.status_code, 404)

    def test_redirects_to_shortened_url(self):
        #create url shortcut
        url = 'http://example.com'
        psc = 'a'
        link = FullURL.objects.create(url=url)
        sc = Shortcut.objects.create(
            value=psc, full_url=link
        )

        response = self.client.get(
            reverse('shortener:redirect_to_url', args=[psc])
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)