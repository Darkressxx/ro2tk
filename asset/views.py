# Template rendering
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Sum

# Staff permission
from django.contrib.admin.views.decorators import staff_member_required

# App models
from niceboat.models import NiceBoatSkill, NiceBoatMP, RandomSet, ItemSet

# Cache framework
from django.core.cache import cache

# UTF8 open
import codecs

def iRO2status(request):
	import socket
	import time

	server_list = [
		['patch.playragnarok2.com', 80, 'Patch'],
		['login.playragnarok2.com', 7101, 'Login'],
		['128.241.94.47', 7204, 'Odin'],
		['128.241.94.49', 7204, 'Freyja'],
		#['66.151.147.235', 80, 'Patch'],
		#['128.241.94.35', 7101, 'Login'],
		#['128.241.94.54', 7402, 'Message'],
		#['128.241.94.42', 7202, 'Odin'],
		#['195.154.67.171', 7202, 'Freyja'],
		#['128.241.94.43', 7207, 'WoE Channel'],
		#['128.241.95.23', 7201, 'Test Server #1'],
		#['128.241.95.24', 7201, 'Test Server #2'],
	]

	cache_key = 'server_response_cached'
	cache_time = 30 # Cache seconds.
	result = cache.get(cache_key)

	if not result:
		server_response = []
		for server in server_list:
			try:
				sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				sock.settimeout(5) # Maximum seconds before considered offline.
				t1=time.time() # Time before connection.
				sock.connect( (server[0],server[1]) ) # Connect to server.
				t2=time.time() # Time after connection.
				t = round(t2-t1, 5) # Calculate and round ping time.
				if t < 0.5:
					server_response.append('<li class="list-group-item"><img class="icon" src="/files/img/' + server[2] + '.png">' + server[2] + ' is <strong>Online</strong></li>')
				elif t >= 0.5:
					server_response.append('<li class="list-group-item list-group-item-warning"><img class="icon" src="/files/img/' + server[2] + '.png">' + server[2] + ' is <strong>Slow</strong></li>')
			except socket.error as msg:
				server_response.append('<li class="list-group-item list-group-item-danger"><img class="icon" src="/files/img/' + server[2] + '.png">' + server[2] + ' is <strong>Offline</strong></li>')
			sock.close()
		result = ''.join(server_response)
		cache.set(cache_key, result, cache_time)

	return render(request, 'iRO2status.html', {'result': result})

def niceboat(request):
	return render(request, 'niceboat.html',)

def mp(request):
	# Get the MP table
	masterpoints = NiceBoatMP.objects.all().order_by("level")

	return render(request, 'mp.html', {'masterpoints': masterpoints})

def random(request, requested_page=1):
	""" List random sets. """

	query = request.GET.get('search', '')

	sets = RandomSet.objects.filter(name__icontains=query)

	# Configure pagination.
	pages = Paginator(sets, 20)

	try:
		"""Get requested page."""
		returned_page = pages.page(requested_page)
	except PageNotAnInteger:
		"""If the page is not an integer, go to page 1."""
		returned_page = pages.page(1)
	except EmptyPage:
		"""If the page is empty, go to last page."""
		returned_page = pages.page(pages.num_pages)

	return render(request, "random.html", {'sets': returned_page.object_list, 'page': returned_page})

