import calendar
import json
import requests
import os
from src.service.logger import logger
from src.constants.constants import API_UPFLUX_UNITS, MAX_LIMIT_CATEGORIES, URL_UPFLUX, FILE_PATH
from utils.utils_json import read_qa_json, update_dates_in_json
from src.utils.utils_path import find_git_root, api_src_by_repo_root, guarantee_sys_path


class UpFluxAPIConnector:
    def __init__(self, url, bearer, group_id, mode="get_request_specific_component"):
        self.url = url
        self.mode = mode

        if self.url is None:  # Init
            self.url = URL_UPFLUX

        self.headers = {
            "Content-Type": "application/json",
            "GroupId": group_id,
            "Processid": "",
            "Authorization": bearer
        }

    def _set_bearer(self, bearer):
        self.headers["Authorization"] = bearer

    def _get_agci_filters_from_upflux_format(self, api_upflux_filters, DATE):
        """
        Funtion to translate filters from API Upflux format to AGCI format
        Args:
            api_upflux_filters: Filters in API Upflux format

        Returns:
            context_filters: Filters in AGCI Format

        """

        # Dictionary containing operators for each filter type
        dict_upflux_operators = {
            "time": {
                # Operators
                "cropa": "limitar casos",
                "int": "casos interligados",
                "cc": "casos contidos",
                "cropastart": "limitar casos iniciados",
                "cropaend": "limitar casos finalizados",
                "start": "casos iniciados",
                "end": "casos finalizados",
            },
            "attribute": {
                # Operators
                "selectonly": "selecionar somente",
                "man": "casos que contém",
                # "falta": "casos contidos",
                # "falta": "limitar casos",
                "except":"exceto"
            }
        }

        context_filters = []
        for filter_dict in api_upflux_filters:
            # Time Filter
            if filter_dict["Id"] == "time":
                mode_upflux = filter_dict["Operator"]
                context_filters.append({
                    "type": "tempo",
                    "mode": dict_upflux_operators["time"][mode_upflux],
                    "DATE": DATE,
                    "start_date": filter_dict["Start"][0:10],
                    "end_date": filter_dict["End"][0:10],
                })

            # Attribute Filter
            if filter_dict["Id"] == "attr":
                mode_upflux = filter_dict["Operator"]
                context_filters.append({
                    "type": "atributo",
                    "mode": dict_upflux_operators["attribute"][mode_upflux],
                    "attribute_key": filter_dict["Attribute"],
                    "attribute_value": filter_dict["Data"],
                })

        return context_filters

    def _postprocess_filters(self, filters, DATE):
        """
        Function to translate dashboard filters and component filters in Upflux
        Format into Agci Filters
        Args:
            filters: Filters in API Upflux format

        Returns:
            all_filters_agci:  Filters in AGCI Format

        """
        all_filters_agci = []

        # postprocess dashboard filters
        if "dashboard_filters" in filters:
            dashboard_filters_upflux = json.loads(filters["dashboard_filters"])
            dashboard_filters_agci = self._get_agci_filters_from_upflux_format(dashboard_filters_upflux, DATE)
            all_filters_agci = all_filters_agci + dashboard_filters_agci

        # postprocess component filters
        if "component_filters" in filters:
            component_filters_upflux = json.loads(filters["component_filters"])
            component_filters_agci = self._get_agci_filters_from_upflux_format(component_filters_upflux, DATE)
            all_filters_agci = all_filters_agci + component_filters_agci

        return all_filters_agci

    def _pos_process(self, answer, DATE, after_posprocess_unit, api_upflux_unit):
        """
        Processes the given answer based on specified date parameters.

        This method takes an answer list and parameters dictionary as input.
        It processes the answer based on the date requirements specified in parameters.
        The method supports processing for a single date or a date range.

        Parameters:
        answer (list): A list of tuples where each tuple contains a date and its associated value.
        parameters (dict): A dictionary containing date-related keys like 'DATE', 'STARTDATE', or 'ENDDATE'.

        Returns:
        object: The processed answer based on the date parameters.
        Returns None if the specified date is not found.
        """
        # Retrieve the target date or date range from parameters
        answer_return = answer
        if isinstance(answer_return, list):
            date_target = self._get_date(DATE)
            change_units = False
            if after_posprocess_unit != api_upflux_unit:
                change_units = True
            # Processing for a single date
            if "DATE" in date_target:
                # Default None when the date is not found
                #answer_return = None
                for item in answer:
                    if change_units:
                        if item.get("label") == date_target["DATE"]:
                            answer_return = item["porcentagem"]
                            break
                    else:
                        # MARCOS
                        # Protection from Bug if item values are Bins type
                        if isinstance(item, list):
                            if item[0]== date_target["DATE"]:
                                answer_return = item[1]
                            elif len(answer) == 1:
                                answer_return = answer
            # Processing for a date range
            elif "STARTDATE" in date_target:
                pos_s = None
                pos_f = None
                i = 0
                for item in answer:
                    if change_units:
                        if item.get("label") == date_target["STARTDATE"]:
                            pos_s = i
                        elif item.get("label") == date_target["ENDDATE"]:
                            pos_f = i     # Includes 'ENDDATE' in the slice
                    else:
                        if item[0] == date_target["STARTDATE"]:
                            pos_s = i
                        elif item[0] == date_target["ENDDATE"]:
                            pos_f = i     # Includes 'ENDDATE' in the slice
                    i += 1
                if (pos_s is not None) and (pos_f is not None):
                    answer_return = answer[pos_s:pos_f+ 1]

        return answer_return

    def _postprocess_complex_bar_graph(self, answer, context_num):
        "A complex graph is a bar that have more than one bar"
        total = answer[0]["RelativeValuesTotal"][0]
        bar_graph_by_context = {
            "2": "itens_com_atraso",
            "3": "Atraso",
            "4": "OV Perfect",
            "5": "Atraso"
        }

        list1= answer[0]["Data"]

        # Remove if more than 10 elements
        list1 = list1[0:min([MAX_LIMIT_CATEGORIES,len(list1)])]

        # Format response
        categories = {elem[0]:{
            "Subtotal_de_itens":elem[1],
            "porcentagem_em_relação_do_total": str(round((elem[1]/total)*100,2)).replace(".",","),
            "porcentagem_" + bar_graph_by_context[context_num] +"_na_categoria": str(round(elem[2],2)).replace(".",","),
            bar_graph_by_context[context_num] +"_na_categoria": (elem[2] / 100) * elem[1],
            } for elem in list1}

        categories = {key: f"{category['Subtotal_de_itens']} itens ({category['porcentagem_em_relação_do_total']}% do total de itens). "+
					   f"A porcentagem de atraso nesses items é de {category['porcentagem_itens_com_atraso_na_categoria']}% "+
					   f"({category['itens_com_atraso_na_categoria']} itens)." for key, category in categories.items()}


        answer = {"Total de itens": total, "Por categorias": categories}

        return answer

    def _postprocess_answer(self, answer, after_posprocess_unit, api_upflux_unit, context_num):
        if ("Data" in answer[0].keys()) and (answer[0]["Data"] != []):
            # When it returns more than two elements in Data
            if len(answer[0]["Data"][0]) > 2:
                answer = self._postprocess_complex_bar_graph(answer, context_num)

            # Only return one or two values in Data
            else:
                # We get absolute value when we have to convert units to percentage
                absolute = float(answer[0]["AbsoluteValuesTotal"][0]) if ("AbsoluteValuesTotal" in answer[0].keys()
                                                                          and answer[0]["AbsoluteValuesTotal"]) else None
                answer = answer[0]["Data"]
                # # Convert
                if after_posprocess_unit != api_upflux_unit:
                    #  from unit                              to unit
                    if api_upflux_unit =="minutos" and after_posprocess_unit == "dias":
                        answer = float(answer[0][0])/(60*24)

                    #  from unit                                to unit
                    if api_upflux_unit == "unidades" and after_posprocess_unit == "porcentagem":
                        # It is a simple bar as template079 Status Recebimento
                        answer = [{"label":value[0], "reais":value[1], "porcentagem":str(round(value[1]*100/absolute,2))+"%"} for value in answer]


        elif ("Bins" in answer[0].keys()) and (answer[0]["Bins"] is not None):
            answer = answer[0]["Bins"]

            # MARCOS
            # Obtain total values and convert minutes to days when the answer are Bins
            # if id_question == "f_o2c_t049" or id_question == "f_o2c_t050" or id_question == "f_o2c_t076" or id_question == "f_o2c_t077":
            total = 0
            for item in answer:
                total += item["Count"]
                item["Range"]["Min"] = item["Range"]["Min"] / 60 / 24
                item["Range"]["Max"] = item["Range"]["Max"] / 60 / 24

            for item in answer:
                item["RepresentativeValue"] = item["Count"] / total # convert to %. but config doesn't tell that they use unit `unidades` with this one

            answer.append({"Total_Values": total})

        return answer

    def _pos_process_status(self, answer, main_keywords):
        main_keywords_lower = [keyword.lower() for keyword in main_keywords]

        def keywords_in_list(must_have, main_keywords_lower):
                return all(keyword in main_keywords_lower for keyword in must_have)
        
        # Check if all the keywords "cancelados", "produto", and "acabado" are present in main_keywords
        condition1 = keywords_in_list(["cancelados", "produto", "acabado"], main_keywords_lower)

        # Check if "cancelados" is present as a substring (or full string) in any keyword 
        # while check if "produto acabado" is present as a full string or present as separete keywords
        condition2 = (any("cancelados" in keyword.lower() for keyword in main_keywords)
                      and ("produto acabado" in main_keywords_lower or keywords_in_list(["produto", "acabado"], main_keywords_lower)))

        if condition1 or condition2:
            indice = 2
            aa = [[sublista[0],sublista[indice]] for sublista in answer[0]["Data"]]
            answer[0]["Data"] = aa

        return answer

    def _postprocess_all(self, answer, main_keywords, DATE, after_posprocess_unit, api_upflux_unit, context_num):
        answer = self._pos_process_status(answer, main_keywords)
        answer = self._postprocess_answer(answer, after_posprocess_unit, api_upflux_unit, context_num)
        answer = self._pos_process(answer, DATE, after_posprocess_unit, api_upflux_unit)
        return answer

    def _request_specific_component(self, component_number, body_request):
        """
        Obtain answer.
        """
        components = body_request["KpiContext"]["Components"]
        component = [component for component in components if component["Id"]==component_number]
        body_request["KpiContext"]["Components"] = component
        self.headers["Processid"] = body_request["KpiContext"]["ProcessId"]
        payload = json.dumps(body_request)

        logger.info("requesting specific component", extra={
            "url": self.url,
            "headers": self.headers,
        })
        response = requests.request("POST", self.url, headers=self.headers, data=payload)

        if response.status_code == 200:
            answer = json.loads(response.text)
        else: # TODO: send message to user based on error
            logger.error("error on request specific component", extra={
                "response": f"{response.status_code} - text: {response.text} - reason: {response.reason} ",
                "payload": payload,
            })
            raise Exception(f"Status Code: {response.status_code} . Error: {response.text}")

        # get Filters used in request
        filters = {}

        ignore_dashboard_filters = component[0]["IgnoreComponentFilters"]

        # Get Component Filters
        if component[0]["FilterContext"] is not None:
            filters["component_filters"] = component[0]["FilterContext"]

        # Get Dashboard filters
        if ((not(ignore_dashboard_filters) and body_request["Filter"] is not None) or ("component_filters" not in filters.keys())):
            filters["dashboard_filters"] = body_request["Filter"]
        
        print(f"O retorno da API é {answer}")
        return answer, filters

    def _process_and_replace(self, filter_json, formated_period={}, date_setting_keys=["Filter", "parentHashFilter"], date_setter_component=["FilterContext"]):
        # 1. Process
        day_s, month_s, year_s = formated_period["DATE"]["STARTDATE"].split("/")
        day_f, month_f, year_f = formated_period["DATE"]["ENDDATE"].split("/")

        if month_f == "02" and day_f == "28" and calendar.isleap(int(year_f)):
            day_f = "29"

        start_date = "yyyy-mm-ddT00:00:00.000Z".replace("yyyy", year_s)
        start_date = start_date.replace("mm", month_s)
        start_date = start_date.replace("dd", day_s)

        end_date = "yyyy-mm-ddT23:59:59.000Z".replace("yyyy", year_f)
        end_date = end_date.replace("mm", month_f)
        end_date = end_date.replace("dd", day_f)

        print(f"new_start_date: {start_date}, new_end_date: {end_date}")

        # 2. Replace
        for date_setter in date_setting_keys:
            update_dates_in_json(filter_json, date_setter, start_date, "Start", end_date, "End")

        for date_setter in date_setter_component:
            for component in filter_json["KpiContext"]["Components"]:
                if (component[date_setter] and ("Start" in component[date_setter] or "start" in component[date_setter])):
                    update_dates_in_json(component, date_setter, start_date, "Start", end_date, "End")

        return filter_json

    def _get_date(self, period):
        if "DATE" in period:
            splitted_date = period["DATE"].split("-")
            period["DATE"] = {"STARTDATE": splitted_date[0], "ENDDATE": splitted_date[1]}

        return period

    def _update_load(self, DATE, payload_json):
        date_setting_keys = ["Filter", "parentHashFilter"]
        repo_root = find_git_root(os.getcwd())
        api_src_path = api_src_by_repo_root(repo_root)
        file_json = os.path.join(api_src_path, FILE_PATH, payload_json)
        d_json = read_qa_json(file_json)
        period = {"DATE": DATE}
        formated_period = self._get_date(period)
        d_json = self._process_and_replace(d_json, formated_period, date_setting_keys)
        return d_json

    def _ask_upflux_direct_payload(self, mapping_params, after_posprocess_unit, api_upflux_unit, scope_dict):
        MAIN_KEYWORDS = scope_dict['context_filters'][0]['main_keywords']
        DATE = scope_dict['context_filters'][1]['DATE']
        payload_json_filename = mapping_params["payload_json"]
        component_number = mapping_params["component_number"]
        
        if DATE:
            body_request = self._update_load(DATE, payload_json_filename)
        answer, filters = self._request_specific_component(component_number, body_request)
        answer = self._postprocess_all(answer, MAIN_KEYWORDS, DATE, after_posprocess_unit, api_upflux_unit, payload_json_filename[0])
        
        filters = self._postprocess_filters(filters, DATE)
        return answer, filters
    