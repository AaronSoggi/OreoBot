from django.test import TestCase, Client
from django.urls import reverse
import json 



class TestViews(TestCase):
    def test_dashboard(self):
        response = self.client.get(self)        

        