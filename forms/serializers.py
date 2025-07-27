from rest_framework import serializers
from .models import RequestForm
from .models import Item

class Item_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('descriptions', 'quantity', 'uom', 'price','item_total_amount')
        
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
            'requested_by',
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
            'encoded_date',
            'reviewed_date',
            'approved_date',
            'released_date',
            'excess',
            'refund',
            'received_by',
            'received_date',
            'liquidated_date',
            'replenish_date',
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
            'requested_by',
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
            'encoded_date',
            'reviewed_date',
            'approved_date',
            'released_date',
            'excess',
            'refund',
            'received_by',
            'received_date',
            'liquidated_date',
            'replenish_date',
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
            'requested_by',
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
            'encoded_date',
            'reviewed_date',
            'approved_date',
            'released_date',
            'excess',
            'refund',
            'received_by',
            'received_date',
            'liquidated_date',
            'replenish_date',
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
        instance.requested_by = validated_data.get('requested_by', instance.requested_by)
        instance.business_unit = validated_data.get('business_unit', instance.business_unit)
        instance.fund_allocation = validated_data.get('fund_allocation', instance.fund_allocation)
        instance.encoded_date = validated_data.get('encoded_date', instance.encoded_date)


        items_data = validated_data.get('items', [])
        existing_items = instance.items.all()
        for item_data in items_data:
            item_id = item_data.get('id', None)
            if item_id:
                item = existing_items.filter(pk=item_id).first()
                if item:
                    item.descriptions = item_data.get('descriptions', item.descriptions)
                    item.quantity = item_data.get('quantity', item.quantity)
                    item.uom = item_data.get('uom', item.uom)
                    item.price = item_data.get('price', item.price)
                    item.item_total_amount = item_data.get('item_total_amount', item.item_total_amount)
                    item.save()

        instance.save()
        return instance


