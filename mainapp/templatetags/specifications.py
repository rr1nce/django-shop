from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TABLE_HEAD = """
                <table class="table">
                    <tbody>
"""

TABLE_TAIL = """
                    </tbody>
                </table>
"""

TABLE_CONTENT = """
                    <tr>
                        <td>{name}</td>
                        <td>{value}</td>
                    </tr>
"""

PRODUCT_SPEC = {
    'notebook': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display',
        'Частота процессора': 'processor_freq',
        'Оперативная память': 'ram',
        'Видеокарта': 'video',
        'Время работа от аккумулятора': 'time_without_charge'
    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display',
        'Разрешение экрана': 'resolution',
        'Объем батареи': 'accum_volume',
        'Оперативная память': 'ram',
        'Поддержка SD-карты': 'sd',
        'Максимальный объем памяти SD-карты': 'sd_volume_max',
        'Разрешение главной камеры': 'main_cam_mp',
        'Разрешение фронтальной камеры': 'front_cam_mp'
    }
}

def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content

@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if model_name == 'smartphone':
        table_content = ''
        flag = False
        for name, value in PRODUCT_SPEC[model_name].items():
            if name == "Поддержка SD-карты":
                if not getattr(product, value):
                    flag = True
                    table_content += TABLE_CONTENT.format(name=name, value="Отсутствует")
                else:
                    flag = False
                    table_content += TABLE_CONTENT.format(name = name, value = "Есть")
            elif name == 'Максимальный объем памяти SD-карты':
                if flag:
                    pass
                else:
                    table_content += TABLE_CONTENT.format(name = name, value = getattr(product, value))
            else:
                table_content += TABLE_CONTENT.format(name = name, value = getattr(product, value))


        return mark_safe(TABLE_HEAD + table_content + TABLE_TAIL)
    else:
        return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)


