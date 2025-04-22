from django import template
from datetime import datetime
import pytz
from django.conf import settings

register = template.Library()

@register.filter(name='format_datetime')
def format_datetime(value, format_string=None):
    """
    Format a string datetime (ISO 8601) to a more readable format.
    
    template example:
    {{ article.created_at|format_datetime }}  -> "18/04/2025 15:30"
    {{ article.created_at|format_datetime:"date" }}  -> "18/04/2025"
    {{ article.created_at|format_datetime:"datetime" }}  -> "18/04/2025 15:30"
    {{ article.created_at|format_datetime:"full" }}  -> "18 de Abril de 2025 às 15:30"
    """
    if not value:
        return ''
        
    try:
        # If the value is already a datetime object, use it directly
        if isinstance(value, datetime):
            dt = value
        else:
            # Converte a string ISO 8601 para datetime
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            
        # Convert to UTC if the timezone is not set
        if settings.USE_TZ:
            dt = dt.astimezone(pytz.timezone(settings.TIME_ZONE))
            
        # Prefine the format strings
        formats = {
            'date': '%d/%m/%Y',
            'datetime': '%d/%m/%Y %H:%M',
            'full': '%d de %B de %Y às %H:%M',
            'short': '%d/%m/%y',
            'time': '%H:%M'
        }
        
        # If a format string is provided, use it; otherwise, default to 'datetime'
        format_string = formats.get(format_string, formats['datetime'])
            
        return dt.strftime(format_string).replace('  ', ' ')
        
    except (ValueError, TypeError, AttributeError):
        return value  # Return the original value if conversion fails