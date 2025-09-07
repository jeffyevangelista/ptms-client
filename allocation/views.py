
from rest_framework.viewsets import ModelViewSet
from .serializers import allocation_Serializer,allocationLog_Serializer
from fund.models import Fund
from django.db import transaction
from .models import Allocation,AllocationLog
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class Allocation_view(ModelViewSet):
    serializer_class = allocation_Serializer
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,) 

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        fund = serializer.validated_data["name"]            # Fund instance
        bu   = serializer.validated_data["business_unit"]
        amt  = serializer.validated_data["amount"]

        # Lock the fund row to prevent race conditions
        fund_locked = Fund.objects.select_for_update().get(pk=fund.pk)

        # Prevent duplicate allocation for the same (fund, BU)
        if Allocation.objects.filter(name=fund_locked, business_unit=bu).exists():
            return Response(
                {"message": "Business unit already allocated for this fund."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if amt <= 0:
            return Response({"message": "Amount must be greater than 0."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Ensure sufficient balance
        if fund_locked.amount < amt:
            return Response({"message": "Insufficient fund balance."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Decrement fund using F expression (concurrency-safe)
        Fund.objects.filter(pk=fund_locked.pk).update(amount=F("amount") - amt)

        # Create the allocation record
        allocation = serializer.save()

        return Response(
            {
                "message": "Fund Allocation created successfully",
                "data": self.get_serializer(allocation).data,
            },
            status=status.HTTP_201_CREATED,
        )
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Edit an allocation:
          - If only amount changes on same fund: adjust by delta (±).
          - If business_unit changes: enforce uniqueness per (fund, BU).
          - If fund changes: refund old fund fully, deduct new fund by new amount.
        All with row locks to avoid race conditions.
        """
        partial = kwargs.pop("partial", False)
        instance: Allocation = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # New values (fallback to current instance if field not provided in PATCH)
        new_fund = serializer.validated_data.get("name", instance.name)  # 'name' is Fund FK
        new_bu   = serializer.validated_data.get("business_unit", instance.business_unit)
        new_amt  = serializer.validated_data.get("amount", instance.amount)

        # Optional: reject non-positive amounts when provided
        if "amount" in serializer.validated_data and new_amt <= 0:
            return Response({"message": "Amount must be greater than 0."}, status=status.HTTP_400_BAD_REQUEST)

        # Prevent duplicate allocation for same (fund, BU) excluding this record
        if Allocation.objects.filter(name=new_fund, business_unit=new_bu).exclude(pk=instance.pk).exists():
            return Response(
                {"message": "Allocation for the specified fund and business unit already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        old_fund = instance.name
        old_amt  = instance.amount

        if new_fund.pk == old_fund.pk:
            # --- Same fund: adjust by delta ---
            delta = new_amt - old_amt
            if delta != 0:
                fund_locked = Fund.objects.select_for_update().get(pk=old_fund.pk)
                if delta > 0:
                    # increasing allocation → need available balance
                    if fund_locked.amount < delta:
                        return Response({"message": "Insufficient fund balance."}, status=status.HTTP_400_BAD_REQUEST)
                    Fund.objects.filter(pk=fund_locked.pk).update(amount=F("amount") - delta)
                else:
                    # decreasing allocation → refund the difference
                    Fund.objects.filter(pk=fund_locked.pk).update(amount=F("amount") + (-delta))
        else:
            # --- Moving to a different fund ---
            # Lock both funds in deterministic order to avoid deadlocks
            fund_ids = sorted([old_fund.pk, new_fund.pk])
            locked = {f.pk: f for f in Fund.objects.select_for_update().filter(pk__in=fund_ids)}

            new_locked = locked[new_fund.pk]
            # ensure destination has enough for the NEW amount
            if new_locked.amount < new_amt:
                return Response({"message": "Insufficient fund balance in the destination fund."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Refund old fund by its full previous amount; deduct from new fund the new amount
            Fund.objects.filter(pk=old_fund.pk).update(amount=F("amount") + old_amt)
            Fund.objects.filter(pk=new_fund.pk).update(amount=F("amount") - new_amt)

        # Persist allocation fields
        instance.name = new_fund
        instance.business_unit = new_bu
        instance.amount = new_amt
        instance.save()

        return Response(
            {"message": "Fund Allocation updated successfully", "data": self.get_serializer(instance).data},
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        """Refund on delete, concurrency-safe."""
        instance: Allocation = self.get_object()
        Fund.objects.select_for_update().filter(pk=instance.name_id).update(amount=F("amount") + instance.amount)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AllocationLog_view(ModelViewSet):
    serializer_class = allocationLog_Serializer
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,) 

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()


class AllocationListView(APIView):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user  # ← already authenticated by JWT/Session

        # If the user can be linked to multiple funds:
        fund_ids = list(user.fund_set.values_list('id', flat=True))
        if not fund_ids:
            return Response([], status=status.HTTP_200_OK)

        # Filter allocations by those funds (FK field is "name" pointing to Fund)
        qs = (Allocation.objects
              .select_related('name', 'business_unit')
              .filter(name_id__in=fund_ids))

        data = allocation_Serializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class Allocation_List_Per_BU_View(APIView):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # all BUs the user belongs to
        bu_qs = request.user.business_unit.all()
        if not bu_qs.exists():
            # Return empty list (cleaner than 400/401 here)
            return Response([], status=status.HTTP_200_OK)

        allocations = (
            Allocation.objects
            .select_related('business_unit', 'name')   # 'name' = Fund FK (if you need it)
            .filter(business_unit__in=bu_qs)
            .order_by('business_unit__business_unit_name', 'id')
        )

        # If you want exactly the same shape you had:
        data = [
            {
                "id": a.id,
                "business_unit_name": a.business_unit.business_unit_name,
                "business_unit_id": a.business_unit_id,
                "allocated_amount": a.amount,
            }
            for a in allocations
        ]
        return Response(data, status=status.HTTP_200_OK)


class Allocation_Log_Per_BU_View(APIView):
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        # If Fund <-> User is M2M, use fund_set; if it’s FK(Fund.user), swap to Fund.objects.filter(user=request.user)
        fund_ids = list(request.user.fund_set.values_list('id', flat=True))
        if not fund_ids:
            return Response([], status=status.HTTP_200_OK)

        # Logs for allocations whose Fund (Allocation.name) is in the user’s funds
        logs = (
            AllocationLog.objects
            .select_related(
                'allocation',
                'allocation__business_unit',
                'allocation__name'  # Fund FK, commonly named "name"
            )
            .filter(allocation__name_id__in=fund_ids)
            .order_by('-id')
        )

        # Shape matches your previous structure but pulls BU/Fund from the related Allocation
        data = [{
            'id': log.id,
            'business_unit_name': getattr(log.allocation.business_unit, 'business_unit_name', str(log.allocation.business_unit)),
            'business_unit_id': getattr(log.allocation.business_unit, 'id', None),
            'allocation_name': getattr(log.allocation.name, 'name', str(log.allocation.name)),  # Fund name
            'amount': log.amount,
        } for log in logs]

        return Response(data, status=status.HTTP_200_OK)

