from rest_framework import serializers
from .models import RequestForm
from businessUnit.models import BusinessUnit
from user.models import User
class RequestForm_Serializer(serializers.ModelSerializer):
    business_unit_name =  serializers.CharField(source='business_unit.business_unit_name', read_only=True)
    encoder_name = serializers.CharField(source='encoded_by.first_name', read_only=True)
    reviewer_name = serializers.CharField(source='reviewed_by.first_name', read_only=True)
    approved = serializers.CharField(source='approved_by.first_name', read_only=True)
    release = serializers.CharField(source='release_by.first_name', read_only=True)
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
                'descriptions',
                'quantity',
                'uom',
                'price',
                'amount',
                'business_unit',
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

        )
