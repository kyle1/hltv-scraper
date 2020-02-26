class Match:
    def __init__(self, url):
        self._match_id = None
        self._match_date_time = None
        self._match_description = None
        self._team_one_id = None
        self._team_two_id = None


class PickBan:
    def __init__(self, url):
        self._match_id = None
        self._pick_number = None
        self._team_id = None
        self._is_pick = None
        self._is_ban = None


class MatchMap:
    def __init__(self):
        self._match_id = None
        self._map_number = None
        self._map_name = None
        self._team_one_id = None
        self._team_two_id = None
        #todo