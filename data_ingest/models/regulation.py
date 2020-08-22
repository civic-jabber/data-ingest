import uuid


class Regulation:
    def get_id(self):
        return uuid.uuid4().hex

    def get_title(self):
        raise NotImplementedError

    def get_description(self):
        raise NotImplementedError

    def get_text(self):
        raise NotImplementedError

    def get_summary(self):
        raise NotImplementedError

    def get_effective_date(self):
        raise NotImplementedError

    def get_point_of_contact(self):
        raise NotImplementedError

    def get_volume(self):
        raise NotImplementedError

    def get_issue(self):
        raise NotImplementedError
