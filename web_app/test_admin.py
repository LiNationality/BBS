from web_app import models
from django.shortcuts import render,HttpResponse,redirect

app_admin={}
class BaseModelAdmin(object):
    list_display = []
    list_filters = []
    search_fields = []
    list_per_page = 20
    ordering = None
    filter_horizontal = []
    readonly_fields = []
    actions = ["delete_selected_objs", ]
    readonly_table = False
    modelform_exclude_fields = []
    def delete_selected_objs(self,request,querysets):
        app_name=self.model._meta.app_label
        table_name=self.model._meta.model_name
        print("--->delete_selected_objs",self,request,querysets)
        if self.readonly_table:
            errors={"readonly_table":"This table is readonly ,cannot be deleted or modified!"}
        else:
            errors={}
        if request.POST.get("delete_confirm")=="yes":
            if not self.readonly_table:
                querysets.delete()
            return redirect(request,"/test/%s/%s"%(app_name,table_name))
        select_ids=','.join([str(i.id) for i in querysets])
        return render(request,"")

