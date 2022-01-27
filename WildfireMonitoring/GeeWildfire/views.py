from django.http import HttpResponse, JsonResponse

# generic base view
from django.views.decorators.http import require_http_methods

# gee
import ee

ee.Initialize()

@require_http_methods(["GET"])
def wmts_link_gee(request):
    # select the Dataset Here's used the MODIS data
    dataset = (ee.ImageCollection('MODIS/006/MOD13Q1')
               .filter(ee.Filter.date('2019-07-01', '2019-11-30'))
               .first())
    modisndvi = dataset.select('NDVI')

    # Styling
    vis_paramsNDVI = {
        'min': 0,
        'max': 9000,
        'palette': ['FE8374', 'C0E5DE', '3A837C', '034B48', ]}

    # add the map to the the folium map
    map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
    url = map_id_dict['tile_fetcher'].url_format
    return JsonResponse({'wmts_link': url})