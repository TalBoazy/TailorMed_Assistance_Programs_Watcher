"""
Asistance Program Entity Class
"""
class AssistanceProgramEntity:
    def __init__(self,url, name, eligible_treatments, status,grant_amount):
        self.url = url
        self.name=name
        self.eligible_treatments=eligible_treatments
        self.status=status
        self.grant_amount=grant_amount