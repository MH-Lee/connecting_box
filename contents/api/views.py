from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from contents.models import Rescue
from contents.api.serializers import RescueSerializer
from utils.paginations import StandardResultPagination

class RescueAPIView(generics.ListAPIView):
    queryset = Rescue.objects.all().order_by('date')
    serializer_class = RescueSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        queryset = Rescue.objects.all()
        date_by = self.request.GET.get('date')
        start_date_by = self.request.GET.get('start_date')
        case_num_by = self.request.GET.get('case_num')
        name_by = self.request.GET.get('company_name')
        address_by = self.request.GET.get('address')
        area_by = self.request.GET.get('area')
        if date_by:
            queryset = queryset.filter(date=date_by)
        if start_date_by:
            queryset = queryset.filter(date__gte=start_date_by)
        if case_num_by:
            queryset = queryset.filter(case_num=case_num_by)
        if name_by:
            queryset = queryset.filter(company_name=name_by)
        if address_by:
            queryset = queryset.filter(company_address=address_by)
        if area_by:
            queryset = queryset.filter(area=area_by)
        return queryset