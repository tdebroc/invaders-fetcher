import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import xmltodict
import urllib.request

mids = ["", "1PRXB3K_wJvCA3c-8w3rILLu6BiRM2_9B",  # 1
        "1dEe2YCPmt-HDHUSNpDQVfrWGV3ENvPMg",  # 2
        "1w-bp3Ivpaoexjyff_pYR-Fy-QiDBUPaM",  # 3
        "1lad_U6wIWr-R9Xd97HcZUmfWIpX-r3sb",  # 4
        "108EQXTIbix9zMTDMgK2rBgRjul0Rebe1",  # 5
        "1o897-QhQkXk0yxli-258R50Zrsm1wLSe",
        "17B3f6d30LU4WG-WLk91kQALFlUQMwQ2U",
        "19iCehPZ1DLcL5b3ZXjc6bqXgXcXkWR9V",
        "1pUpM8_XbrmAkIQdYQAhTog7oCMUZOZDw",
        "1qM97n9VLQipXee7m9VRhEZhQNr3OTUVL",  # 10
        "1lY0hDG3ttyzJYY9m_276f8Pl2npDJivu",
        "1Uj-nH43W18ZRxj4Jl9Fugjf32LVNDia1",
        "1RZ1A8iQkeqLP3SKGA3ixt92JWLCoZ8xv",
        "1ZMmqPoW0DF2LvND08hoDFihNGaWA-k9o",
        "1sqScjE3S3ddHGVbNOMMS9HM96nGeMYAf",  # 15
        "1U5EA66HKIqaki60SBlp2YHgDv-CmjJEL",
        "1aE3Zeyt8KSTAJE8jnjXJEpjAEExMLjEE",
        "1DpJSVawRwy3hAcelr3xl91MEY9R6esrd",
        "10r0LyJ6_GSBg2o9fqSFqux0O64ZSWUuJ",
        "14__VE8rqrHVSFAvKlKhDCWClo_CNVxNT"]

VISITED_COLOR = "0288D1"
DESTROYED_COLOR = "A52714"
FILTER_COLORS = [VISITED_COLOR, DESTROYED_COLOR]
OneKM = 122798


class GmapDirectionBuilder:

    def __init__(self):
        self.curr_url = "https://www.google.com/maps/dir/"
        self.count = 0

    def add_pos(self, loc):
        adress = loc["latitude"] + "," + loc["longitude"]
        if self.count < 20:
            self.curr_url = self.curr_url + adress + "/"

        self.count = self.count + 1




def calculate_arr(i):
    mid = mids[i]
    print("## Arrondissement " + str(i))
    url = "https://www.google.com/maps/d/u/0/kml?hl=en&mid=" + mid + "&forcekml=1&cid=mp"
    xml_data = urllib.request.urlopen(url).read().decode("utf-8")

    def getXYFromPlace(coord_string):
        coords = coord_string.split(",")
        x = int(float(coords[0]) * 10 * 1000 * 1000)
        y = int(float(coords[1]) * 10 * 1000 * 1000)
        return (x, y)

    invader_to_loc = {}
    my_dict = xmltodict.parse(xml_data)
    all_places = my_dict["kml"]["Document"]["Folder"]["Placemark"]
    map_name = my_dict["kml"]["Document"]["name"]
    locations = []
    places_names = []
    for place in all_places:
        place_color = place["styleUrl"].split("-")[2]
        if place_color in FILTER_COLORS:
            continue
        coords = getXYFromPlace(place["Point"]["coordinates"])
        locations.append(coords)
        places_names.append(place["name"])
        invader_to_loc[place["name"]] = {
            "latitude": place["Point"]["coordinates"].split(",")[1],
            "longitude": place["Point"]["coordinates"].split(",")[0]
        }
    print("There is", len(places_names), "invaders to catch in " + str(map_name.replace(".kml", "")) + ".")

    def create_data_model():
        """Stores the data for the problem."""
        data = {}
        # Locations in block units
        data['locations'] = locations  # yapf: disable
        data['num_vehicles'] = 1
        data['depot'] = 0
        return data

    def compute_euclidean_distance_matrix(locations):
        """Creates callback to return distance between points."""
        distances = {}
        for from_counter, from_node in enumerate(locations):
            distances[from_counter] = {}
            for to_counter, to_node in enumerate(locations):
                if from_counter == to_counter:
                    distances[from_counter][to_counter] = 0
                else:
                    # Euclidean distance
                    distances[from_counter][to_counter] = (int(
                        math.hypot((from_node[0] - to_node[0]),
                                   (from_node[1] - to_node[1]))))
        return distances

    matrix = compute_euclidean_distance_matrix(locations)
    distance_matrix = compute_euclidean_distance_matrix(locations)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    data = create_data_model()
    data["distance_matrix"] = matrix
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    def print_solution(manager, routing, solution):

        """Prints solution on console."""
        # print('Objective: {} miles'.format(solution.ObjectiveValue()))
        gmapDirectionBuilder = GmapDirectionBuilder()
        index = routing.Start(0)
        plan_output = 'Route for vehicle 0:\n'
        route_distance = 0
        places_in_order = []
        while not routing.IsEnd(index):
            plan_output += ' {} ->'.format(manager.IndexToNode(index))
            previous_index = index
            places_in_order.append(places_names[index])

            loc = invader_to_loc[places_names[index]]
            gmapDirectionBuilder.add_pos(loc)

            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

        plan_output += ' {}\n'.format(manager.IndexToNode(index))
        # print(plan_output)
        plan_output += 'Route distance: {}miles\n'.format(route_distance)
        walk_in_km = int(route_distance / OneKM)

        print("Optimal route for invaders is: ")
        print(" -> ".join(places_in_order))
        print("Walk is ", walk_in_km, " KM")
        print("Gmap directions: ", gmapDirectionBuilder.curr_url)
        print("Density is : " + str(round(len(places_names) / walk_in_km, 1)))
        print("")


    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(manager, routing, solution)


calculate_arr(17)
# for i in range(1, 20):
#    calculate_arr(i)
# http://maps.google.com/maps?saddr=48.8668569,2.3534702&daddr=48.8647176,2.3533964+to:48.8647267,2.3543965
