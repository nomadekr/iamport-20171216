import json
from django import forms
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('imp_uid',)

    def as_iamport(self):
        # 본 Form의 Hidden 필드 위젯
        hidden_fields = mark_safe(''.join(smart_text(field) for field in self.hidden_fields()))

        # IMP.request_pay의 인자로 넘길 인자 목록
        fields = {
            'merchant_uid': str(self.instance.merchant_uid),
            'name': self.instance.name,
            'amount': self.instance.amount,
        }

        return hidden_fields + render_to_string('shop/_iamport.html', {
            'json_fields': mark_safe(json.dumps(fields, ensure_ascii=False)),
            'iamport_shop_id': 'iamport',  # FIXME: 각자의 상점 아이디로 변경 가능
        })

    def save(self):
        order = super().save(commit=False)
        order.status = 'paid'  # FIXME: 아임포트 API를 통한 확인 후에 변경을 해야만 합니다.
        order.save()

        return order

