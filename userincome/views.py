from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Source, UserIncome
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse , HttpResponse
import json
from userpreferences.models import UserPreference
import datetime
import csv
import xlwt

from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile
from django.db.models import Sum


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get("searchText")

        income = UserIncome.objects.filter(
            amount__startswith = search_str, owner=request.user) | UserIncome.objects.filter(
            date__startswith = search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains = search_str, owner=request.user)| UserIncome.objects.filter(
            source__icontains = search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)





@login_required(login_url='/authentication/login/')

def index(request):
    source = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'source': source,
        'page_obj': page_obj,
        'currency': currency,
    }

    return render(request, 'income/index.html', context)

def add_income(request):
    source = Source.objects.all()
    context = {
        'source': source,
        'values': request.POST
        }
    if request.method == 'GET':
        return render(request,"income/add_income.html", context)
    if request.method =='POST':
        amount = request.POST['amount']
        if  not amount:
            messages.error(request, 'Miqdor talab qilinadi')
            return render(request,"income/add_income.html", context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if  not description:
            messages.error(request, 'tavsifi talab qilinadi')
            return render(request,"income/add_income.html", context)
        UserIncome.objects.create(owner=request.user, amount=amount, description=description, date=date, source=source)
        messages.success(request, 'Yozib olish muvaffaqiyatli tejaldi')

        return redirect('income')
    
@login_required(login_url='/authentication/login/')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    source = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'source': source
    }
        
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        if  not amount:
            messages.error(request, 'Miqdor talab qilinadi')
            return render(request,"income/edit-income.html", context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if  not description:
            messages.error(request, 'tavsifi talab qilinadi')
            return render(request,"income/edit-income.html", context)

        income.owner = request.user
        income.amount=amount
        income.date=date
        income.source=source
        income.description=description
        income.save()
        messages.success(request, 'Yozib olish muvaffaqiyatli yangilandi')

        return redirect('income')

        messages.info(request, 'Handling post form')
        return render(request, 'income/edit-income.html', context)



def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'daromad olib tashlandi')
    return redirect("income")



def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    income = UserIncome.objects.filter(owner = request.user,
        date__gte = six_months_ago, date__lte = todays_date
    )
    finalrep = {}

    def get_income(income):
        return income.source
    
    source_list = map(get_income, income)

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = income.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount
    
    for x in income:
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)
    return JsonResponse({'income_source_date': finalrep}, safe=False)



def stats_viewIncome(request):
    return render(request, 'income/stats.html')



def export_csv(request):


    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'source', 'Date'])

    expenses = UserIncome.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount,
                         expense.description,
                         expense.source,
                         expense.date])
        
    return response



def export_excel(request):
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=UserIncome' + str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('income')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'source', 'Date']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = UserIncome.objects.filter(owner=request.user).values_list(
        'amount', 'description','source', 'date'
    )

    for row in rows:
        row_num +=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response

def export_pdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Income' + str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    income = UserIncome.objects.filter(owner=request.user)

    sum = income.aaggregate(Sum('amount'))

    html_string = render_to_string(
        'income/pdf-output.html', {'income': income, 'total': sum}
    )
    # html = HTML(string=html_string)
    # result = html_string.write_pdf()

    # with tempfile.NamedTemporaryFile(delete=True) as output:
    #     output.write(result)
    #     output.flush()
    #     output = open(output.name, 'rb')
    #     response.write(output.read())

    return response

    
