from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .forms import *
import re
from django.utils.html import escape

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        user = request.user
        gm_list = GameMaster.objects.filter(user=request.user)
        campaign_list = list()
        for gm in gm_list:
            campaign_list.append(gm.campaign)
        context = {
            'user': user,
            'campaign_list': campaign_list,
        }
    else:
        user = False
        context = {
            'user': user,
        }
    return render(request, 'worldbuilder/index.html', context)


def campaign(request,campaign_id):
    if request.user.is_authenticated:
        try:
            gm = GameMaster.objects.get(campaign=campaign_id,user=request.user)
        except ObjectDoesNotExist:
            context = {
            }
            return render(request, 'worldbuilder/index.html', context)
        if gm:
            campaign = gm.campaign
            nodes = Area.objects.filter(campaign=campaign)
            context= {
                'campaign': campaign,
                'nodes': nodes,
            }
            return render(request, 'worldbuilder/campaign.html', context)

    else:
        context = {

        }
        return render(request, 'worldbuilder/index.html',context)


def area(request, area_id):
    if request.user.is_authenticated:
        area = Area.objects.get(id=area_id)
        try:
            campaign=area.campaign
            gm = GameMaster.objects.get(campaign=campaign,user=request.user)
        except ObjectDoesNotExist:
            context = {}
            return render(request, 'worldbuilder/index.html', context)
        except MultipleObjectsReturned:
            context = {}
            return render(request, 'worldbuilder/index.html', context)
        if gm:
            area_notes = escape(area.notes)
            area_notes = markup_area_links(area_notes, area)
            area_notes = markup_dice_rolls(area_notes)
            area_notes = markup_read_aloud(area_notes)

            area_description = escape(area.description)
            area_description = markup_area_links(area_description, area)
            area_description = markup_dice_rolls(area_description)
            area_description = markup_read_aloud(area_description)

            context= {
                'campaign': campaign,
                'area': area,
                'area_notes': area_notes,
                'area_description': area_description,
            }
            return render(request, 'worldbuilder/area.html', context)

    else:
        context = {
        }
        return render(request, 'worldbuilder/index.html',context)


