from posts.views import new_post
from django.http import response
from django import forms  
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from time import sleep

from posts.models import User,Group,Post

User = get_user_model()

class ViewModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title = 'Название группы',
            slug = 'test-slug',
            description = 'Test-slug'
        )

        cls.posts = Post.objects.create(
            text='Текст вашего поста',
            group = cls.group,
            author = User.objects.create(username ='artur')
        )
        sleep(0.01) 
        cls.group2 = Group.objects.create(
            title = 'Назван22ие группы',
            slug = 'test2-slug',
            description = 'Test-slug'
        )
        cls.posts2 = Post.objects.create(
            text='Текст222а',
            group = cls.group2,
            author = User.objects.create(username ='ivan')
        )  
       
    def setUp(self):
        self.user = User.objects.create_user(username='test-user') 
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
       
    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Собираем в словарь пары "имя_html_шаблона: name"
        templates_pages_names = {
            'index.html': reverse('index'),
            'new.html': reverse('new_post'),
            'group.html': reverse('group_posts',args= [ViewModelTest.group.slug])
            }     
       
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 

    def test_home_page_shows_correct_context(self):
        """Проверка главной страницы  на шаблон""" 
        response = self.authorized_client.get(reverse('index'))

        post_object = response.context['posts'][1]
        post_author_0 = post_object.author
        post_pub_date_0 = post_object.pub_date
        post_text_0 = post_object.text

        self.assertEqual(post_author_0.username, ViewModelTest.posts.author.username)
        self.assertEqual(post_text_0, ViewModelTest.posts.text)
        self.assertEqual(post_pub_date_0, ViewModelTest.posts.pub_date)

    def test_group_page_shows_correct_context(self):
        """Проверка страницы группы на шаблон""" 
        response = self.authorized_client.get(reverse('group_posts',args= [ViewModelTest.group.slug]))
        
        group_object = response.context['posts'][0]
        
        group_author_0 = group_object.author
        group_pub_date_0 = group_object.pub_date
        group_text_0 = group_object.text

        self.assertEqual(group_author_0.username,ViewModelTest.posts.author.username)
        self.assertEqual(group_pub_date_0,ViewModelTest.posts.pub_date)
        self.assertEqual(group_text_0,ViewModelTest.posts.text)

    def test_new_posts_page_shows_correct_context(self):
        """Проверка страницы нового поста  на шаблон""" 
        response = self.authorized_client.get(reverse('new_post'))

        form_fields={
        'text': forms.fields.CharField,
        'group':forms.fields.ChoiceField
        }        
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)       

    def test_create_new_post(self):
        """Посты совападют """   
        last_post = Post.objects.last()    
        self.assertEqual(ViewModelTest.posts.id, last_post.id)

    def test_index_create_new_post(self):
        """ Новый пост появляется на странице index """
        response = self.authorized_client.get(reverse('index'))
        post_object = response.context['posts'][1]
        post_text_index = post_object.text
        last_post = Post.objects.last()
        self.assertEqual(post_text_index,last_post.text)

    def test_new_post_group_identification(self):
        """ Новый пост  не  появляетя не в своей группе """
        response = self.authorized_client.get(reverse('group_posts',args= [ViewModelTest.group2.slug]))
        post2_object = response.context['posts'][0]
        post2_id = post2_object.id
        last_post = Post.objects.last()
        self.assertNotEqual(post2_id,last_post.id)
        
 