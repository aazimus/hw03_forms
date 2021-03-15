# posts/tests/tests_url.py
from django.conf.urls import url
from posts.views import index
from django.test import TestCase, Client
from django.urls import reverse
#from django.urls import include, path
from posts.models import Post,Group, User

class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get(reverse('index'))  
        self.assertEqual(response.status_code, 200) 


class Test_Client_Url(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='user') 
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        
        super().setUpClass()        
        cls.guest_client = Client() 
        cls.group = Group.objects.create(
            title = 'Проба',
            slug = 'test-slug',
            description = 'Описание группы'
        )

        #cls.urls_code = {            
        #reverse('index',args= None):[200,200],
        #reverse('new_post',args=None):[302,200],
        #reverse("group_posts",args= [Test_Client_Url.group.slug]):[200,200]
        #}

        cls.urls_code = {            
        'index':[200,200,None],
        'new_post':[302,200,None],
        'group_posts':[200,200,Test_Client_Url.group.slug]
        }

    def rev(self,url_name,argument = None):
        #url_name = self.url_name
        #argument = self.argument
        return reverse(url_name, args= self.argument )
        
    def test_home_url_exists_at_desired_location(self):
        """Тесты на не авторизтрованного пользователя прошли"""
                        
        for urls,none_user_code in Test_Client_Url.urls_code.items():
            with self.subTest():
                response = self.guest_client.get(Test_Client_Url.rev(urls,none_user_code[2]))
                self.assertEqual(response.status_code,none_user_code[0])         

    
    def test_home_url_user_location(self):
        """Тесты на авторизированного пользователя прошли"""
        for urls, authorized_user_code in Test_Client_Url.urls_code.items():
            with self.subTest():
                response = self.authorized_client.get(urls)
                self.assertEqual(response.status_code,authorized_user_code[1]) 

    def test_urls_uses_correct_template(self):
        """ URL-адрес использует соответствующий шаблон. """
        templates_url_names = {
        'index.html': reverse('index'),
        'new.html': reverse('new_post'),
        #'group.html': reverse('group_posts',args= [Test_Client_Url.group.slug])
        'group.html': '/group/test-slug/'
        }
        for template, reverse_name in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 

    def test_new_url_redirect_anonymous_on_admin_login(self):
        """ Перенаправление не авторизированиго пользователя с new на регистрацию"""
        response = Test_Client_Url.guest_client.get(reverse('new_post'), follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/new/')                               