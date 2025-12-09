import json
from django.core.serializers.json import DjangoJSONEncoder

class AnalyticsAdminMixin:
    change_list_template = "admin/chart_change_list.html"
    chart_title = "Analytics"
    chart_type = "bar"

    def get_chart_data(self, queryset):

        return {}

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        


        qs = self.get_queryset(request)
        chart_data = self.get_chart_data(qs)
        
        if chart_data:
            extra_context['chart_data'] = json.dumps(chart_data, cls=DjangoJSONEncoder)
            extra_context['chart_title'] = self.chart_title
            extra_context['chart_type'] = self.chart_type
        
        return super().changelist_view(request, extra_context=extra_context)
