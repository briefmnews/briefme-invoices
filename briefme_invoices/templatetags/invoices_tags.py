from django import template


register = template.Library()


@register.simple_tag
def has_invoicing_information(user):
    has_name = (user.last_name and user.first_name) or user.organization
    has_address = user.address and user.zip and user.city and user.country
    return has_name and has_address
