from rest_framework import serializers
from .models import RequestForm
from .models import Refund ,Excess, Item
class Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('descriptions', 'quantity', 'uom', 'price')
        
class RequestForm_Serializer(serializers.ModelSerializer):
    business_unit_name = serializers.CharField(source='business_unit.business_unit_name', read_only=True)
    encoder_name = serializers.CharField(source='encoded_by.first_name', read_only=True)
    encoder_last = serializers.CharField(source='encoded_by.last_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewed_by.first_name', read_only=True)
    reviewer_last = serializers.CharField(source='reviewed_by.last_name', read_only=True)
    approved = serializers.CharField(source='approved_by.first_name', read_only=True)
    approved_last = serializers.CharField(source='approved_by.last_name', read_only=True)
    release = serializers.CharField(source='release_by.first_name', read_only=True)
    release_last = serializers.CharField(source='release_by.last_name', read_only=True)
    items = Item_Serializer(many=True)

    class Meta:
        model = RequestForm
        fields = (
            'id',
            'voucher_no',
            'activity',
            'profit_center',
            'covered_from',
            'covered_to',
            'date_requested',
            'amount',
            'business_unit',
            'status',
            'encoded_by',
            'reviewed_by',
            'approved_by',
            'release_by',
            'business_unit_name',
            'encoder_name',
            'reviewer_name',
            'approved',
            'release',
            'fund_allocation',
            'approved_last',
            'reviewer_last',
            'encoder_last',
            'release_last',
            'with_receipt',
            'with_out_receipt',
            'items',
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        request_form = RequestForm.objects.create(**validated_data)

        for item_data in items_data:
            Item.objects.create(request_form=request_form, **item_data)

        return request_form


class UpdateRequestForm_Serializer(serializers.ModelSerializer):
    business_unit_name = serializers.CharField(source='business_unit.business_unit_name', read_only=True)
    encoder_name = serializers.CharField(source='encoded_by.first_name', read_only=True)
    encoder_last = serializers.CharField(source='encoded_by.last_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewed_by.first_name', read_only=True)
    reviewer_last = serializers.CharField(source='reviewed_by.last_name', read_only=True)
    approved = serializers.CharField(source='approved_by.first_name', read_only=True)
    approved_last = serializers.CharField(source='approved_by.last_name', read_only=True)
    release = serializers.CharField(source='release_by.first_name', read_only=True)
    release_last = serializers.CharField(source='release_by.last_name', read_only=True)
    items = Item_Serializer(many=True, read_only=True)
    fund_name = serializers.SerializerMethodField()

    class Meta:
        model = RequestForm
        fields = (
            'id',
            'voucher_no',
            'activity',
            'profit_center',
            'covered_from',
            'covered_to',
            'date_requested',
            'amount',
            'business_unit',
            'status',
            'encoded_by',
            'reviewed_by',
            'approved_by',
            'release_by',
            'business_unit_name',
            'encoder_name',
            'reviewer_name',
            'approved',
            'release',
            'fund_allocation',
            'approved_last',
            'reviewer_last',
            'encoder_last',
            'release_last',
            'with_receipt',
            'with_out_receipt',
            'items',
            'fund_name',
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])

        request_form = RequestForm.objects.create(**validated_data)

        for item_data in items_data:
            Item.objects.create(request_form=request_form, **item_data)

        return request_form
    
    def get_fund_name(self, obj):
        fund_name = obj.fund_allocation.name.name
        return fund_name
    
class editRequestForm_Serializer(serializers.ModelSerializer):
    business_unit_name = serializers.CharField(source='business_unit.business_unit_name', read_only=True)
    encoder_name = serializers.CharField(source='encoded_by.first_name', read_only=True)
    encoder_last = serializers.CharField(source='encoded_by.last_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewed_by.first_name', read_only=True)
    reviewer_last = serializers.CharField(source='reviewed_by.last_name', read_only=True)
    approved = serializers.CharField(source='approved_by.first_name', read_only=True)
    approved_last = serializers.CharField(source='approved_by.last_name', read_only=True)
    release = serializers.CharField(source='release_by.first_name', read_only=True)
    release_last = serializers.CharField(source='release_by.last_name', read_only=True)
    items = Item_Serializer(many=True)

    class Meta:
        model = RequestForm
        fields = (
            'id',
            'voucher_no',
            'activity',
            'profit_center',
            'covered_from',
            'covered_to',
            'date_requested',
            'amount',
            'business_unit',
            'status',
            'encoded_by',
            'reviewed_by',
            'approved_by',
            'release_by',
            'business_unit_name',
            'encoder_name',
            'reviewer_name',
            'approved',
            'release',
            'fund_allocation',
            'approved_last',
            'reviewer_last',
            'encoder_last',
            'release_last',
            'with_receipt',
            'with_out_receipt',
            'items',
        )

    def update(self, instance, validated_data):
        instance.voucher_no = validated_data.get('voucher_no', instance.voucher_no)
        instance.activity = validated_data.get('activity', instance.activity)
        instance.profit_center = validated_data.get('profit_center', instance.profit_center)
        instance.covered_from = validated_data.get('covered_from', instance.covered_from)
        instance.covered_to = validated_data.get('covered_to', instance.covered_to)
        instance.date_requested = validated_data.get('date_requested', instance.date_requested)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.status = validated_data.get('status', instance.status)

        items_data = validated_data.get('items', [])
        for item_data in items_data:
            item_voucher_no = item_data.get('voucher_no')
            if item_voucher_no:
                item_instance = instance.items.filter(voucher_no=item_voucher_no).first()
                if item_instance:
                    item_instance.descriptions = item_data.get('descriptions', item_instance.descriptions)
                    item_instance.quantity = item_data.get('quantity', item_instance.quantity)
                    item_instance.uom = item_data.get('uom', item_instance.uom)
                    item_instance.price = item_data.get('price', item_instance.price)
                    item_instance.save()

        instance.save()
        return instance

class Refund_Serializer(serializers.ModelSerializer):
    available_amount =  serializers.CharField(source='voucher_no.amount', read_only=True)
    business_unit =  serializers.CharField(source='voucher_no.amount', read_only=True)
    class Meta:
        model = Refund
        fields = (
                'id',
                'voucher_no',
                'refund_amount',
                'available_amount',
                'user',
                'business_unit',

        )
    
class Excess_Serializer(serializers.ModelSerializer):
    available_amount =  serializers.CharField(source='voucher_no.amount', read_only=True)
    class Meta:
        model = Excess
        fields = (
                'id',
                'voucher_no',
                'excess_amount',
                'available_amount',
                'user',

        )