@staff_member_required
def update(request):

	########
	# Sets #
	########

	try:
		""" Open UTF8 converted item list. """
		f = codecs.open("niceboat/static/iRO2/ItemInfo.csv", "r", "utf-8")
	except:
		return HttpResponse('ItemInfo.csv not found.')

	lineskip = 2
	item_dup = []
	rng_dup = []

	for line in f:
		if lineskip:
			""" Skip lines. """
			lineskip = lineskip - 1
			continue

		line = line.split('\t')

		server = int(line[2])

		# Skip sets from other servers.
		if not (server & 4):
			continue

		set = RandomSet()

		set.itemid = int(line[0])

		# Skip duplicate item ids.
		if set.itemid in item_dup:
			continue
		else:
			item_dup.append(set.itemid)

		set.randomsetid = int(line[27])

		# Skip non-existent or duplicate sets.
		if not set.randomsetid:
			continue
		elif set.randomsetid in rng_dup:
			continue
		else:
			rng_dup.append(set.randomsetid)

		nameid = int(line[44])
		descid = int(line[45])

		set.grade = int(line[6])
		set.icon = str(line[52])

		# Set icon path.
		if 'null' in set.icon:
			continue
		set.icon = 'iRO2' + set.icon[1:].replace('.dds', '.png').replace('\\', '/').lower()

		try:
			""" Open UTF8 converted item name translation. """
			t = codecs.open("niceboat/static/iRO2/string_item_name.tbl", "r", "utf-8")
		except:
			return HttpResponse('string_item_name.tbl not found.')
		for tline in t:
			if str(nameid) in tline:
				tline = tline.split('\t')
				set.name = tline[1]
		t.close

		# Set name blacklist.
		if not set.name:
			continue
		elif 'No' and 'Trans' and 'ID' in set.name:
			continue
		elif 'Cat' and 'Mask' in set.name:
			continue
		elif 'Dye' in set.name:
			continue
		elif 'White' and 'Tiger' in set.name:
			continue
		elif 'DNA' and 'Fragment' in set.name:
			continue
		elif 'DNA' and 'fragment' in set.name:
			continue

		try:
			""" Open UTF8 converted item description translation. """
			d = codecs.open("niceboat/static/iRO2/string_item_description.tbl", "r", "utf-8")
		except:
			return HttpResponse('string_item_description.tbl not found.')
		for dline in d:
			if str(descid) in dline:
				dline = dline.split('\t')
				set.desc = dline[1][:1000]
				set.desc = set.desc.replace('\\n', '\n')
				set.desc = set.desc.replace('\\r', '\n')
				set.desc = set.desc.strip('"')
		d.close

		# Set description blacklist.
		if not set.desc:
			continue
		elif 'No' and 'Trans' and 'ID' in set.desc:
			continue
		set.save()
	f.close

	#########
	# Items #
	#########

	try:
		""" Open UTF8 converted item list. """
		r = codecs.open("niceboat/static/iRO2/RandomSet.csv", "r", "utf-8")
	except:
		return HttpResponse('RandomSet.csv not found.')

	lineskip = 2
	item_dup = []

	for line in r:
		if lineskip:
			""" Skip lines. """
			lineskip = lineskip - 1
			continue

		line = line.split('\t')

		server = int(line[8])

		# Skip items from other servers.
		if not (server & 4):
			continue

		item = ItemSet()

		try:
			""" Get Random Set model related to the item. """
			item.randomset = RandomSet.objects.get(pk=int(line[0]))
		except:
			continue

		nameid = int(line[2])
		item.ratio = int(line[5])

		if nameid in item_dup:
			item_dup[(nameid)]
		else:
			item_dup.append((nameid, item.ratio))

		try:
			""" Open UTF8 converted item name translation. """
			rn = codecs.open("niceboat/static/iRO2/string_item_name.tbl", "r", "utf-8")
		except:
			return HttpResponse('string_item_name.tbl not found.')
		for rnline in rn:
			if str(nameid) in rnline:
				rnline = rnline.split('\t')
				item.name = rnline[1]
		rn.close

		try:
			""" Open UTF8 converted item description translation. """
			rd = codecs.open("niceboat/static/iRO2/string_item_description.tbl", "r", "utf-8")
		except:
			return HttpResponse('string_item_description.tbl not found.')
		for rdline in rd:
			if str(nameid) in rdline:
				rdline = rdline.split('\t')
				item.desc = rdline[1][:250]
				item.desc = item.desc.replace('\\n', '\n')
				item.desc = item.desc.replace('\\r', '\n')
				item.desc = item.desc.strip('"')
				if item.desc == '0':
					item.desc = 'No description for this item.'
		rd.close

		item.save()
	r.close

	#########
	# Ratio #
	#########

	for set in RandomSet.objects.all():
		items = ItemSet.objects.filter(randomset=set.pk)

		# Sum of all the ratios.
		ratio_total = items.aggregate(Sum('ratio'))

		for item in items:
			item.ratio = (float(item.ratio) / float(ratio_total['ratio__sum'])) * 100
			item.ratio = round(item.ratio, 5)
			item.save()

	#item.ml = int(line[15])
	#item.job = int(line[17])
	#item.type = int(line[18])
	#item.slot = int(line[19])
	#item.weaponid = int(line[21])
	#item.armorid = int(line[22])
	#item.socketid = int(line[28])

	return HttpResponse('Random Set update successful.')
