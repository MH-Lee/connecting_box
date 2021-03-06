from rest_framework import serializers
from contents.models import Rescue


class RescueSerializer(serializers.ModelSerializer):
    content_url = serializers.SerializerMethodField('get_content_url')
    class Meta:
        model = Rescue
        fields = ('id',
                  'date',
                  'area',
                  'case_num',
                  'company_name',
                  'company_address',
                  'ceo',
                  'court',
                  'subject',
                  'news_title',
                  'news_url',
                  'content_url')
    
    def get_content_url(self, obj):
        return "/information/rescue_detail/{}/".format(obj.id)