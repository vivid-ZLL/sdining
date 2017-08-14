from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from business.models import Business, Food
from .models import Order


@login_required(login_url='/')
def makeorder(request):
    try:
        request.session['order'] = request.session['order']
    except:
        request.session['order'] = {}
    foodpk = request.POST.get('foodpk', False)
    businesspk = request.POST.get('businesspk', False)
    num = request.POST.get('num', False)

    def check_attr():
        try:
            f = int(foodpk)
            b = int(businesspk)
            n = int(num)
        except:
            return False

        if f in Food.objects.values_list('pk', flat=True) and b in Business.objects.values_list('pk',
                                                                                                flat=True) and n == 1:
            return True
        else:
            return False

    request.session['order'].update({'business': businesspk, foodpk: num})
    s = check_attr()
    if s:
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


@login_required(login_url='/')
def removeorder(request):
    try:
        request.session['order'] = request.session['order']
    except:
        request.session['order'] = {}
    foodpk = request.POST.get('foodpk', False)
    businesspk = request.POST.get('businesspk', False)

    def check_attr():
        try:
            b = int(businesspk)
            f = int(foodpk)
        except:
            return False

        if f in Food.objects.values_list('pk', flat=True) and b in Business.objects.values_list('pk', flat=True):
            return True
        else:
            return False

    del request.session['order'][foodpk]
    s = check_attr()
    if s:
        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


class ShowOrderView(LoginRequiredMixin, TemplateView):
    login_url = '/'

    template_name = 'operation/order.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        try:
            orderdic = request.session['order']
        except:
            return HttpResponseNotFound("您还未点餐")
        food_list = []
        psum = 0
        for fpk in orderdic.keys():
            if fpk == 'business':
                bpk = orderdic['business']
            else:
                try:
                    f = Food.objects.get(pk=fpk)
                    food_list.append(f)
                    psum = psum + f.price
                except:
                    return HttpResponseNotFound()
        context['food_list'] = food_list
        context['pricesum'] = psum
        context['businesspk'] = bpk
        return self.render_to_response(context)

    def post(self, request):
        if not request.user.usertype:
            return JsonResponse({'status': 2})
        confirm = request.POST.get('confirm', False)
        if confirm:
            try:
                orderdic = request.session['order']
            except:
                return HttpResponseNotFound("您还未点餐")
            print(orderdic)
            try:
                for fpk in orderdic.keys():
                    if fpk == 'business':
                        b = Business.objects.get(pk=orderdic['business'])
                        if not b.is_open:
                            return JsonResponse({'status': 0})
                    else:
                        f = Food.objects.get(pk=fpk)
                        Order.objects.create(user=request.user, food=f)
            except:
                return JsonResponse({'status': 0})
            return JsonResponse({'status': 1})
        else:
            return JsonResponse({'status': 0})