def new_campaign(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = CampaignForm(request.POST)

            if form.is_valid():
                campaign = Campaign(
                    name = form.cleaned_data['name'],
                    description = form.cleaned_data['description'],
                )
                campaign.save()
                gm = GameMaster(
                    campaign = campaign,
                    user = request.user,
                )
                gm.save()
                return redirect('/worldbuilder')
        else:
            form = CampaignForm()
            context = {
                'form': form,
            }
        return render(request, 'worldbuilder/new_campaign.html', context)

    else:
        return redirect('/accounts/login')


def new_area(request,campaign_id):
    if request.user.is_authenticated():
        campaign = Campaign.objects.get(id=campaign_id)
        gms = GameMaster.objects.filter(campaign=campaign_id)
        try:
            gms.get(user=request.user)
        except:
            return redirect('worldbuilder/')
        area_list = Area.objects.filter(campaign=campaign_id)
        if request.method == 'POST':
            area_form = AreaForm(request.POST, campaign=campaign_id)

            if area_form.is_valid():
                area = Area(
                    code = area_form.cleaned_data['code'],
                    name = area_form.cleaned_data['name'],
                    description = area_form.cleaned_data['description'],
                    notes = area_form.cleaned_data['notes'],
                    parent = area_form.cleaned_data['parent'],
                    campaign = campaign,
                )
                area.save()

                return redirect('/worldbuilder/campaign/' + campaign_id)
        else:
            area_form = AreaForm(campaign=campaign_id)
            campaign = Campaign.objects.get(id=campaign_id)
            context = {
                'area_form': area_form,
                'campaign': campaign,
                'area_list': area_list,
            }
            return render(request, 'worldbuilder/new_area.html', context)
    else:
        return redirect('accounts/login')


def edit_campaign(request,campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    if request.user.is_authenticated():
        try:
            GameMaster.objects.get(campaign=campaign_id,user=request.user)
        except ObjectDoesNotExist:
            return render(request, 'worldbuilder/index.html', {})
        except MultipleObjectsReturned:
            print('MultipleObjectsReturned error, check database')
            return render(request, 'worldbuilder/index.html', {})
        if request.method == 'POST':
            form = CampaignForm(request.POST, instance=campaign)

            if form.is_valid():
                form.save()
                return redirect('/worldbuilder')
        else:
            form = CampaignForm(instance=campaign)
            context = {
                'form': form,
                'campaign': campaign,
            }
        return render(request, 'worldbuilder/new_campaign.html', context)


def edit_area(request,area_id):
    area = Area.objects.get(id=area_id)
    try:
        campaign = area.campaign
        GameMaster.objects.get(campaign=campaign, user=request.user)
        area_list = Area.objects.filter(campaign=campaign)
        # children = area.get_descendants()
        # child_ids = []
        # for child in children:
        #     child_ids.append(child.id)
        # area_list = area_list.exclude(id__in=child_ids)
    except ObjectDoesNotExist:
        return render(request, 'worldbuilder/index.html', {})
    except MultipleObjectsReturned:
        print('MultipleObjectsReturned error, check database')
        return render(request, 'worldbuilder/index.html', {})
    if request.method == 'POST':
        area_form = AreaForm(request.POST, instance=area, campaign=campaign)

        if area_form.is_valid():
            area_form.save()
            return redirect('/worldbuilder/area/' + area_id)
    else:
        area_form = AreaForm(instance=area, campaign=campaign)
        context = {
            'area_form': area_form,
            'area': area,
            'area_list': area_list,
        }
    return render(request, 'worldbuilder/new_area.html', context)


def delete_campaign(request,campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    if request.user.is_authenticated():
        try:
            GameMaster.objects.get(campaign=campaign_id, user=request.user)
        except ObjectDoesNotExist:
            return render(request, 'worldbuilder/index.html', {})
        if request.method == 'POST':
            campaign.delete()
            return redirect('/worldbuilder/')
        else:
            nodes = Area.objects.filter(campaign=campaign)
            context = {
                'campaign': campaign,
                'purpose': 'delete',
                'nodes': nodes,
            }
    return render(request, 'worldbuilder/campaign.html', context)


def delete_area(request, area_id):
    area = Area.objects.get(id=area_id)
    if request.user.is_authenticated():
        try:
            campaign = area.campaign
            GameMaster.objects.get(campaign=campaign, user=request.user)
        except ObjectDoesNotExist:
            return render(request, 'worldbuilder/index.html', {})
        except MultipleObjectsReturned:
            print('MultipleObjectsReturned error, check database')
            return render(request, 'worldbuilder/index.html', {})
        if request.method == 'POST':
            area.delete()
            return redirect('/worldbuilder/campaign/' + str(campaign.id))
        else:
            area_notes = escape(area.notes)
            area_notes = markup_area_links(area_notes, area)
            area_notes = markup_dice_rolls(area_notes)
            area_notes = markup_read_aloud(area_notes)

            area_description = escape(area.description)
            area_description = markup_area_links(area_description, area)
            area_description = markup_dice_rolls(area_description)
            area_description = markup_read_aloud(area_description)

            context = {
                'campaign': campaign,
                'area': area,
                'area_notes': area_notes,
                'area_description': area_description,
                'purpose': 'delete',
            }
    return render(request, 'worldbuilder/area.html', context)


#TODO: Move following functions to separate file
def markup_area_links(text, area):
    text = re.split('(area\s*[\w]+)', text, flags=re.IGNORECASE)
    for i, val in enumerate(text):
        area_match = re.fullmatch('(area\s*)([\w]+)', val, flags=re.IGNORECASE)
        if area_match:
            try:
                connected_area = Area.objects.get(code__iexact=area_match.group(2), campaign=area.campaign)
                text[i] = '<a href="/worldbuilder/area/' + str(connected_area.id) + '">' + area_match.group(
                    0) + '</a>'
            except:
                pass
    return ''.join(text)


def markup_read_aloud(text):
    text = re.split('(---.*?\---)', text, flags=re.DOTALL)
    for i, val in enumerate(text):
        read_aloud = re.fullmatch('((---)(.*?)(---))', val, flags=re.DOTALL)
        if read_aloud:
            text[i] = '<div class="readAloud">' + read_aloud.group(3) + '</div>'
    return ''.join(text)


def markup_dice_rolls(text):
    text = re.split('(\d+d\d+)', text, flags=re.IGNORECASE)
    for i, val in enumerate(text):
        dice_match = re.fullmatch('(\d+d\d+)', val, flags=re.IGNORECASE)
        if dice_match:
            text[i] = '<span class="diceRoll">' + val + '</span>'
    return ''.join(text)