from django import template
from django.core.exceptions import FieldDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta
register=template.Library()


@register.simple_tag
def render_table_name(table):
    return table._meta.verbose_name

@register.simple_tag
def render_table_url(request,table_obj):
    colum_data="<a href='{request_path}{table_obj_id}/change/'>{table_uid}</a>".format(
        request_path=request.path,
        table_obj_id=table_obj.id,
        table_uid=table_obj.uid,
    )
    row_ele=''
    row_ele+="<td>%s</td>"%colum_data
    return mark_safe(row_ele)

@register.simple_tag
def render_obj_id(table_obj):
    return str(table_obj.id)

@register.simple_tag
def render_tableobjs_all(table):
    return table.objects.all()