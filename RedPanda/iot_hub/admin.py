from django.contrib import admin

# Register your models here.

from .models import DataSource, Event, Variable, Widget

class VariableInline(admin.TabularInline):
	model = Variable
	extra = 0

class VariableAdmin(admin.ModelAdmin):
	list_display = ('name','source_short_id', 'unit','var_id')
	readonly_fields = ('var_id',)

class DataSourceAdmin(admin.ModelAdmin):
	list_display = ('name','source_id','create_date')
	readonly_fields = ('source_id','create_date', 'edition_date')
	inlines = [VariableInline]

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('source_id','create_date', 'edition_date')
   


admin.site.register(DataSource,DataSourceAdmin)
admin.site.register(Event)
admin.site.register(Variable,VariableAdmin)
admin.site.register(Widget)