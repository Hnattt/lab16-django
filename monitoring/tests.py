from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError,transaction
from .models import Device
class DeviceTests(TestCase):
 def setUp(self):
  self.a=Device.objects.create(name='Холод камера',serial='V03-A'); Device.objects.create(name='Холод шлюз',serial='V03-B'); Device.objects.create(name='Склад',serial='V03-C')
 def test_pages_search(self):
  self.assertEqual(self.client.get('/').status_code,200); self.assertEqual(self.client.get(f'/devices/{self.a.pk}/').status_code,200); self.assertEqual(self.client.get('/devices/999/').status_code,404); self.assertEqual(self.client.post('/').status_code,405)
  before=Device.objects.count(); r=self.client.get('/',{'q':'Холод'}); self.assertEqual(len(r.context['devices']),2); self.assertEqual(len(self.client.get('/',{'q':''}).context['devices']),3); self.assertEqual(len(self.client.get('/',{'q':'неіснуючий-зразок'}).context['devices']),0); self.assertEqual(Device.objects.count(),before)
 def test_empty(self):
  Device.objects.all().delete(); self.assertContains(self.client.get('/'),'Пристроїв немає')
 def test_duplicate(self):
  with self.assertRaises(IntegrityError), transaction.atomic(): Device.objects.create(name='Дубль',serial=self.a.serial)
 def test_admin_rights(self):
  u=get_user_model().objects.create_user(username='regular',password='local-test'); self.client.force_login(u); self.assertEqual(self.client.get('/admin/').status_code,302)
  admin=get_user_model().objects.create_superuser(username='admin',password='local-test'); self.client.force_login(admin)
  r=self.client.post('/admin/monitoring/device/add/',{'name':'Тестовий','serial':'ADMIN-DEMO'}); self.assertEqual(r.status_code,302); self.assertTrue(Device.objects.filter(serial='ADMIN-DEMO').exists())
