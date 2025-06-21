import requests

class UMLSClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.auth_endpoint = "https://utslogin.nlm.nih.gov/cas/v1/api-key"
        self.base_url = "https://uts-ws.nlm.nih.gov"
        self.version = "current"
        self.tgt = self.get_tgt()

    def get_tgt(self):
        params = {'apikey': self.api_key}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.auth_endpoint, data=params, headers=headers)
        if response.status_code == 201:
            return response.headers['location']
        raise Exception("Failed to obtain TGT")

    def get_service_ticket(self):
        params = {'service': 'http://umlsks.nlm.nih.gov'}
        response = requests.post(self.tgt, data=params)
        if response.status_code == 200:
            return response.text
        raise Exception("Failed to obtain service ticket")

    def search_term(self, term):
        ticket = self.get_service_ticket()
        search_url = f"{self.base_url}/rest/search/{self.version}"
        params = {'string': term, 'ticket': ticket}
        response = requests.get(search_url, params=params)
        results = response.json()
        return results['result']['results']

    def get_related_concepts(self, cui):
        ticket = self.get_service_ticket()
        url = f"{self.base_url}/rest/content/{self.version}/CUI/{cui}/relations"
        params = {'ticket': ticket}
        response = requests.get(url, params=params)
        results = response.json()
        return results['result']


def map_symptom_to_conditions(symptom, umls_client, max_conditions=5):
    search_results = umls_client.search_term(symptom)
    conditions = set()
    keywords = set(symptom.lower().split())

    for result in search_results:
        cui = result['ui']
        if cui != 'NONE':
            related = umls_client.get_related_concepts(cui)
            for concept in related:
                if concept.get('relationLabel') == 'RO' or 'RQ' in concept.get('additionalRelationLabel', ''):
                    related_name = concept['relatedIdName']
                    related_keywords = set(related_name.lower().split())
                    if keywords & related_keywords:
                        conditions.add(related_name)
                if len(conditions) >= max_conditions:
                    break
        if len(conditions) >= max_conditions:
            break

    return list(conditions)


def get_drugs_for_condition(condition):
    base_url = "https://api.fda.gov/drug/label.json"
    params = {'search': f'indications_and_usage:"{condition}"', 'limit': 5}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        drugs = []
        for entry in data.get('results', []):
            openfda = entry.get('openfda', {})
            brand = openfda.get('brand_name', [])
            generic = openfda.get('generic_name', [])
            drugs.extend(brand + generic)
        return list(set(drugs))
    return []
